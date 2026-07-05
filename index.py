"""
Keyword se image/video links fetch karne ka script (no API key needed).
Uses DuckDuckGo search internally.

Install (agar nahi kiya hai):
    pip install ddgs --break-system-packages

Note: Ye scraping-based approach hai, official API nahi. Zyada fast/bulk
requests bhejne par rate-limit (403) aa sakta hai. Isliye:
  - Har request ke beech 1-2 second ka gap rakho (time.sleep)
  - Bahut zyada keywords ek sath mat chalao
  - Production/scale ke liye NewsAPI/Pexels jaisi official API zyada stable hai
"""

import utils.session
import time
from ddgs import DDGS


def get_image_links(keyword: str, max_results: int = 10) -> list[str]:
    """Keyword ke basis par image URLs ki list deta hai."""
    urls = []
    with DDGS() as ddgs:
        results = ddgs.images(keyword, max_results=max_results)
        for r in results:
            url = r.get("image")
            if url:
                urls.append(url)
    return urls


def get_video_links(keyword: str, max_results: int = 10) -> list[str]:
    """Keyword ke basis par video page URLs ki list deta hai (YouTube etc.)."""
    urls = []
    with DDGS() as ddgs:
        results = ddgs.videos(keyword, max_results=max_results)
        for r in results:
            url = r.get("content") or r.get("embed_url")
            if url:
                urls.append(url)
    return urls


def get_news_links(keyword: str, max_results: int = 10) -> list[dict]:
    """Keyword ke basis par news articles (title + url + image) deta hai."""
    items = []
    with DDGS() as ddgs:
        results = ddgs.news(keyword, max_results=max_results)
        for r in results:
            items.append({
                "title": r.get("title"),
                "url": r.get("url"),
                "image": r.get("image"),
                "date": r.get("date"),
            })
    return items


if __name__ == "__main__":
    keyword = "nitish kumar"  # <-- apna keyword yaha daalo

    print("== Images ==")
    for link in get_image_links(keyword, max_results=5):
        print(link)

    time.sleep(1.5)  # rate-limit se bachne ke liye gap

    print("\n== News (title + image) ==")
    for item in get_news_links(keyword, max_results=5):
        print(item["title"], "->", item["image"])