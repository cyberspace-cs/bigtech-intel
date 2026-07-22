"""公司画像路由：搜索 / 筛选 / 详情。"""
import json

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Company, KeyPerson, CrawlFact
from ..schemas import CompanyOut, CrawlFactOut

router = APIRouter(prefix="/api/companies", tags=["companies"])


def _parse_list(s: str):
    try:
        return json.loads(s) if s else []
    except Exception:
        return []


def _parse_objs(s: str):
    try:
        v = json.loads(s) if s else []
        return v if isinstance(v, list) else []
    except Exception:
        return []


def _to_out(c: Company) -> CompanyOut:
    people = (
        c.key_people
        if c.key_people
        else []
    )
    facts = [
        CrawlFactOut(
            id=f.id,
            company_id=f.company_id,
            source=f.source,
            title=f.title,
            url=f.url,
            summary=f.summary,
            query=f.query,
            created_at=f.created_at,
        )
        for f in c.crawl_facts
    ]
    return CompanyOut(
        id=c.id,
        name=c.name,
        tier=c.tier,
        priority=c.priority,
        emoji=c.emoji,
        direction=c.direction,
        featured=c.featured,
        jd_positions=_parse_list(c.jd_positions),
        jd_capability=c.jd_capability,
        jd_hook=c.jd_hook,
        intent=c.intent,
        stack=_parse_list(c.stack),
        phase_focus=c.phase_focus,
        recruit_url=c.recruit_url,
        recruit_label=c.recruit_label,
        bg_summary=c.bg_summary,
        bg_strategy=c.bg_strategy,
        bg_product=c.bg_product,
        bg_sources=_parse_list(c.bg_sources),
        recent_developments=_parse_objs(c.recent_developments),
        tech_architecture=_parse_objs(c.tech_architecture),
        key_people=[
            {"name": p.name, "role": p.role, "detail": p.detail, "school": p.school}
            for p in people
        ],
        crawl_facts=facts,
    )


@router.get("", response_model=list[CompanyOut])
def list_companies(
    q: str = Query("", description="搜索：公司名/方向/能力画像/关键人物/技术栈"),
    tier: int = Query(0, description="0=全部 1=第一梯队 2=第二梯队"),
    db: Session = Depends(get_db),
):
    query = db.query(Company)
    if tier in (1, 2):
        query = query.filter(Company.tier == tier)

    companies = query.all()

    if q.strip():
        needle = q.lower()
        scored = []
        for c in companies:
            blob = " ".join(
                [
                    c.name,
                    c.direction,
                    c.jd_capability,
                    c.jd_hook,
                    c.intent,
                    c.priority,
                    " ".join(_parse_list(c.stack)),
                    " ".join(_parse_list(c.jd_positions)),
                    c.bg_summary,
                    " ".join(str(x) for x in _parse_objs(c.recent_developments)),
                    " ".join(str(x) for x in _parse_objs(c.tech_architecture)),
                    " ".join(p.name + " " + p.detail + " " + p.school for p in c.key_people),
                ]
            ).lower()
            if needle in blob:
                scored.append(c)
        companies = scored

    companies.sort(key=lambda x: (x.tier, not x.featured, x.name))
    return [_to_out(c) for c in companies]


@router.get("/{company_id}", response_model=CompanyOut)
def get_company(company_id: str, db: Session = Depends(get_db)):
    c = db.query(Company).filter(Company.id == company_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="公司不存在")
    return _to_out(c)
