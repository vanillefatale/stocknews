# news_newsapi.py

"""
NewsAPI collector for financial news.
"""

import os
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta

class NewsAPICollector:
    """NewsAPI collector class."""
    
    def __init__(self):
        """Initialize NewsAPI collector."""
        self.api_key = os.getenv("NEWSAPI_KEY")
        self.base_url = "https://newsapi.org/v2/everything"
        
        if not self.api_key:
            raise ValueError("NewsAPI key not found in environment variables")
    
    def fetch_news(self, query: str, count: int = 1) -> List[Dict[str, str]]:
        """
        Fetch news for a specific query.
        
        Args:
            query (str): Search query
            count (int): Number of news items to fetch
            
        Returns:
            List[Dict[str, str]]: List of news items
        """
        try:
            # Get date range for last 7 days
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            params = {
                "q": query,
                "apiKey": self.api_key,
                "language": "en",
                "sortBy": "relevancy",
                "pageSize": count,
                "from": start_date.strftime("%Y-%m-%d"),
                "to": end_date.strftime("%Y-%m-%d")
            }
            
            res = requests.get(self.base_url, params=params)
            res.raise_for_status()
            data = res.json()
            
            if data["status"] != "ok":
                raise Exception(f"API Error: {data.get('message', 'Unknown error')}")
            
            news_items = []
            for article in data["articles"][:count]:
                news_items.append({
                    "title": article["title"],
                    "link": article["url"],
                    "date": article["publishedAt"].split("T")[0],
                    "snippet": article["description"] or article["content"] or ""
                })
            
            return news_items
        except Exception as e:
            print(f"❌ NewsAPI 뉴스 수집 실패 ({query}): {e}")
            return []
