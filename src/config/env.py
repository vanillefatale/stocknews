# env_config.py
import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()

load_env()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
NAVER_CLIENT_ID =  os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
CX = os.getenv("CX")