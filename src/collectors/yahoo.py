"""
Yahoo Finance news collector.
"""

import feedparser
from typing import List, Dict, Optional
from datetime import datetime
from urllib.parse import quote

class YahooCollector:
    """Yahoo Finance news collector class."""
    
    def __init__(self):
        """Initialize Yahoo collector."""
        self.base_url = "https://feeds.finance.yahoo.com/rss/2.0/headline?s={}&region=US&lang=en-US"
    
    def fetch_news(self, ticker: str, count: int = 3) -> List[Dict[str, str]]:
        """
        Fetch news for a specific ticker.
        
        Args:
            ticker (str): Stock ticker symbol
            count (int): Number of news items to fetch
            
        Returns:
            List[Dict[str, str]]: List of news items
        """
        try:
            # URL encode the ticker to handle spaces and special characters
            encoded_ticker = quote(ticker)
            feed = feedparser.parse(self.base_url.format(encoded_ticker))
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
            print(f"❌ Yahoo Finance 뉴스 수집 실패 ({ticker}): {e}")
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
            dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
            return dt.strftime("%Y-%m-%d")
        except:
            return date_str
