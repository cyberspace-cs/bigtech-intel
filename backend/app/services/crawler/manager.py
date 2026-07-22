"""爬虫编排管理器：调度适配器、写入数据库、记录日志。"""
from __future__ import annotations

import asyncio

from sqlalchemy.orm import Session

from ...database import SessionLocal
from ...models import Company, CrawlFact, CrawlLog
from .base import CrawlResult
from .adapters.wikipedia import WikipediaCrawler
from .adapters.baidu_baike import BaiduBaikeCrawler
from .adapters.official_site import OfficialSiteCrawler

CRAWLERS = {
    "wikipedia": WikipediaCrawler,
    "baidu_baike": BaiduBaikeCrawler,
    "official": OfficialSiteCrawler,
}


def get_crawler(name: str):
    cls = CRAWLERS.get(name)
    return cls() if cls else None


def _log(db: Session, trigger: str, target: str, adapter: str, status: str, message: str) -> CrawlLog:
    log = CrawlLog(trigger=trigger, target=target, adapter=adapter, status=status, message=message)
    db.add(log)
    db.flush()
    return log


def _choose_candidate(candidates: list[str], query: str) -> str:
    """从搜索候选里挑最贴合的词条：先精确（去括号），再包含，否则取首位。"""
    if not candidates:
        return query
    q = query.replace(" ", "").lower()
    for c in candidates:
        t = c.split("(")[0].strip().replace(" ", "").lower()
        if t == q:
            return c
    for c in candidates:
        if q in c.replace(" ", "").lower():
            return c
    return candidates[0]


async def run_adapter(name: str, query: str) -> CrawlResult | None:
    crawler = get_crawler(name)
    if not crawler:
        return None
    try:
        candidates = await crawler.search(query)
        identifier = _choose_candidate(candidates, query)
        return await crawler.fetch(identifier)
    except Exception:
        return None


async def crawl_query(
    query: str,
    adapter: str = "wikipedia",
    company_id: str | None = None,
    link_to_company: bool = True,
    trigger: str = "manual",
    db: Session | None = None,
) -> list[dict]:
    """返回抓取结果日志（纯字典，避免 ORM detached 问题）。"""
    own = db is None
    if own:
        db = SessionLocal()
    results: list[dict] = []
    try:
        targets = ["wikipedia", "baidu_baike"] if adapter == "all" else [adapter]
        company = db.query(Company).filter(Company.id == company_id).first() if company_id else None

        for name in targets:
            if name == "official" and not query.startswith("http"):
                continue
            res = await run_adapter(name, query)
            if res:
                db.add(
                    CrawlFact(
                        company_id=company.id if (company and link_to_company) else None,
                        source=res.source,
                        title=res.title,
                        url=res.url,
                        summary=res.summary,
                        raw_text=res.raw_text,
                        query=query,
                    )
                )
                log = _log(db, trigger, query, res.source, "success",
                           f"抓取到「{res.title}」（{res.source}），摘要 {len(res.summary)} 字。")
            else:
                log = _log(db, trigger, query, name, "failed", f"{name} 未抓取到有效内容。")
            results.append({
                "id": log.id,
                "trigger": log.trigger,
                "target": log.target,
                "adapter": log.adapter,
                "status": log.status,
                "message": log.message,
                "created_at": log.created_at,
            })
        db.commit()
    finally:
        if own:
            db.close()
    return results


async def refresh_all(db: Session | None = None):
    """遍历所有公司，用 Wikipedia 补充公开背景（持续完善信息）。"""
    own = db is None
    if own:
        db = SessionLocal()
    try:
        companies = db.query(Company).all()
        for c in companies:
            await crawl_query(
                query=c.name,
                adapter="wikipedia",
                company_id=c.id,
                link_to_company=True,
                trigger="refresh-all",
                db=db,
            )
            await asyncio.sleep(0.5)  # 礼貌限速
        _log(db, "refresh-all", "all", "wikipedia", "success",
             f"已对 {len(companies)} 家公司触发 Wikipedia 补充抓取。")
        db.commit()
    finally:
        if own:
            db.close()
