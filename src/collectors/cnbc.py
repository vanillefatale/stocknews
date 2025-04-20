"""
CNBC news collector.
"""

import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Tuple

from cnbc_news import update_cnbc_sheet

from ..utils.translator import translate_with_claude
from ..utils.summarizer import summarize_with_claude
from ..utils.logger import setup_logger
from ..config.sheet import load_sheet
from ..config.settings import Settings

logger = setup_logger("cnbc")

class CNBCCollector:
    """CNBC news collector class."""
    
    def __init__(self, settings: Settings):
        """
        Initialize CNBC collector.
        
        Args:
            settings (Settings): Application settings
        """
        self.settings = settings
        self.sheet = load_sheet(
            settings.sheet_id,
            worksheet_name=settings.get_sheet_name("cnbc")
        )
        self.url = "https://www.cnbc.com/id/100003114/device/rss/rss.html"
        self.headers = {"User-Agent": "Mozilla/5.0"}
        
        logger.debug("Initialized CNBC collector")
    
    def fetch_news(self, count: int = None) -> Tuple[List[List[str]], List[List[str]]]:
        """
        Fetch news from CNBC RSS feed.
        
        Args:
            count (int, optional): Number of news items to fetch
            
        Returns:
            Tuple[List[List[str]], List[List[str]]]: Original and translated news
        """
        count = count or self.settings.get_news_settings("cnbc").get("count", 30)
        
        try:
            logger.info("Fetching CNBC news")
            res = requests.get(self.url, headers=self.headers)
            res.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to fetch CNBC RSS: {e}")
            return [], []

        soup = BeautifulSoup(res.content, "xml")
        items = soup.find_all("item")[:count]
        logger.info(f"Found {len(items)} news items")

        original_news = []
        translated_news = []

        for i, item in enumerate(items, 1):
            title = item.title.text.strip()
            description = item.description.text.strip()
            link = item.link.text.strip()
            pub_date_raw = item.pubDate.text.strip()

            try:
                pub_date = datetime.strptime(pub_date_raw, "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%d %H:%M")
            except Exception as e:
                logger.warning(f"Failed to parse date '{pub_date_raw}': {e}")
                pub_date = pub_date_raw

            logger.debug(f"Processing news item {i}/{len(items)}")
            
            # 원본 영문 뉴스 저장 (제목, 내용, 날짜, 링크)
            original_news.append([title, description, pub_date, link])
            
            # 제목과 내용 번역
            translated_title = translate_with_claude(title)
            translated_desc = translate_with_claude(description)
            
            # 번역된 뉴스 저장
            translated_news.append([translated_title, translated_desc])

        return original_news, translated_news
    
    def update_sheet(self) -> None:
        """Update Google Sheet with collected news."""
        logger.info("Starting sheet update")
        original_news, translated_news = self.fetch_news()

        if not original_news or not translated_news:
            logger.warning("No news to update")
            return

        settings = self.settings.get_news_settings("cnbc")
        update_range = settings.get("update_range", {})

        try:
            # 원본 영문 뉴스 업데이트
            self.sheet.update(
                update_range.get("original", "A2:D31"),
                original_news
            )
            logger.info("Updated original news")
            
            # 번역된 한국어 뉴스 업데이트
            self.sheet.update(
                update_range.get("translated", "A34:B63"),
                translated_news
            )
            logger.info("Updated translated news")
            
            logger.info("✅ CNBC news update completed")
        except Exception as e:
            logger.error(f"Failed to update sheet: {e}")

if __name__ == "__main__":
    update_cnbc_sheet(SHEET_ID) 