"""把 seed_data 灌入数据库（首次运行 / 幂等更新）。

设计要点：
- 公司画像字段为「幂等 upsert」：已有行更新标量字段（含新增的
  recent_developments / tech_architecture），不删除已抓取的 crawl_facts、
  不重建 key_people，避免重复灌入。
- lineage / resume / recruit / crawl_log 仅在对应表为空时写入，防止重复。
- 对已有 companies 表做 ALTER 迁移，补齐新增列（SQLite 安全）。
"""
import json

from sqlalchemy import inspect, text

from .database import Base, SessionLocal, engine
from .models import (
    Company,
    CrawlLog,
    KeyPerson,
    LineageMember,
    RecruitEntry,
    RecruitIntel,
    ResumeStrategy,
    ResumeTip,
)
from . import seed_data as S


def _json(obj):
    return json.dumps(obj, ensure_ascii=False)


# 新增列定义：列名 -> 类型
_NEW_COLUMNS = {
    "recent_developments": "TEXT",
    "tech_architecture": "TEXT",
    "core_products": "TEXT",
}


def _migrate_columns(db):
    """已有 companies 表补齐新增列（SQLite 仅支持 ADD COLUMN）。"""
    cols = {c["name"] for c in inspect(db.bind).get_columns("companies")}
    for col, ddl in _NEW_COLUMNS.items():
        if col not in cols:
            db.execute(
                text(f"ALTER TABLE companies ADD COLUMN {col} {ddl} DEFAULT ''")
            )
    if _NEW_COLUMNS:
        db.commit()


def _migrate_recruit_intel(db):
    """recruit_intel 表补齐 raw 列（SQLite 仅支持 ADD COLUMN）。"""
    cols = {c["name"] for c in inspect(db.bind).get_columns("recruit_intel")}
    if "raw" not in cols:
        db.execute(text("ALTER TABLE recruit_intel ADD COLUMN raw TEXT DEFAULT ''"))
        db.commit()


def _apply_profile(c: Company, data: dict):
    """更新单个公司的标量画像字段（含新增字段）。"""
    jd = data.get("jd", {})
    bg = data.get("background", {})
    c.name = data.get("name", c.name)
    c.tier = data.get("tier", c.tier)
    c.priority = data.get("priority", c.priority)
    c.emoji = data.get("emoji", c.emoji)
    c.direction = data.get("direction", c.direction)
    c.featured = data.get("featured", c.featured)
    c.jd_positions = _json(jd.get("positions", []))
    c.jd_capability = jd.get("capability", "")
    c.jd_hook = jd.get("hook", "")
    c.intent = jd.get("intent", "")
    c.stack = _json(jd.get("stack", []))
    c.phase_focus = jd.get("phaseFocus", "")
    c.recruit_url = jd.get("recruit", {}).get("url", "")
    c.recruit_label = jd.get("recruit", {}).get("label", "")
    c.bg_summary = bg.get("summary", "")
    c.bg_strategy = bg.get("strategy", "")
    c.bg_product = bg.get("product", "")
    c.bg_sources = _json(bg.get("sources", []))
    c.recent_developments = _json(data.get("recent", []))
    c.tech_architecture = _json(data.get("tech", []))
    c.core_products = _json(data.get("products", []))


def _build_company(data: dict) -> Company:
    c = Company(id=data["id"])
    _apply_profile(c, data)
    for kp in data.get("background", {}).get("keyPeople", []):
        c.key_people.append(
            KeyPerson(
                name=kp.get("name", ""),
                role=kp.get("role", ""),
                detail=kp.get("detail", ""),
                school=kp.get("school", ""),
            )
        )
    return c


def seed(db=None):
    own = db is None
    if own:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()

    try:
        _migrate_columns(db)
        _migrate_recruit_intel(db)

        # —— 公司画像：幂等 upsert ——
        for data in S.TIER1 + S.TIER2 + S.TIER3:
            existing = db.query(Company).filter(Company.id == data["id"]).first()
            if existing:
                _apply_profile(existing, data)
            else:
                db.add(_build_company(data))

        # —— 其他表：仅空表时写入，防重复 ——
        if db.query(LineageMember).count() == 0:
            for faction, block in S.LINEAGE.items():
                for i, m in enumerate(block["members"]):
                    db.add(
                        LineageMember(
                            faction=faction,
                            name=m["name"],
                            company=m.get("company", ""),
                            role=m.get("role", ""),
                            school=m.get("school", ""),
                            note=m.get("note", ""),
                            sort=i,
                        )
                    )

        if db.query(ResumeTip).count() == 0:
            for i, t in enumerate(S.RESUME_TIPS):
                db.add(ResumeTip(title=t["t"], detail=t["d"], sort=i))

        if db.query(ResumeStrategy).count() == 0:
            for i, s in enumerate(S.RESUME_STRATEGY):
                db.add(
                    ResumeStrategy(
                        company=s["company"],
                        intent=s["intent"],
                        stack=s["stack"],
                        phase=s["phase"],
                        sort=i,
                    )
                )

        # recruit 表做 upsert：按 company 更新 tier/direction/url，保证梯队调整可回写
        for i, r in enumerate(S.RECRUIT_TABLE):
            existing = (
                db.query(RecruitEntry).filter(RecruitEntry.company == r["company"]).first()
            )
            if existing:
                existing.tier = r["tier"]
                existing.direction = r["direction"]
                existing.url = r["url"]
                existing.sort = i
            else:
                db.add(
                    RecruitEntry(
                        tier=r["tier"],
                        company=r["company"],
                        direction=r["direction"],
                        url=r["url"],
                        sort=i,
                    )
                )

        # 招聘情报：仅空表时写入种子（来自用户粘贴的 BOSS 急招 JD）
        if db.query(RecruitIntel).count() == 0:
            for r in S.RECRUIT_INTEL_SEED:
                db.add(RecruitIntel(**r))

        if db.query(CrawlLog).count() == 0:
            db.add(
                CrawlLog(
                    trigger="seed",
                    target="all",
                    adapter="seed",
                    status="success",
                    message=f"初始化种子数据：{len(S.TIER1)+len(S.TIER2)+len(S.TIER3)} 家公司 / 2 个派系图谱 / {len(S.RESUME_TIPS)} 条简历建议。",
                )
            )

        db.commit()
    finally:
        if own:
            db.close()


if __name__ == "__main__":
    seed()
    print("Seed 完成（幂等 upsert）。")
