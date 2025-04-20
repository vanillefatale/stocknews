from datetime import datetime
import feedparser
import urllib.parse 

def get_google_rss_global_news(ticker, count=5):
    """
    Google 뉴스 RSS (영어) 기반 글로벌 종목 뉴스 수집
    query: 검색어 (예: 'Nvidia')
    count: 가져올 뉴스 개수
    """
    query = urllib.parse.quote_plus(ticker)  # ← 공백 포함 인코딩
    url = f"https://news.google.com/rss/search?q={query}&hl=en&gl=US&ceid=US:en"
    feed = feedparser.parse(url)

    results = []
    for entry in feed.entries[:count]:
        raw_date = entry.published if "published" in entry else "N/A"

        try:
            parsed_date = datetime.strptime(raw_date, "%a, %d %b %Y %H:%M:%S %Z")
            publish_date = parsed_date.strftime("%Y-%m-%d")
        except:
            publish_date = "N/A"

        results.append({
            "title": entry.title,
            "link": entry.link,
            "snippet": entry.summary,
            "lang": "lang_en",
            "publish_date": publish_date
        })

    return results if results else None
