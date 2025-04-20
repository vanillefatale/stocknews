# cnbc_news.py

import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from src.config.sheet import load_sheet

load_dotenv()
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

def fetch_cnbc_rss(count=10):
    url = "https://www.cnbc.com/id/100003114/device/rss/rss.html"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
    except Exception as e:
        print(f"❌ CNBC RSS 수집 실패: {e}")
        return []

    soup = BeautifulSoup(res.content, "xml")
    items = soup.find_all("item")[:count]

    result = []
    for item in items:
        title = item.title.text.strip()
        description = item.description.text.strip()
        link = item.link.text.strip()
        pub_date_raw = item.pubDate.text.strip()

        try:
            pub_date = datetime.strptime(pub_date_raw, "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%d %H:%M")
        except:
            pub_date = pub_date_raw

        result.append([title, description, pub_date, link])

    return result

def update_cnbc_sheet(sheet_id):
    sheet = load_sheet(sheet_id, worksheet_name="cnbc")
    news = fetch_cnbc_rss(count=30)

    if not news:
        print("❌ 뉴스 없음")
        return

    # A2:D11 영역 업데이트
    # sheet.update("A2:D31", news)
    sheet.update(range_name='A2:D31', values=news)
    print("✅ CNBC 뉴스 업데이트 완료")

if __name__ == "__main__":
    update_cnbc_sheet(SHEET_ID)
