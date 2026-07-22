"""爬虫路由：手动触发 / 全量刷新 / 查看日志与抓取结果。"""
from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Company, CrawlFact, CrawlLog
from ..schemas import CrawlLogOut, CrawlFactOut, CrawlRequest, CrawlTriggerResult
from ..services.crawler.manager import crawl_query, refresh_all

router = APIRouter(prefix="/api/crawl", tags=["crawl"])


@router.post("/trigger", response_model=CrawlTriggerResult)
async def trigger_crawl(req: CrawlRequest, db: Session = Depends(get_db)):
    query = req.query
    if not query and req.company_id:
        c = db.query(Company).filter(Company.id == req.company_id).first()
        query = c.name if c else None
    if not query:
        return CrawlTriggerResult(triggered=0, logs=[])
    logs = await crawl_query(
        query=query,
        adapter=req.adapter or "wikipedia",
        company_id=req.company_id,
        link_to_company=req.link_to_company,
        trigger="manual",
        db=db,
    )
    out = [
        CrawlLogOut(
            id=l.get("id"), trigger=l.get("trigger"), target=l.get("target"),
            adapter=l.get("adapter"), status=l.get("status"), message=l.get("message"),
            created_at=l.get("created_at"),
        )
        for l in logs
    ]
    return CrawlTriggerResult(triggered=len(out), logs=out)


@router.post("/refresh-all")
async def refresh_all_companies(background: BackgroundTasks):
    background.add_task(refresh_all)
    return {"accepted": True, "message": "已在后台对全部公司触发 Wikipedia 补充抓取。"}


@router.get("/logs", response_model=list[CrawlLogOut])
def get_logs(limit: int = Query(50, le=200), db: Session = Depends(get_db)):
    rows = db.query(CrawlLog).order_by(CrawlLog.id.desc()).limit(limit).all()
    return [
        CrawlLogOut(
            id=r.id, trigger=r.trigger, target=r.target, adapter=r.adapter,
            status=r.status, message=r.message, created_at=r.created_at,
        )
        for r in rows
    ]


@router.get("/facts", response_model=list[CrawlFactOut])
def get_facts(company_id: str = Query(None), limit: int = Query(50, le=200), db: Session = Depends(get_db)):
    q = db.query(CrawlFact)
    if company_id:
        q = q.filter(CrawlFact.company_id == company_id)
    rows = q.order_by(CrawlFact.id.desc()).limit(limit).all()
    return [
        CrawlFactOut(
            id=f.id, company_id=f.company_id, source=f.source, title=f.title,
            url=f.url, summary=f.summary, query=f.query, created_at=f.created_at,
        )
        for f in rows
    ]
