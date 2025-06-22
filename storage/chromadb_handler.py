import chromadb
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
import torch
import pickle
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from config import config

# Ensure the DB path exists
os.makedirs(config.chromadb_path, exist_ok=True)

# Use a persistent client to save data to disk
client = chromadb.PersistentClient(path=config.chromadb_path)
collection = client.get_or_create_collection(name="chapters")
model = SentenceTransformer(config.embedding_model)

# Enhanced reward memory and RL scoring
reward_memory = []
scoring_model = None
RL_TRAIN_THRESHOLD = 10

def load_scoring_model():
    """Load trained scoring model if it exists"""
    global scoring_model
    model_path = "rl_scoring_model.pkl"
    if os.path.exists(model_path):
        try:
            with open(model_path, "rb") as f:
                scoring_model = pickle.load(f)
            print("🧠 RL scoring model loaded!")
        except Exception as e:
            print(f"⚠️ Failed to load scoring model: {e}")

# Load model on import
load_scoring_model()

def save_version(url, text, metadata=None):
    """Save version with enhanced metadata and active status."""
    embedding = model.encode(text).tolist()

    # New versions are active by default
    full_metadata = {
        "url": url,
        "timestamp": str(datetime.now()),
        "char_count": len(text),
        "word_count": len(text.split()),
        "is_active": True
    }

    if metadata:
        full_metadata.update(metadata)

    doc_id = f"{url.replace('/', '_')}_{int(datetime.now().timestamp())}"

    collection.add(
        documents=[text],
        metadatas=[full_metadata],
        ids=[doc_id],
        embeddings=[embedding]
    )

    print(f"💾 Version saved with ID: {doc_id}")
    return doc_id


def retrieve_best_match(query, n_results=5):
    """Retrieve with RL-based ranking, searching only active versions."""
    query_vec = model.encode(query).tolist()

    # Get more results than needed for re-ranking, searching only active documents
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=min(n_results * 2, 20),
        where={"is_active": True}
    )

    if not results or not results.get('documents') or not results['documents'][0]:
        print("ℹ️ No documents found in the database.")
        return "No match found."

    # Decide whether to use RL ranking
    use_rl = scoring_model and len(reward_memory) >= RL_TRAIN_THRESHOLD
    
    if use_rl:
        print("🧠 Applying RL-based ranking to results...")
        ranked_results = apply_rl_ranking(query, results, n_results)
        if ranked_results and ranked_results["documents"]:
            return ranked_results["documents"][0]
        else:
            print("⚠️ RL ranking returned no results, falling back to semantic.")
            return results['documents'][0][0]
    else:
        print("ℹ️ Using default semantic search.")
        if not scoring_model:
            print(f"   (Reason: RL model not trained yet. Provide at least {RL_TRAIN_THRESHOLD} ratings to train.)")
        elif len(reward_memory) < RL_TRAIN_THRESHOLD:
            print(f"   (Reason: Not enough feedback. {len(reward_memory)}/{RL_TRAIN_THRESHOLD} ratings provided.)")
        return results['documents'][0][0]

def retrieve_with_rl_ranking(query, n_results=5):
    """Retrieve multiple results with RL-based ranking"""
    query_vec = model.encode(query).tolist()

    # Get more results than needed for re-ranking
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=min(n_results * 2, 20)
    )

    if not results['documents'][0]:
        return {"documents": [], "metadatas": [], "scores": []}

    # Apply RL-based re-ranking if model is trained
    if scoring_model and len(reward_memory) > 10:
        return apply_rl_ranking(query, results, n_results)

    # Fallback to semantic similarity
    return {
        "documents": results['documents'][0][:n_results],
        "metadatas": results['metadatas'][0][:n_results],
        "scores": results['distances'][0][:n_results]
    }


def submit_feedback(query, result, reward):
    """Submit feedback for RL training"""
    query_embedding = model.encode(query).tolist()
    result_embedding = model.encode(result).tolist()

    feedback_entry = {
        "query": query,
        "query_embedding": query_embedding,
        "result": result,
        "result_embedding": result_embedding,
        "reward": reward,
        "timestamp": datetime.now()
    }

    reward_memory.append(feedback_entry)
    print(f"📊 Feedback recorded: Query='{query[:50]}...' Reward={reward}")

    # Retrain model when threshold is met
    if len(reward_memory) >= RL_TRAIN_THRESHOLD and len(reward_memory) % 5 == 0:
        print(f"📈 Reached {len(reward_memory)} feedback entries. Triggering model retraining...")
        train_scoring_model()

def train_scoring_model():
    """Train RL-based scoring model using a pipeline for robustness."""
    global scoring_model

    if len(reward_memory) < RL_TRAIN_THRESHOLD:
        print(f"ℹ️ Skipping training, not enough data ({len(reward_memory)}/{RL_TRAIN_THRESHOLD}).")
        return

    print("🧠 Training RL scoring model with new data...")

    # Prepare training data
    X = []
    y = []

    for entry in reward_memory:
        q_emb = np.array(entry["query_embedding"])
        r_emb = np.array(entry["result_embedding"])
        cosine_sim = np.dot(q_emb, r_emb) / (np.linalg.norm(q_emb) * np.linalg.norm(r_emb))
        euclidean_dist = np.linalg.norm(q_emb - r_emb)
        features = [cosine_sim, euclidean_dist, len(entry["result"])]
        X.append(features)
        y.append(entry["reward"])

    # Create a pipeline with a scaler and the model for robustness
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', LinearRegression())
    ])
    
    scoring_model = pipeline
    scoring_model.fit(X, y)

    save_scoring_model()
    print("✅ RL scoring model updated and saved!")

def apply_rl_ranking(query, results, n_results):
    """Apply RL-based ranking to results efficiently without re-encoding."""
    query_emb = np.array(model.encode(query))

    doc_ids = results['ids'][0]
    if not doc_ids:
        return {"documents": [], "metadatas": [], "scores": []}
        
    try:
        retrieved_data = collection.get(ids=doc_ids, include=['embeddings', 'documents', 'metadatas'])
        embedding_map = {id: emb for id, emb in zip(retrieved_data['ids'], retrieved_data['embeddings'])}
    except Exception as e:
        print(f"⚠️ Could not fetch embeddings for re-ranking, falling back. Error: {e}")
        return None

    scored_results = []
    
    for i, doc_id in enumerate(retrieved_data['ids']):
        doc_emb = np.array(embedding_map.get(doc_id))
        doc_text = retrieved_data['documents'][i]
        
        if doc_emb is None:
            continue

        # Calculate features
        cosine_sim = np.dot(query_emb, doc_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(doc_emb))
        euclidean_dist = np.linalg.norm(query_emb - doc_emb)
        doc_length = len(doc_text)
        features = [[cosine_sim, euclidean_dist, doc_length]]

        # Predict score using RL model
        rl_score = scoring_model.predict(features)[0]

        scored_results.append({
            "document": doc_text,
            "metadata": retrieved_data['metadatas'][i],
            "rl_score": rl_score
        })

    # Sort by RL score (descending)
    scored_results.sort(key=lambda x: x["rl_score"], reverse=True)

    # Return top N results
    top_results = scored_results[:n_results]

    return {
        "documents": [r["document"] for r in top_results],
        "metadatas": [r["metadata"] for r in top_results],
        "scores": [r["rl_score"] for r in top_results]
    }

def save_scoring_model():
    """Save trained scoring model"""
    if scoring_model:
        try:
            with open("rl_scoring_model.pkl", "wb") as f:
                pickle.dump(scoring_model, f)
        except Exception as e:
            print(f"⚠️ Failed to save scoring model: {e}")

def get_statistics():
    """Get statistics about stored content and feedback"""
    try:
        # Get collection stats
        collection_count = collection.count()
        feedback_count = len(reward_memory)

        print(f"\n📊 STORAGE STATISTICS:")
        print(f"   📚 Stored documents: {collection_count}")
        print(f"   💭 Feedback entries: {feedback_count}")
        print(f"   🧠 RL model trained: {'Yes' if scoring_model else 'No'}")

        if feedback_count > 0:
            rewards = [entry["reward"] for entry in reward_memory]
            avg_reward = sum(rewards) / len(rewards)
            print(f"   ⭐ Average reward: {avg_reward:.2f}")

    except Exception as e:
        print(f"❌ Error getting statistics: {e}")

def list_versions_for_url(url):
    """List all versions, active and inactive, for a given URL."""
    print(f"📄 Listing all versions for URL: {url}")
    versions = collection.get(where={"url": url}, include=["metadatas", "documents"])
    if not versions or not versions['ids']:
        print("   No versions found.")
        return None
    return versions

def delete_version_by_id(doc_id):
    """Permanently delete a specific version by its ID."""
    try:
        collection.delete(ids=[doc_id])
        print(f"✅ Version '{doc_id}' deleted successfully.")
        return True
    except Exception as e:
        print(f"❌ Error deleting version '{doc_id}': {e}")
        return False

def set_active_version(doc_id_to_activate):
    """Set a specific version as active, and all others for that URL as inactive."""
    # Get the URL from the version we want to activate
    item = collection.get(ids=[doc_id_to_activate], include=["metadatas"])
    if not item['ids']:
        print(f"❌ Version ID '{doc_id_to_activate}' not found.")
        return False
        
    url = item['metadatas'][0].get('url')
    if not url:
        print("❌ Could not find URL for the specified version. Cannot proceed.")
        return False

    # Get all versions for that URL
    all_versions = collection.get(where={"url": url}, include=["metadatas"])
    
    ids_to_update = []
    metadatas_to_update = []

    for i, doc_id in enumerate(all_versions['ids']):
        meta = all_versions['metadatas'][i]
        meta['is_active'] = (doc_id == doc_id_to_activate)
        ids_to_update.append(doc_id)
        metadatas_to_update.append(meta)
        
    collection.update(ids=ids_to_update, metadatas=metadatas_to_update)
    print(f"✅ Version '{doc_id_to_activate}' is now the ONLY active version for URL: {url}")
    return True