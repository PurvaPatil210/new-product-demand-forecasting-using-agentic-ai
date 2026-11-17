import requests
import feedparser  
import numpy as np
from pytrends.request import TrendReq
from datetime import datetime, timedelta


class MarketIntelligenceAgent:
    """
    Collects external demand signals and converts them into
    a single normalized trend factor.
    """

    def run(self, new_product: dict) -> float:
        keyword = self._build_keyword(new_product)

        google_trend = self._google_trends_score(keyword)
        news_trend = self._news_buzz_score(keyword)

        trend_score = (
            0.55 * google_trend +
            0.45 * news_trend 
        )

        # Convert 0–1 score into demand multiplier
        trend_factor = 1 + trend_score * 0.4   # max +40%

        return round(trend_factor, 2)


    def _build_keyword(self, new_product: dict) -> str:
        return f"{new_product['brand']} {new_product['sub_category']}"

    def _google_trends_score(self, keyword: str) -> float:
        try:
            pytrends = TrendReq(hl="en-US", tz=330)
            pytrends.build_payload(
                [keyword],
                timeframe="today 12-m"
            )

            interest = pytrends.interest_over_time()
            if interest.empty:
                return 0.0

            avg_interest = interest[keyword].mean()
            return min(avg_interest / 100, 1.0)

        except Exception:
            return 0.0

    def _news_buzz_score(self, keyword: str) -> float:
        try:
            rss_url = (
                "https://news.google.com/rss/search?"f"q={keyword}&hl=en-IN&gl=IN&ceid=IN:en"
            )
            feed = feedparser.parse(rss_url)

            last_30_days = datetime.now() - timedelta(days=30)

            recent_articles = [
                entry for entry in feed.entries
                if "published_parsed" in entry
                and datetime(*entry.published_parsed[:6]) > last_30_days
            ]

            count = len(recent_articles)

            # Normalize: 0–1
            return min(count / 20, 1.0)

        except Exception:
            return 0.0
        
    

