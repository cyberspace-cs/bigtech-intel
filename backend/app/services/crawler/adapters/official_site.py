"""官方站点轻量适配器：抓取 <title> 与 meta description / 首段，用于补充官网动态。"""
from __future__ import annotations

from bs4 import BeautifulSoup

from ..base import BaseCrawler, CrawlResult
from ..httpclient import fetch


class OfficialSiteCrawler(BaseCrawler):
    name = "official"

    async def search(self, query: str) -> list[str]:
        return [query]

    async def fetch(self, identifier: str) -> CrawlResult | None:
        if not identifier.startswith("http"):
            return None
        try:
            html = await fetch(identifier)
            if not html:
                return None
            soup = BeautifulSoup(html, "lxml")
            title = soup.title.get_text(strip=True) if soup.title else identifier
            desc = soup.select_one('meta[name="description"]')
            summary = desc.get("content", "").strip() if desc else ""
            if not summary:
                p = soup.select_one("p")
                summary = p.get_text(" ", strip=True)[:400] if p else ""
            if not summary:
                return None
            return CrawlResult(
                source="official",
                title=title,
                url=identifier,
                summary=summary,
                raw_text=summary,
            )
        except Exception:
            return None
