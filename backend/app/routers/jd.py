"""招聘情报 API：列表 / 解析预览 / 入库 / 删除。"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import RecruitIntel
from ..schemas import RecruitIntelCreate, RecruitIntelOut
from ..jd_parse import parse_jd

router = APIRouter(prefix="/api/jd", tags=["jd"])

_OVERRIDE_KEYS = ("company", "title", "salary", "city", "jtype", "direction", "matched", "note", "raw")


def _apply_overrides(d: dict, payload: RecruitIntelCreate):
    for k in _OVERRIDE_KEYS:
        v = getattr(payload, k, None)
        if v is not None:
            d[k] = v
    if payload.url:
        d["url"] = payload.url
    return d


@router.get("", response_model=list[RecruitIntelOut])
def list_jd(
    tier: int = Query(0),
    jtype: int = Query(0),
    q: str = Query(""),
    db: Session = Depends(get_db),
):
    query = db.query(RecruitIntel)
    if tier in (1, 2, 3):
        query = query.filter(RecruitIntel.tier == tier)
    if jtype in (1, 2, 3, 4):
        query = query.filter(RecruitIntel.jtype == jtype)
    if q:
        like = f"%{q}%"
        query = query.filter(
            RecruitIntel.title.like(like)
            | RecruitIntel.company.like(like)
            | RecruitIntel.direction.like(like)
            | RecruitIntel.matched.like(like)
        )
    rows = query.order_by(RecruitIntel.id.desc()).all()
    return [RecruitIntelOut.model_validate(r) for r in rows]


@router.post("/parse", response_model=RecruitIntelOut)
def parse_only(payload: RecruitIntelCreate):
    """仅解析预览，不入库；前端确认后再 POST /api/jd。"""
    d = _apply_overrides(parse_jd(payload.text, payload.source), payload)
    return RecruitIntelOut(**d)


@router.post("", response_model=RecruitIntelOut)
def add_jd(payload: RecruitIntelCreate, db: Session = Depends(get_db)):
    d = _apply_overrides(parse_jd(payload.text, payload.source), payload)
    row = RecruitIntel(**d)
    db.add(row)
    db.commit()
    db.refresh(row)
    return RecruitIntelOut.model_validate(row)


@router.delete("/{jid}")
def delete_jd(jid: int, db: Session = Depends(get_db)):
    row = db.query(RecruitIntel).filter(RecruitIntel.id == jid).first()
    if row:
        db.delete(row)
        db.commit()
    return {"ok": True}
