"""
Application settings and configuration.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings class."""
    
    def __init__(self):
        """Initialize settings."""
        # Google Sheets
        self.sheet_id = os.getenv("GOOGLE_SHEET_ID")
        
        # API Keys
        self.claude_api_key = os.getenv("CLAUDE_API_KEY")
        self.newsapi_key = os.getenv("NEWSAPI_KEY")
        
        # Claude API Settings
        self.claude_settings = {
            "model": "claude-3-5-haiku-20241022",
            "max_tokens": 800,
            "temperature": 0.3
        }
        
        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.debug = os.getenv("DEBUG", "False").lower() == "true"
        
        # Sheet Names
        self.sheet_names = {
            "cnbc": "cnbc",
            "global": "global",
            "korea": "korea"
        }
        
        # News Collection Settings
        self.news_settings = {
            "cnbc": {
                "count": 30,
                "update_range": {
                    "original": "A2:D31",
                    "translated": "A34:B63"
                }
            },
            "yahoo": {
                "count": 3
            },
            "newsapi": {
                "count": 1
            },
            "google": {
                "count": 2
            },
            "naver": {
                "count": 5
            }
        }
    
    def get_sheet_name(self, key: str) -> str:
        """Get sheet name by key."""
        return self.sheet_names.get(key, "")
    
    def get_news_settings(self, source: str) -> Dict[str, Any]:
        """Get news settings by source."""
        return self.news_settings.get(source, {}) 