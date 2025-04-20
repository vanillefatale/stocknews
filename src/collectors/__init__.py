"""
News collectors for different sources.
"""

from .cnbc import CNBCCollector
from .yahoo import YahooCollector
from .newsapi import NewsAPICollector
from .google_rss import GoogleRSSCollector
from .naver import NaverCollector

__all__ = [
    'CNBCCollector',
    'YahooCollector',
    'NewsAPICollector',
    'GoogleRSSCollector',
    'NaverCollector',
] 