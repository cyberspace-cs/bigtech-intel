"""团队背景图谱路由：清华系 / 北大系。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import LineageMember
from ..schemas import LineageOut, LineageMemberOut
from .. import seed_data as S

router = APIRouter(prefix="/api/lineage", tags=["lineage"])


@router.get("", response_model=dict)
def get_lineage(db: Session = Depends(get_db)):
    result = {}
    for faction, block in S.LINEAGE.items():
        members = (
            db.query(LineageMember)
            .filter(LineageMember.faction == faction)
            .order_by(LineageMember.sort)
            .all()
        )
        if not members:
            members = [LineageMemberOut(**m) for m in block["members"]]
        else:
            members = [LineageMemberOut(name=m.name, company=m.company, role=m.role, school=m.school, note=m.note) for m in members]
        result[faction] = LineageOut(
            title=block["title"], desc=block["desc"], members=members
        )
    return result
