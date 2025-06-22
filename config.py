import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """Configuration settings for the AI Publishing System"""

    # API Configuration
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = "gemini-2.5-flash"

    # Workflow Configuration
    max_human_iterations: int = 3
    auto_screenshot: bool = True

    # AI Model Configuration
    embedding_model: str = "all-MiniLM-L6-v2"

    # Storage Configuration
    chromadb_path: str = "./chromadb_data"
    enable_rl_ranking: bool = True
    rl_retrain_frequency: int = 10
    rl_model_path: str = "rl_scoring_model.pkl"

    # UI Configuration
    preview_length: int = 300
    show_debug_info: bool = False
    use_enhanced_prompts: bool = True

    # Processing Configuration
    min_text_length: int = 50
    max_text_length: int = 100000
    preserve_formatting: bool = True

    # Screenshot Configuration
    screenshot_path: str = "chapter_screenshot.png"
    full_page_screenshot: bool = True

    # Logging Configuration
    log_level: str = "INFO"
    log_file: str = "ai_publishing.log"

    def validate(self):
        """Validate configuration settings"""
        errors = []

        if not self.gemini_api_key:
            errors.append("GEMINI_API_KEY is required")

        if self.max_human_iterations < 1:
            errors.append("max_human_iterations must be at least 1")

        if self.preview_length < 50:
            errors.append("preview_length must be at least 50")

        if self.rl_retrain_frequency < 1:
            errors.append("rl_retrain_frequency must be at least 1")

        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")

        return True

    def get_display_config(self):
        """Get configuration for display (without sensitive info)"""
        return {
            "gemini_model": self.gemini_model,
            "max_human_iterations": self.max_human_iterations,
            "auto_screenshot": self.auto_screenshot,
            "embedding_model": self.embedding_model,
            "enable_rl_ranking": self.enable_rl_ranking,
            "preview_length": self.preview_length,
            "show_debug_info": self.show_debug_info,
            "use_enhanced_prompts": self.use_enhanced_prompts
        }

    def update_from_args(self, args):
        """Update configuration from command line arguments"""
        if hasattr(args, 'iterations') and args.iterations:
            self.max_human_iterations = args.iterations

        if hasattr(args, 'debug') and args.debug:
            self.show_debug_info = True
            self.log_level = "DEBUG"

        if hasattr(args, 'no_rl') and args.no_rl:
            self.enable_rl_ranking = False

# Global configuration instance
config = Config()

def load_config(config_file=None):
    """Load configuration from file if provided"""
    global config

    if config_file and os.path.exists(config_file):
        try:
            import json
            with open(config_file, 'r') as f:
                config_data = json.load(f)

            # Update config with file data
            for key, value in config_data.items():
                if hasattr(config, key):
                    setattr(config, key, value)

            print(f"✅ Configuration loaded from {config_file}")
        except Exception as e:
            print(f"⚠️ Error loading config file: {e}")

    # Validate configuration
    try:
        config.validate()
        print("✅ Configuration validated successfully")
    except ValueError as e:
        print(f"❌ Configuration validation failed: {e}")
        raise

def save_config(config_file="config.json"):
    """Save current configuration to file"""
    try:
        import json
        config_dict = {
            "gemini_model": config.gemini_model,
            "max_human_iterations": config.max_human_iterations,
            "auto_screenshot": config.auto_screenshot,
            "embedding_model": config.embedding_model,
            "enable_rl_ranking": config.enable_rl_ranking,
            "rl_retrain_frequency": config.rl_retrain_frequency,
            "preview_length": config.preview_length,
            "show_debug_info": config.show_debug_info,
            "use_enhanced_prompts": config.use_enhanced_prompts,
            "min_text_length": config.min_text_length,
            "max_text_length": config.max_text_length,
            "preserve_formatting": config.preserve_formatting,
            "log_level": config.log_level
        }

        with open(config_file, 'w') as f:
            json.dump(config_dict, f, indent=2)

        print(f"✅ Configuration saved to {config_file}")
        return True
    except Exception as e:
        print(f"❌ Error saving config: {e}")
        return False

def print_config():
    """Print current configuration"""
    print("\n🔧 CURRENT CONFIGURATION:")
    print("=" * 50)

    display_config = config.get_display_config()
    for key, value in display_config.items():
        print(f"   {key}: {value}")

    print("=" * 50)