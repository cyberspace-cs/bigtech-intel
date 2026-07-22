"""爬虫适配器基类。

设计原则（礼貌爬取）：
- 明确 User-Agent
- 超时控制
- 失败优雅降级（返回 None，不抛异常中断整体流程）
- 不绕过反爬、不登录、只抓公开页面
"""
from __future__ import annotations

import abc
from dataclasses import dataclass

UA = "BigTechIntelBot/0.1 (+job-research; respectful crawler)"


@dataclass
class CrawlResult:
    source: str
    title: str
    url: str
    summary: str
    raw_text: str = ""


class BaseCrawler(abc.ABC):
    name: str = "base"

    @abc.abstractmethod
    async def search(self, query: str) -> list[str]:
        """返回候选条目标题（用于自动定位）。"""

    @abc.abstractmethod
    async def fetch(self, identifier: str) -> CrawlResult | None:
        """根据标题/URL 抓取一条结构化结果；失败返回 None。"""
