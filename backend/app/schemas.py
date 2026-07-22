"""Pydantic 响应/请求模型。"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class KeyPersonOut(BaseModel):
    name: str
    role: str = ""
    detail: str = ""
    school: str = ""


class CrawlFactOut(BaseModel):
    id: int
    company_id: Optional[str] = None
    source: str = ""
    title: str = ""
    url: str = ""
    summary: str = ""
    query: str = ""
    created_at: Optional[datetime] = None


class CompanyOut(BaseModel):
    id: str
    name: str
    tier: int
    priority: str = ""
    emoji: str = ""
    direction: str = ""
    featured: bool = False
    jd_positions: List[str] = []
    jd_capability: str = ""
    jd_hook: str = ""
    intent: str = ""
    stack: List[str] = []
    phase_focus: str = ""
    recruit_url: str = ""
    recruit_label: str = ""
    bg_summary: str = ""
    bg_strategy: str = ""
    bg_product: str = ""
    bg_sources: List[str] = []
    recent_developments: List[dict] = []
    tech_architecture: List[dict] = []
    key_people: List[KeyPersonOut] = []
    crawl_facts: List[CrawlFactOut] = []

    class Config:
        from_attributes = True


class LineageMemberOut(BaseModel):
    name: str
    company: str = ""
    role: str = ""
    school: str = ""
    note: str = ""


class LineageOut(BaseModel):
    title: str
    desc: str
    members: List[LineageMemberOut]


class ResumeTipOut(BaseModel):
    title: str
    detail: str


class ResumeStrategyOut(BaseModel):
    company: str
    intent: str
    stack: str
    phase: str


class RecruitEntryOut(BaseModel):
    tier: int
    company: str
    direction: str
    url: str


class CrawlLogOut(BaseModel):
    id: int
    trigger: str = ""
    target: str = ""
    adapter: str = ""
    status: str = ""
    message: str = ""
    created_at: Optional[datetime] = None


class CrawlRequest(BaseModel):
    query: Optional[str] = None
    company_id: Optional[str] = None
    adapter: Optional[str] = "wikipedia"  # wikipedia | baidu_baike | official | all
    link_to_company: bool = True


class CrawlTriggerResult(BaseModel):
    triggered: int
    logs: List[CrawlLogOut]
