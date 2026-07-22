"""JD 文本结构化解析：粘贴 BOSS / 官网 / 猎头代招的 JD 文本 → 结构化字段。

设计：纯正则 + 关键词命中，无外部依赖；解析结果可被前端预览覆盖后再入库。
"""
import re
from datetime import date

from . import seed_data as S

CITIES = [
    "北京", "上海", "深圳", "杭州", "广州", "成都", "南京", "武汉",
    "西安", "苏州", "合肥", "天津", "重庆", "长沙", "厦门", "青岛",
    "宁波", "东莞", "佛山", "珠海",
]
EDU_MAP = ["博士", "硕士", "本科", "大专"]
PHASE_HINTS = {
    "A": ["工具调用", "工具层", "工具网关", "function calling", "tool"],
    "B": ["记忆", "短期记忆", "长期记忆", "多轮"],
    "C": ["上下文", "检索", "rag", "压缩"],
    "D": ["多智能体", "多 agent", "编排", "规划-执行", "分层"],
    "E": ["评估", "评测", "任务成功率", "步骤准确率", "自动化评估"],
    "F": ["可观测", "tracing", "metrics", "推理延迟", "成本", "量化", "高并发"],
}
PHASE_DESC = {
    "A": "工具网关", "B": "记忆", "C": "上下文/RAG",
    "D": "多Agent编排", "E": "评测", "F": "可观测/推理优化",
}


def _today():
    return date.today().strftime("%Y-%m-%d")


def parse_jd(text, source="BOSS直聘"):
    t = text or ""
    low = t.lower()
    d = {
        "id": 0,
        "tier": 0,
        "company": "",
        "title": "",
        "salary": "",
        "city": "",
        "exp": "",
        "edu": "",
        "jtype": 1 if "急招" in t else 2,
        "direction": "大模型 Agent 应用开发",
        "source": source,
        "url": "",
        "matched": "",
        "note": "",
        "date": _today(),
    }

    # 薪资：40-70K·16薪
    m = re.search(r"(\d{1,3})\s*-\s*(\d{1,3})\s*K", t)
    if m:
        sal = f"{m.group(1)}-{m.group(2)}K"
        m2 = re.search(r"(\d+)\s*薪", t)
        if m2:
            sal += f"·{m2.group(1)}薪"
        d["salary"] = sal

    # 城市
    for c in CITIES:
        if c in t:
            d["city"] = c
            break

    # 经验
    me = re.search(r"(\d+)\s*-\s*(\d+)\s*年", t)
    if me:
        d["exp"] = f"{me.group(1)}-{me.group(2)}年"
    else:
        me2 = re.search(r"(\d+)\s*年(以上|以内|内)?", t)
        if me2:
            d["exp"] = me2.group(0).strip()

    # 学历
    for e in EDU_MAP:
        if e in t:
            d["edu"] = e
            break

    # 公司（代招公司 / 公司名称 / 公司：）
    mc = re.search(r"(?:代招公司|公司名称|公司)\s*[:：]\s*([^\n，。]+)", t)
    if mc:
        comp = mc.group(1).strip()
        if "代招" in t:
            comp += "（代招/猎头）"
        d["company"] = comp

    # 标题：取首行并清理
    first = t.strip().splitlines()[0] if t.strip() else ""
    title = first.split("，")[0].split("（")[0].split("·")[0]
    title = title.replace("急招", "").replace("大厂", "").replace("-", "").strip("-")
    if "工程师" not in title and "开发" in title:
        title = title.replace("开发", "开发工程师")
    if title.startswith("Agent"):
        title = "Agent 开发工程师"
    d["title"] = title or "Agent 开发工程师"

    # 方向（Agent 优先，避免「推理延迟」等误判为推理优化）
    if any(k in t for k in ["具身", "机器人", "VLA", "Sim2Real", "具身智能"]):
        d["direction"] = "具身 Agent 应用开发"
    elif any(k in t for k in ["多模态", "视觉", "图像生成", "视频生成", "图像"]):
        d["direction"] = "多模态 / Agent"
    elif ("agent" in low) or ("智能体" in t) or ("多智能体" in t):
        d["direction"] = "大模型 Agent 应用开发"
    elif any(k in t for k in ["推理优化", "推理框架", "推理服务", "推理引擎", "vllm", "量化", "高并发", "continuous batching"]):
        d["direction"] = "大模型推理优化"
    elif any(k in low for k in ["rag", "检索", "搜索 agent"]):
        d["direction"] = "RAG / 搜索 Agent"
    else:
        d["direction"] = "大模型 Agent 应用开发"

    # 命中跟踪厂 + Phase 覆盖
    d["matched"] = _match_companies(t, d["direction"])
    cov = [p for p, kws in PHASE_HINTS.items() if any(k in low for k in kws)]
    if cov:
        d["note"] = (
            f"命中 Phase {'/'.join(cov)}（"
            + "/".join(PHASE_DESC.get(c, c) for c in cov)
            + "），与八周作品集路线高度对齐。"
        )
    return d


def _match_companies(text, direction):
    low = text.lower()
    pool = []
    for comp in S.TIER1 + S.TIER2 + S.TIER3:
        jd = comp.get("jd", {})
        blob = " ".join([
            comp.get("direction", ""),
            " ".join(jd.get("stack", [])),
            " ".join(p.get("name", "") for p in comp.get("products", [])),
            jd.get("hook", ""),
        ]).lower()
        pool.append((comp.get("name", ""), blob))

    def relevant(blob):
        if direction == "具身 Agent 应用开发":
            return any(k in blob for k in ["具身", "机器人", "vla"])
        if direction == "大模型推理优化":
            return any(k in blob for k in ["推理", "vllm", "量化", "高并发"])
        # Agent / RAG / 多模态 大类
        return any(k in blob for k in ["agent", "多智能体", "评测", "多模态", "具身", "harness"])

    hits = [name for name, blob in pool if relevant(blob)]
    # 去重保序
    seen, out = set(), []
    for h in hits:
        if h not in seen:
            seen.add(h)
            out.append(h)
    return "·".join(out[:8])
