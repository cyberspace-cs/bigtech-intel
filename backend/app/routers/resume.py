"""简历策略路由：6 条改动 + 分厂定制表。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ResumeTip, ResumeStrategy
from ..schemas import ResumeTipOut, ResumeStrategyOut
from .. import seed_data as S

router = APIRouter(prefix="/api/resume", tags=["resume"])


@router.get("/tips", response_model=list[ResumeTipOut])
def get_tips(db: Session = Depends(get_db)):
    rows = db.query(ResumeTip).order_by(ResumeTip.sort).all()
    if rows:
        return [ResumeTipOut(title=r.title, detail=r.detail) for r in rows]
    return [ResumeTipOut(title=t["t"], detail=t["d"]) for t in S.RESUME_TIPS]


@router.get("/strategy", response_model=list[ResumeStrategyOut])
def get_strategy(db: Session = Depends(get_db)):
    rows = db.query(ResumeStrategy).order_by(ResumeStrategy.sort).all()
    if rows:
        return [
            ResumeStrategyOut(company=r.company, intent=r.intent, stack=r.stack, phase=r.phase)
            for r in rows
        ]
    return [ResumeStrategyOut(**s) for s in S.RESUME_STRATEGY]
