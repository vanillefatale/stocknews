"""
Google RSS news collector.
"""

import feedparser
from typing import List, Dict, Optional
from datetime import datetime
from urllib.parse import quote

class GoogleRSSCollector:
    """Google RSS news collector class."""
    
    def __init__(self):
        """Initialize Google RSS collector."""
        self.base_url = "https://news.google.com/rss/search?q={}&hl=en-US&gl=US&ceid=US:en"
    
    def fetch_news(self, query: str, count: int = 2) -> List[Dict[str, str]]:
        """
        Fetch news for a specific query.
        
        Args:
            query (str): Search query
            count (int): Number of news items to fetch
            
        Returns:
            List[Dict[str, str]]: List of news items
        """
        try:
            encoded_query = quote(query)
            feed = feedparser.parse(self.base_url.format(encoded_query))
            items = feed.entries[:count]
            
            news_items = []
            for item in items:
                news_items.append({
                    "title": item.title,
                    "link": item.link,
                    "publish_date": self._parse_date(item.published),
                    "snippet": item.get("summary", "")
                })
            
            return news_items
        except Exception as e:
            print(f"❌ Google RSS 뉴스 수집 실패 ({query}): {e}")
            return []
    
    def _parse_date(self, date_str: str) -> str:
        """
        Parse date string to formatted date.
        
        Args:
            date_str (str): Date string from RSS feed
            
        Returns:
            str: Formatted date string
        """
        try:
            dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
            return dt.strftime("%Y-%m-%d")
        except:
            return date_str
