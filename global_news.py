import os
import time
from dotenv import load_dotenv
from src.config.sheet import load_sheet
from src.collectors.yahoo import YahooCollector
from src.collectors.newsapi import NewsAPICollector
from src.collectors.google_rss import GoogleRSSCollector
from src.config.settings import Settings

load_dotenv()
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")


# ✅ 종목 50개씩 묶는 유틸
def chunked(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


# ✅ 시트 로딩
def load_global_tickers(sheet_id):
    sheet = load_sheet(sheet_id, worksheet_name="global")
    tickers = sheet.col_values(1)[1:]  # A열 (헤더 제외)
    return tickers, sheet


# ✅ 종목명 → 시트 행번호 탐색
def get_row_for_ticker(sheet, ticker_name):
    tickers = sheet.col_values(1)
    for i, name in enumerate(tickers):
        if name.strip() == ticker_name.strip():
            return i + 1
    return None


# ✅ 뉴스 수집 (Yahoo 3 + NewsAPI 1 + GoogleRSS 2)
def fetch_global_news(ticker):
    news_items = []

    yahoo = YahooCollector()
    yahoo_items = yahoo.fetch_news(ticker, count=3) or []
    for item in yahoo_items:
        news_items.append({
            "title": item["title"],
            "link": item["link"],
            "date": item["publish_date"],
            "snippet": item.get("snippet", "")
        })

    googlerss = GoogleRSSCollector()
    rss_items = googlerss.fetch_news(ticker, count=2) or []
    for item in rss_items:
        news_items.append({
            "title": item["title"],
            "link": item["link"],
            "date": item["publish_date"],
            "snippet": item.get("snippet", "")
        })

    newsapi = NewsAPICollector()
    newsapi_items = newsapi.fetch_news(ticker, count=1) or []
    for item in newsapi_items:
        news_items.append({
            "title": item["title"],
            "link": item["link"],
            "date": item["date"],
            "snippet": item.get("snippet", "")
        })

    return news_items


# ✅ 배치 실행 함수
def run_global_news_summary(sheet_id, batch_size=50):
    tickers, sheet = load_global_tickers(sheet_id)
    total_updated = 0

    # 종목별 뉴스 수집
    for batch in chunked(tickers, batch_size):
        batch_data = []
        row_map = {}

        for ticker in batch:
            print(f"🌍 [수집 중] {ticker}")
            row = get_row_for_ticker(sheet, ticker)
            if not row:
                print(f"⚠️ 종목 '{ticker}' 행 찾기 실패 → 건너뜀")
                continue

            news_items = fetch_global_news(ticker)

            values = [ticker]
            for item in news_items[:6]:  # 최대 6개 뉴스
                values.extend([item["title"], item["link"], item["date"]])
            while len(values) < 19:  # 부족할 경우 빈칸 채우기
                values.extend(["", "", ""])

            row_map[row] = values
            total_updated += 1

        # 일반 뉴스 데이터 업데이트
        batch_data = [
            {"range": f"A{row}:S{row}", "values": [row_map[row]]}
            for row in sorted(row_map.keys())
        ]

        if batch_data:
            sheet.batch_update(batch_data)
            print(f"✅ 배치 업데이트 완료: {len(batch_data)}개")

        time.sleep(2)

    print(f"\n🎯 전체 완료: 총 {total_updated}개 종목 처리됨")


# ✅ 실행
if __name__ == "__main__":
    run_global_news_summary(SHEET_ID)
