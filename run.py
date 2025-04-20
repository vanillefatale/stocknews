"""
Main execution file for stock news collection.
"""

import os
from dotenv import load_dotenv
import time
from global_news import run_global_news_summary
from kr_news import run_kr_news_summary
from news_cnbc import update_cnbc_sheet

def main():
    # Load environment variables
    load_dotenv()
    SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
    
    print("\n🇰🇷 한국 뉴스 수집 시작...")
    run_kr_news_summary(SHEET_ID)
    time.sleep(2)
    
    print("\n🌍 글로벌 뉴스 수집 시작...")
    run_global_news_summary(SHEET_ID)
    time.sleep(2)  # API 호출 간 간격 두기
    
    print("\n📈 CNBC 뉴스 수집 시작...")
    update_cnbc_sheet()
    
    print("\n✨ 모든 뉴스 수집 완료!")

if __name__ == "__main__":
    main()
