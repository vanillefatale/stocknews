import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from src.utils.sheets import load_sheet
from src.utils.translator import translate_with_claude

# Load environment variables
load_dotenv()
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

def fetch_cnbc_rss():
    """
    Fetch and parse CNBC RSS feeds.
    """
    try:
        # CNBC RSS feed URL
        # url = "https://www.cnbc.com/id/10000664/device/rss/rss.html"
        #전체 Top News	https://www.cnbc.com/id/100003114/device/rss/rss.html
        #World News	https://www.cnbc.com/id/100727362/device/rss/rss.html
        #Finance	https://www.cnbc.com/id/10000664/device/rss/rss.html
        #Technology	https://www.cnbc.com/id/19854910/device/rss/rss.html
        #Markets	https://www.cnbc.com/id/10001147/device/rss/rss.html
        url = "https://www.cnbc.com/id/100003114/device/rss/rss.html"
        # Set headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        
        # Fetch RSS feed
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse XML content
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        # Collect news items
        original_news = []
        translated_news = []
        
        for item in items[:30]:  # Get first 30 items
            title = item.title.text
            content = item.description.text
            pub_date = item.pubDate.text
            link = item.link.text
            
            # Store original news
            original_news.append([title, content, pub_date, link])
            
            # Translate title and content
            translated_title = translate_with_claude(title)
            translated_content = translate_with_claude(content)
            
            # Store translated news
            translated_news.append([translated_title, translated_content])
            
            print(f"Processed: {title}")  # Add progress indicator
        
        return original_news, translated_news
        
    except Exception as e:
        print(f"Error fetching CNBC RSS: {str(e)}")
        return [], []

def update_cnbc_sheet():
    """
    Update Google Sheet with CNBC news.
    """
    try:
        # Get news data
        original_news, translated_news = fetch_cnbc_rss()
        
        if not original_news or not translated_news:
            print("❌ No news data to update")
            return
        
        # Load worksheet directly
        worksheet = load_sheet(SHEET_ID, "cnbc")
        if not worksheet:
            print("❌ Failed to load Google Sheet")
            return
        
        # Update original news (A2:D31)
        worksheet.update(range_name='A2:D31', values=original_news)

        # Update translated news (A34:B63)
        worksheet.update(range_name='A34:B63', values=translated_news)
        
        print("✅ CNBC 뉴스 업데이트 완료")
        
    except Exception as e:
        print(f"Error updating CNBC sheet: {str(e)}")

if __name__ == "__main__":
    update_cnbc_sheet() 