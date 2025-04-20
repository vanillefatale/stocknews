# kr_news.py

import os
from dotenv import load_dotenv
from src.config.sheet import load_sheet
from datetime import datetime
import feedparser
from src.collectors.naver import fetch_news
from urllib.parse import quote
import time

# ✅ 환경변수 로딩
load_dotenv()
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

def get_google_rss_news(ticker, count=5):
    """
    Google 뉴스 RSS 기반 종목 뉴스 수집
    ticker: 종목명 (예: '삼성전자')
    count: 가져올 뉴스 개수
    """
    try:
        # URL 인코딩 적용
        encoded_ticker = quote(ticker)
        url = f"https://news.google.com/rss/search?q={encoded_ticker}&hl=ko&gl=KR&ceid=KR:ko"
        
        # 요청 시도
        feed = feedparser.parse(url)
        
        # 피드가 비어있는지 확인
        if not feed.entries:
            print(f"⚠️ 구글 뉴스 검색 결과 없음: {ticker}")
            return None

        results = []
        for entry in feed.entries[:count]:
            raw_date = entry.published if "published" in entry else "N/A"

            try:
                parsed_date = datetime.strptime(raw_date, "%a, %d %b %Y %H:%M:%S %Z")
                publish_date = parsed_date.strftime("%Y-%m-%d")
            except Exception as e:
                print(f"⚠️ 날짜 파싱 실패 ({ticker}): {e}")
                publish_date = "N/A"

            results.append({
                "title": entry.title,
                "link": entry.link,
                "snippet": entry.summary,
                "lang": "lang_ko",
                "publish_date": publish_date
            })

        return results if results else None
    except Exception as e:
        print(f"❌ 구글 뉴스 RSS 수집 실패 ({ticker}): {e}")
        return None

# ✅ 시트 불러오기 + 종목 리스트 추출
def load_kr_tickers(sheet_id):
    sheet = load_sheet(sheet_id, worksheet_name="kr")
    tickers = sheet.col_values(1)[1:]  # A열 종목명 (헤더 제외)
    return tickers, sheet

# ✅ 종목명 → 시트 행 번호 찾기
def get_row_for_ticker(sheet, ticker_name):
    tickers = sheet.col_values(1)
    for i, name in enumerate(tickers):
        if name.strip() == ticker_name.strip():
            return i + 1  # 1-based index
    return None

# ✅ 뉴스 수집 (Naver + Google RSS)
def fetch_kr_news(ticker):
    news_items = []

    try:
        # 네이버 뉴스 먼저 수집
        naver_items = fetch_news(ticker, display=10) or []
        for item in naver_items[:3]:
            news_items.append({
                "title": item["title"],
                "link": item["link"],
                "date": item["date"]
            })

        # 구글 뉴스 수집
        rss_items = get_google_rss_news(ticker, count=3) or []
        for item in rss_items[:3]:
            news_items.append({
                "title": item["title"],
                "link": item["link"],
                "date": item["publish_date"]
            })
    except Exception as e:
        print(f"❌ 뉴스 수집 중 오류 발생 ({ticker}): {e}")

    return news_items

# ✅ 시트에 뉴스 쓰기 (A~S열)
def update_kr_sheet(sheet, row, ticker, news_items):
    try:
        values = [ticker]
        for item in news_items:
            values.extend([item["title"], item["link"], item["date"]])
        while len(values) < 19:
            values.extend(["", "", ""])
        sheet.update(f"A{row}:S{row}", [values])
    except Exception as e:
        print(f"❌ 시트 업데이트 실패 ({ticker}): {e}")

# ✅ 전체 실행
def run_kr_news_summary(sheet_id):
    tickers, sheet = load_kr_tickers(sheet_id)
    total_processed = 0

    for ticker in tickers:
        try:
            print(f"\n🔍 {ticker}")
            row = get_row_for_ticker(sheet, ticker)

            if not row:
                print(f"⚠️ 종목 '{ticker}'의 위치를 찾을 수 없음 → 건너뜀")
                continue

            news_items = fetch_kr_news(ticker)

            if not news_items:
                print("❌ 뉴스 없음")
                continue

            update_kr_sheet(sheet, row, ticker, news_items)
            print("✅ 완료")
            total_processed += 1
            
            # API 호출 간 간격 두기
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ 종목 처리 중 오류 발생 ({ticker}): {e}")
            continue
    
    print(f"\n🎯 전체 완료: 총 {total_processed}개 종목 처리됨")

# ✅ 메인
if __name__ == "__main__":
    run_kr_news_summary(SHEET_ID)
