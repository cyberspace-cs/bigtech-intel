"""百度百科适配器（尽力而为）：按词条名抓取摘要段落。
注意：百度百科有反爬，可能返回验证页或限流；失败即优雅降级。"""
from __future__ import annotations

from bs4 import BeautifulSoup

from ..base import BaseCrawler, CrawlResult
from ..httpclient import fetch

BASE = "https://baike.baidu.com/item/"


class BaiduBaikeCrawler(BaseCrawler):
    name = "baidu_baike"

    async def search(self, query: str) -> list[str]:
        return [query]

    async def fetch(self, identifier: str) -> CrawlResult | None:
        try:
            url = BASE + identifier
            html = await fetch(url)
            if not html:
                return None
            soup = BeautifulSoup(html, "lxml")
            summary_el = soup.select_one(".lemma-summary") or soup.select_one(".summary")
            if summary_el:
                text = summary_el.get_text(" ", strip=True)
            else:
                p = soup.select_one("div.para") or soup.select_one("p")
                text = p.get_text(" ", strip=True) if p else ""
            if not text or len(text) < 20:
                return None
            title = soup.select_one("h1") or soup.select_one(".lemma-title")
            title = title.get_text(strip=True) if title else identifier
            return CrawlResult(
                source="baidu_baike",
                title=title,
                url=url,
                summary=text[:600],
                raw_text=text,
            )
        except Exception:
            return None
