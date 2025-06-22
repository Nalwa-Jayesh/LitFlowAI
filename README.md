# AI Publishing System - Enhanced Version

An intelligent content processing system that fetches, processes, and refines web content through AI agents and human-in-the-loop workflows with reinforcement learning capabilities.

## 🚀 Features

- 🔍 **Web Scraping**: Fetch content and screenshots from any URL using Playwright
- 🤖 **AI Processing**: Multi-agent system (Writer, Reviewer, Editor) powered by Google Gemini
- 👥 **Enhanced Human-in-the-Loop**: Multi-iteration review with 5 interaction modes
- 🧠 **Smart Retrieval**: RL-enhanced content search and ranking with ChromaDB
- 💾 **Advanced Version Control**: Comprehensive content versioning with metadata
- 📊 **Feedback Learning**: Reinforcement learning from user interactions

## 🛠️ Quick Setup

### 1. Install Dependencies
```bash
# Navigate to project directory
cd ai_pub-proto

# Activate virtual environment (if using one)
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install Python packages
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
```

### 2. Environment Configuration
Make sure your `.env` file contains:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Test Your Setup
```bash
# Quick test (essential components only)
python test_system.py --quick

# Full test suite
python test_system.py
```

## 📖 Usage

### Basic Processing
```bash
# Process a chapter with default settings (3 iterations max)
python main.py --mode process --url "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"

# Process with custom iteration limit
python main.py --mode process --url "https://example.com/content" --iterations 5
```

### Search Stored Content
```bash
# Search previously processed content
python main.py --mode search --query "gates of morning chapter"
```

## 🎛️ Human-in-the-Loop Options

During the review process, you have 5 options:

1. **`accept`** - ✅ Accept the current version
2. **`edit`** - ✏️ Manually edit the current version
3. **`regenerate`** - 🔄 Ask AI to regenerate based on your feedback
4. **`revert`** - ⏪ Go back to a previous version
5. **`compare`** - 🔍 Compare all versions side-by-side

### Example Human Review Session
```
🔄 HUMAN REVIEW - ITERATION 1/3
================================

📚 VERSION COMPARISON:
- ORIGINAL: 1,234 chars | 185 words
- AI_SPUN: 1,189 chars | 178 words  
- AI_REVIEWED: 1,245 chars | 188 words
- AI_EDITED: 1,203 chars | 181 words (🔄 CURRENT)

🤔 What would you like to do?
   1. 'accept'     - ✅ Accept current version
   2. 'edit'       - ✏️ Manually edit current version
   3. 'regenerate' - 🔄 Ask AI to regenerate with feedback
   4. 'revert'     - ⏪ Go back to a previous version
   5. 'compare'    - 🔍 Compare all versions side-by-side

👉 Enter your choice: regenerate
💬 Your feedback: make it more formal and add more technical detail
```

## 🧠 Reinforcement Learning Features

The system learns from your feedback to improve search results:

### Rating System
When searching, rate results 1-5:
- 1 = Very Poor
- 2 = Poor  
- 3 = Average
- 4 = Good
- 5 = Excellent

### Automatic Model Training
- RL model retrains every 10 feedback entries
- Uses cosine similarity, distance, and content length features
- Improves ranking over time based on your preferences

## 📁 Project Structure

```
ai_pub-proto/
├── ai_agents/           # AI processing agents
│   ├── writer.py       # Content rewriting
│   ├── reviewer.py     # Content review
│   └── editor.py       # Final editing
├── interface/          # Human interaction
│   └── human_loop.py   # Enhanced multi-iteration review
├── scraper/           # Web content fetching
│   └── fetcher.py     # Playwright-based scraper
├── storage/           # Data persistence
│   └── chromadb_handler.py  # Enhanced RL-based storage
├── utils/             # Utilities
│   ├── gemini_api.py  # Gemini API integration
│   └── prompts.py     # Enhanced AI prompts
├── main.py           # Main workflow orchestration
├── config.py         # System configuration
├── test_system.py    # Test suite
└── requirements.txt  # Dependencies
```

## ⚙️ Configuration

The system uses `config.py` for settings:

```python
from config import config, print_config

# View current configuration
print_config()

# Modify settings
config.max_human_iterations = 5
config.enable_rl_ranking = True
config.preview_length = 500
```

### Key Configuration Options
- `max_human_iterations`: Maximum review iterations (default: 3)
- `enable_rl_ranking`: Use RL for search ranking (default: True)
- `preview_length`: Text preview length (default: 300)
- `gemini_model`: AI model to use (default: "gemini-2.5-flash")

## 🔧 Advanced Usage

### Custom Style Preferences
```python
from ai_agents.writer import ai_writer

# Process with specific style
result = ai_writer(text, style_preferences="formal academic tone, technical language")
```

### Manual Storage Operations
```python
from storage.chromadb_handler import save_version, get_statistics

# Save with metadata
doc_id = save_version(url, content, {"version_type": "manual_edit", "quality": "high"})

# Get system statistics
get_statistics()
```

### Feedback Training
```python
from storage.chromadb_handler import submit_feedback

# Provide feedback for learning
submit_feedback("search query", "result content", reward=0.8)  # Scale: -1 to 1
```

## 🧪 Testing

### Quick Test (Essential Components)
```bash
python test_system.py --quick
```

### Full Test Suite
```bash
python test_system.py
```

Tests cover:
- ✅ Module imports
- ✅ Environment configuration
- ✅ Gemini API connectivity
- ✅ AI agents functionality
- ✅ Storage system
- ✅ Prompt generation
- ✅ Web scraping capabilities

## 🚨 Troubleshooting

### Common Issues

**❌ Import Errors**
```bash
pip install -r requirements.txt
```

**❌ Playwright Browser Missing**
```bash
playwright install chromium
```

**❌ Gemini API Key Error**
- Check `.env` file exists and contains `GEMINI_API_KEY=your_key`
- Verify API key is valid and has proper permissions

**❌ ChromaDB Errors**
- Delete any existing ChromaDB data: `rm -rf chromadb_data/`
- Restart the application

**❌ Network/Scraping Issues**
- Check internet connection
- Some websites may block automated access
- Try different URLs for testing

### Debug Mode
```bash
# Enable debug logging
python main.py --mode process --url "..." --debug
```

## 📊 Performance Tips

1. **Batch Processing**: Process multiple chapters in sequence for better RL training
2. **Feedback Quality**: Provide consistent, detailed feedback for better learning
3. **Iteration Limits**: Use 2-3 iterations for efficiency vs. 5+ for maximum quality
4. **Style Consistency**: Use similar style preferences across related content

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Custom AI model integration
- [ ] Batch processing workflows
- [ ] Advanced RL algorithms (PPO, DQN)
- [ ] Web interface for easier interaction
- [ ] Export to various formats (PDF, EPUB, etc.)

## 📝 Example Workflow

1. **Start Processing**:
   ```bash
   python main.py --mode process --url "https://example.com/chapter1"
   ```

2. **AI Processing**: System automatically runs Writer → Reviewer → Editor

3. **Human Review**: Interactive multi-iteration refinement

4. **Final Storage**: Processed content saved with metadata

5. **Future Retrieval**: 
   ```bash
   python main.py --mode search --query "chapter1 content"
   ```

6. **Continuous Learning**: Rate search results to improve future recommendations

## 🤝 Contributing

Feel free to enhance the system by:
- Adding new AI agents
- Improving prompt engineering
- Implementing advanced RL algorithms
- Adding new export formats
- Enhancing the user interface

---

**Happy Publishing!** 🚀📚✨