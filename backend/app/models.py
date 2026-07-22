"""ORM 模型：公司画像、关键人物、团队背景图谱、简历策略、招聘入口、爬虫产物。"""
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(String(64), primary_key=True)
    name = Column(String(128), nullable=False, index=True)
    tier = Column(Integer, nullable=False, default=2)  # 1=第一梯队大厂 2=第二梯队独角兽 3=第三梯队中小厂
    priority = Column(String(64), default="")
    emoji = Column(String(8), default="")
    direction = Column(String(128), default="")
    featured = Column(Boolean, default=False)

    # JD 画像
    jd_positions = Column(Text, default="[]")  # JSON list
    jd_capability = Column(Text, default="")
    jd_hook = Column(Text, default="")
    intent = Column(String(256), default="")
    stack = Column(Text, default="[]")  # JSON list
    phase_focus = Column(String(256), default="")
    recruit_url = Column(String(512), default="")
    recruit_label = Column(String(128), default="")

    # 团队背景
    bg_summary = Column(Text, default="")
    bg_strategy = Column(Text, default="")
    bg_product = Column(Text, default="")
    bg_sources = Column(Text, default="[]")  # JSON list

    # 画像细化（近期进展 / 目前技术架构）
    recent_developments = Column(Text, default="[]")  # JSON list of {date,title,detail}
    tech_architecture = Column(Text, default="[]")  # JSON list of {name,desc}

    # 核心产品调研
    core_products = Column(Text, default="[]")  # JSON list of {name,desc}

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    key_people = relationship(
        "KeyPerson", back_populates="company", cascade="all, delete-orphan"
    )
    crawl_facts = relationship(
        "CrawlFact", back_populates="company", cascade="all, delete-orphan"
    )


class KeyPerson(Base):
    __tablename__ = "key_people"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(String(64), ForeignKey("companies.id"), nullable=False)
    name = Column(String(128), nullable=False)
    role = Column(String(256), default="")
    detail = Column(Text, default="")
    school = Column(String(128), default="")

    company = relationship("Company", back_populates="key_people")


class LineageMember(Base):
    __tablename__ = "lineage_members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    faction = Column(String(16), nullable=False, index=True)  # qinghua | beida
    name = Column(String(128), nullable=False)
    company = Column(String(128), default="")
    role = Column(String(256), default="")
    school = Column(String(128), default="")
    note = Column(Text, default="")
    sort = Column(Integer, default=0)


class ResumeTip(Base):
    __tablename__ = "resume_tips"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128), nullable=False)
    detail = Column(Text, default="")
    sort = Column(Integer, default=0)


class ResumeStrategy(Base):
    __tablename__ = "resume_strategy"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company = Column(String(128), nullable=False)
    intent = Column(String(256), default="")
    stack = Column(String(512), default="")
    phase = Column(String(256), default="")
    sort = Column(Integer, default=0)


class RecruitEntry(Base):
    __tablename__ = "recruit_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tier = Column(Integer, default=2)
    company = Column(String(128), nullable=False)
    direction = Column(String(256), default="")
    url = Column(String(512), default="")
    sort = Column(Integer, default=0)


class CrawlFact(Base):
    """爬虫抓取到的公开事实，可挂到具体公司或独立留存。"""

    __tablename__ = "crawl_facts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(String(64), ForeignKey("companies.id"), nullable=True)
    source = Column(String(64), default="")  # wikipedia / baidu_baike / official
    title = Column(String(256), default="")
    url = Column(String(512), default="")
    summary = Column(Text, default="")
    raw_text = Column(Text, default="")
    query = Column(String(256), default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="crawl_facts")


class CrawlLog(Base):
    __tablename__ = "crawl_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trigger = Column(String(64), default="")  # manual / seed
    target = Column(String(256), default="")
    adapter = Column(String(64), default="")
    status = Column(String(16), default="")  # success / failed / skipped
    message = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
