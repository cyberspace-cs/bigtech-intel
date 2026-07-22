"""Wikipedia（中文）适配器：使用官方 REST / Action API，公开、稳定、易解析。"""
from __future__ import annotations

from ..base import BaseCrawler, CrawlResult
from ..httpclient import fetch

API = "https://zh.wikipedia.org/w/api.php"
REST = "https://zh.wikipedia.org/api/rest_v1/page/summary"


class WikipediaCrawler(BaseCrawler):
    name = "wikipedia"

    # 显示名 -> 更可能命中的词条名
    ALIASES = {
        "字节Seed": "字节跳动",
        "智谱 GLM": "智谱",
        "腾讯混元": "腾讯混元",
        "Kimi / 月之暗面": "月之暗面",
        "百川智能": "百川智能",
        "阿里通义": "通义千问",
        "MiniMax": "MiniMax",
    }

    async def search(self, query: str) -> list[str]:
        try:
            q = self.ALIASES.get(query, query)
            # fetch 不替我们拼 query，这里直接拼 URL
            url = f"{API}?action=query&list=search&srsearch={q}&format=json&srlimit=5&utf8=1"
            data = await fetch(url, as_json=True)
            if not data:
                return []
            return [item["title"] for item in data.get("query", {}).get("search", [])]
        except Exception:
            return []

    async def fetch(self, identifier: str) -> CrawlResult | None:
        try:
            summary_url = REST + "/" + identifier
            summary = await fetch(summary_url, as_json=True)
            if not summary:
                return None
            title = summary.get("title", identifier)
            extract = summary.get("extract", "")
            page_url = summary.get("content_urls", {}).get("desktop", {}).get("page", "")

            ext_url = (
                f"{API}?action=query&prop=extracts&exintro=1&explaintext=1"
                f"&titles={identifier}&format=json&utf8=1"
            )
            raw = ""
            data2 = await fetch(ext_url, as_json=True)
            if data2:
                pages = data2.get("query", {}).get("pages", {})
                for pid, p in pages.items():
                    raw = p.get("extract", "")
                    break

            if not extract and not raw:
                return None
            return CrawlResult(
                source="wikipedia",
                title=title,
                url=page_url,
                summary=extract,
                raw_text=raw or extract,
            )
        except Exception:
            return None
