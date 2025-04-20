# news_naver.py

import re
import requests
from datetime import datetime, timedelta
from src.config.env import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET
from bs4 import BeautifulSoup
from typing import List, Dict, Optional


def is_recent(pubdate_str):
    """
    pubDate 문자열이 최근 3일 이내인지 확인 (RFC822 포맷)
    예시: 'Fri, 12 Apr 2025 09:34:00 +0900'
    """
    try:
        news_time = datetime.strptime(pubdate_str, "%a, %d %b %Y %H:%M:%S %z")
        now = datetime.now(news_time.tzinfo)
        return now - news_time <= timedelta(days=3)
    except Exception as e:
        print(f"⚠️ 날짜 파싱 실패: {e}")
        return False


def fetch_news(query, display=10):
    """
    네이버 뉴스에서 query 키워드로 뉴스 수집
    - 정확도순 정렬
    - 종목명 포함 + 3일 이내 뉴스만 허용
    - 최대 3건 반환
    """
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    params = {
        "query": query,
        "display": display,
        "start": 1,
        "sort": "sim"  # 정확도순
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ 네이버 뉴스 API 요청 실패: {e}")
        return []

    items = response.json().get("items", [])
    results = []

    for item in items:
        title = item["title"].replace("<b>", "").replace("</b>", "")
        desc = item["description"].replace("<b>", "").replace("</b>", "")
        link = item.get("originallink") or item.get("link")
        pubdate = item.get("pubDate")

        # 종목명이 제목에 없으면 제외
        if query not in title:
            continue

        # 날짜 필터
        if not pubdate or not is_recent(pubdate):
            continue

        # ✅ 날짜 포맷 변환
        try:
            parsed = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")
            formatted_date = parsed.strftime("%Y-%m-%d")
        except Exception as e:
            print(f"⚠️ 날짜 포맷 실패: {e}")
            formatted_date = "N/A"

        results.append({
            "title": title,
            "description": desc,
            "link": link,
            "date": formatted_date
        })

        if len(results) >= 3:
            break

    return results


class NaverCollector:
    """Naver Finance news collector class."""
    
    def __init__(self):
        """Initialize Naver collector."""
        self.base_url = "https://finance.naver.com/item/news_news.naver"
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        }
    
    def fetch_news(self, code: str, count: int = 5) -> List[Dict[str, str]]:
        """
        Fetch news for a specific stock code.
        
        Args:
            code (str): Stock code
            count (int): Number of news items to fetch
            
        Returns:
            List[Dict[str, str]]: List of news items
        """
        try:
            params = {
                "code": code,
                "page": 1
            }
            
            res = requests.get(
                self.base_url,
                params=params,
                headers=self.headers
            )
            res.raise_for_status()
            
            soup = BeautifulSoup(res.text, "html.parser")
            rows = soup.select("table.type5 tr")
            
            news_items = []
            for row in rows:
                # Skip header rows
                if not row.select_one("td.title"):
                    continue
                
                title_tag = row.select_one("td.title a")
                if not title_tag:
                    continue
                
                title = title_tag.text.strip()
                link = "https://finance.naver.com" + title_tag["href"]
                date = row.select_one("td:nth-child(3)").text.strip()
                
                news_items.append({
                    "title": title,
                    "link": link,
                    "publish_date": date,
                    "source": row.select_one("td:nth-child(2)").text.strip()
                })
                
                if len(news_items) >= count:
                    break
            
            return news_items
        except Exception as e:
            print(f"❌ 네이버 금융 뉴스 수집 실패 ({code}): {e}")
            return []
