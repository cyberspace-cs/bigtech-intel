"""招聘入口速查表路由。"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import RecruitEntry
from ..schemas import RecruitEntryOut
from .. import seed_data as S

router = APIRouter(prefix="/api/recruit", tags=["recruit"])


@router.get("", response_model=list[RecruitEntryOut])
def get_recruit(tier: int = Query(0), db: Session = Depends(get_db)):
    q = db.query(RecruitEntry)
    if tier in (1, 2, 3):
        q = q.filter(RecruitEntry.tier == tier)
    rows = q.order_by(RecruitEntry.sort).all()
    if rows:
        return [
            RecruitEntryOut(tier=r.tier, company=r.company, direction=r.direction, url=r.url)
            for r in rows
        ]
    return [RecruitEntryOut(**r) for r in S.RECRUIT_TABLE]
