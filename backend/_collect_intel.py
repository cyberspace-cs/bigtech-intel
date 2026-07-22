"""批量入库：20 家跟踪厂的 社招(2)/实习(3)/校招(4) 招聘情报。

数据来源：公开渠道（官网 careers / 牛客 / 校招宣讲 / 实习僧 / 猎聘 / 飞书招聘）
的 WebSearch 采集结果（2026-07-22）。BOSS 直聘因登录墙无法自动抓取，
故官方/聚合源以可访问的 URL 为准，并在 note 中标注投递入口。

去重：按 (url) 或 (company+title+city) 去重，脚本可重复执行而不产生重复。
"""
import sys
from datetime import date

sys.path.insert(0, ".")

from app.database import SessionLocal
from app.models import RecruitIntel

DATE = date.today().strftime("%Y-%m-%d")

# jtype: 2=社招 3=实习 4=校招
COLLECTED = [
    # ===================== TIER 1 =====================
    # 腾讯混元
    dict(tier=1, company="腾讯混元", title="混元 青云计划 校招（大模型/Agent方向）", city="北京",
         jtype=4, direction="大模型 Agent 应用开发",
         source="腾讯校招官网", url="https://join.qq.com",
         note="混元大模型青云计划校招，覆盖北京/上海/深圳，含 Agent 应用算法与工程岗。"),
    dict(tier=1, company="腾讯混元", title="混元 青云计划 实习（大模型/Agent方向）", city="上海",
         jtype=3, direction="大模型 Agent 应用开发",
         source="腾讯校招官网", url="https://join.qq.com",
         note="混元青云计划日常/暑期实习，Agent 应用开发方向，可留用。"),
    dict(tier=1, company="腾讯混元", title="混元 Agent 算法/工程 社招", city="深圳",
         jtype=2, direction="大模型 Agent 应用开发",
         source="腾讯招聘", url="https://careers.tencent.com",
         note="混元大模型社招，Agent 应用算法与工程岗，深圳为主。"),

    # 字节 Seed
    dict(tier=1, company="字节Seed", title="Seed 校招（早期职业计划）", city="北京",
         jtype=4, direction="大模型 Agent 应用开发",
         source="字节 Seed 官网", url="https://seed.bytedance.com/zh/seedearlycareer",
         note="ByteDance Seed 早期职业计划，校招覆盖北京/上海/新加坡。"),
    dict(tier=1, company="字节Seed", title="Seed 实习（大模型/Agent）", city="上海",
         jtype=3, direction="大模型 Agent 应用开发",
         source="字节 Seed 官网", url="https://seed.bytedance.com/zh/seedearlycareer",
         note="Seed 团队日常/暑期实习，大模型与 Agent 方向，可转正。"),
    dict(tier=1, company="字节Seed", title="AI 搜索 Agent 算法工程师（校招）", city="上海",
         jtype=4, direction="大模型 Agent 应用开发",
         source="字节校招", url="https://jobs.bytedance.com/campus",
         note="AI 搜索 Agent 算法工程师校招岗，上海，Agent 应用核心方向。"),

    # 阿里通义
    dict(tier=1, company="阿里通义", title="AI 产品经理-超级智能体（阿里 2027 实习）", city="杭州",
         jtype=3, direction="大模型 Agent 应用开发",
         source="牛客", url="https://www.nowcoder.com",
         note="阿里 2027 届实习，超级智能体方向 AI 产品经理，广州/杭州/北京可投。"),
    dict(tier=1, company="阿里通义", title="千问 Qwen 基础大模型（阿里星 2027 实习）", city="北京",
         jtype=3, direction="大模型应用",
         source="牛客", url="https://www.nowcoder.com",
         note="阿里星计划 2027 实习，Qwen 基础大模型方向，上海/杭州/北京。"),
    dict(tier=1, company="阿里通义", title="阿里云 2027 实习（大模型/Agent）", city="深圳",
         jtype=3, direction="大模型应用",
         source="阿里招聘", url="https://talent.alibaba.com",
         note="阿里云 2027 实习，覆盖杭州/北京/上海/深圳等，含大模型与 Agent 岗。"),

    # 百度
    dict(tier=1, company="百度", title="2027 AIDU 智能体算法工程师（校招）", city="北京",
         jtype=4, direction="大模型应用",
         source="百度招聘", url="https://talent.baidu.com",
         note="百度 AIDU 校招，智能体算法工程师，北京。"),
    dict(tier=1, company="百度", title="2027 AIDU Agent 应用全栈工程师（校招）", city="北京",
         jtype=4, direction="大模型 Agent 应用开发",
         source="百度招聘", url="https://talent.baidu.com",
         note="百度 AIDU 校招，Agent 应用全栈工程师，北京。"),
    dict(tier=1, company="百度", title="大模型算法工程师 实习", city="北京",
         jtype=3, direction="大模型应用",
         source="百度招聘", url="https://talent.baidu.com",
         note="百度大模型算法工程师日常/暑期实习，北京。"),

    # 京东
    dict(tier=1, company="京东", title="京东 JDYOUNG 大模型算法工程师 实习", city="北京",
         jtype=3, direction="AI Agent 产品经理",
         source="京东校招", url="https://campus.jd.com",
         note="京东 JDYOUNG 实习计划，万名可留用，大模型算法工程师实习-北京。"),
    dict(tier=1, company="京东", title="言犀 大模型算法工程师 实习", city="北京",
         jtype=3, direction="大模型 Agent 应用开发",
         source="京东校招", url="https://campus.jd.com",
         note="京东言犀大模型团队日常实习，北京，偏 Agent 应用。"),
    dict(tier=1, company="京东", title="后端开发-京东言犀智能体平台（社招）", city="北京",
         jtype=2, direction="大模型 Agent 应用开发",
         source="京东招聘", url="https://campus.jd.com",
         note="京东言犀智能体平台后端社招，北京，Agent 平台工程。"),

    # 快手
    dict(tier=1, company="快手", title="日常实习 Agent 研发工程师", city="杭州",
         jtype=3, direction="大模型 Agent 研发",
         source="快手招聘", url="https://zhaopin.kuaishou.cn",
         note="快手日常实习，Agent 研发工程师，杭州。"),
    dict(tier=1, company="快手", title="快 Star-X 实习（大模型/Agent）", city="北京",
         jtype=3, direction="大模型 Agent 研发",
         source="快手招聘", url="https://zhaopin.kuaishou.cn",
         note="快手快 Star-X 实习生计划，大模型/Agent 方向。"),
    dict(tier=1, company="快手", title="留用实习 大模型 AI Agent 开发工程师", city="杭州",
         jtype=3, direction="大模型 Agent 研发",
         source="快手招聘", url="https://zhaopin.kuaishou.cn",
         note="快手留用实习，大模型 AI Agent 开发工程师，杭州。"),

    # 美团
    dict(tier=1, company="美团", title="大模型应用 实习生", city="北京",
         jtype=3, direction="本地生活 Agent",
         source="美团招聘", url="https://zhaopin.meituan.com",
         note="美团大模型应用实习生，北京，本地生活 Agent 方向。"),
    dict(tier=1, company="美团", title="LongCat 大模型人才 校招提前批", city="成都",
         jtype=4, direction="本地生活 Agent",
         source="美团招聘", url="https://zhaopin.meituan.com",
         note="美团 LongCat 大模型人才校招提前批，北京/上海/深圳/成都/杭州。"),
    dict(tier=1, company="美团", title="LongCat 北斗计划 社招", city="北京",
         jtype=2, direction="本地生活 Agent",
         source="美团招聘", url="https://zhaopin.meituan.com",
         note="美团 LongCat 北斗计划社招，大模型/Agent 核心岗。"),

    # ===================== TIER 2 =====================
    # 智谱 GLM
    dict(tier=2, company="智谱GLM", title="校招 后训练/Agent/推理 Infra", city="北京",
         jtype=4, direction="Agent / MultiAgent / 模型训练",
         source="智谱招聘(飞书)", url="https://zhipu-ai.jobs.feishu.cn",
         note="智谱 GLM 校招，后训练/Agent/推理 Infra 方向，北京。"),
    dict(tier=2, company="智谱GLM", title="27 届 后训练算法工程师 实习", city="北京",
         jtype=3, direction="Agent / MultiAgent / 模型训练",
         source="实习僧/wondercv", url="https://www.wondercv.com",
         note="智谱 27 届日常实习，后训练算法工程师，北京。"),
    dict(tier=2, company="智谱GLM", title="2027 实习（大模型/Agent）", city="北京",
         jtype=3, direction="Agent / MultiAgent / 模型训练",
         source="智谱招聘(飞书)", url="https://zhipu-ai.jobs.feishu.cn",
         note="智谱 2027 实习计划，大模型与 Agent 方向。"),

    # Kimi / 月之暗面
    dict(tier=2, company="Kimi / 月之暗面", title="Kimi 穿越计划 校招", city="新加坡",
         jtype=4, direction="推理框架 / Agentic",
         source="月之暗面招聘", url="https://careers.kimi.com",
         note="月之暗面穿越计划校招（16 人精英计划），北京/上海/深圳/新加坡。"),
    dict(tier=2, company="Kimi / 月之暗面", title="26 届 秋招（大模型/Agentic）", city="北京",
         jtype=4, direction="推理框架 / Agentic",
         source="月之暗面招聘", url="https://careers.kimi.com",
         note="月之暗面 26 届秋招，北京/上海/深圳/新加坡/美国湾区。"),

    # DeepSeek
    dict(tier=2, company="DeepSeek", title="大模型算法工程师 社招", city="杭州",
         jtype=2, direction="应用开发 / 全栈 / AI 产品",
         source="DeepSeek 官网", url="https://www.deepseek.com",
         note="DeepSeek 社招，大模型算法工程师，北京/杭州/乌兰察布。"),
    dict(tier=2, company="DeepSeek", title="Agent Harness 团队 实习", city="北京",
         jtype=3, direction="应用开发 / 全栈 / AI 产品",
         source="DeepSeek 官网", url="https://www.deepseek.com",
         note="DeepSeek Agent Harness 团队实习（研究员/工程师/产品经理），北京/杭州。"),
    dict(tier=2, company="DeepSeek", title="研究员/工程师 扩招（全岗）", city="杭州",
         jtype=2, direction="应用开发 / 全栈 / AI 产品",
         source="DeepSeek 官网", url="https://www.deepseek.com",
         note="DeepSeek 2026-06 最大规模扩招，7 类 33 岗，全面接收实习。"),

    # MiniMax
    dict(tier=2, company="MiniMax", title="校招（对话/Agent）", city="上海",
         jtype=4, direction="对话 / Agent",
         source="MiniMax 招聘", url="https://www.minimax.io",
         note="MiniMax 校招，上海/北京/硅谷，对话与 Agent 方向。"),
    dict(tier=2, company="MiniMax", title="服务端研发实习生-AI Agent 方向", city="上海",
         jtype=3, direction="对话 / Agent",
         source="MiniMax 招聘", url="https://www.minimax.io",
         note="MiniMax 服务端研发实习，AI Agent 方向，上海。"),
    dict(tier=2, company="MiniMax", title="大模型算法实习生", city="北京",
         jtype=3, direction="对话 / Agent",
         source="MiniMax 招聘", url="https://www.minimax.io",
         note="MiniMax 大模型算法实习，北京。"),

    # 百川智能
    dict(tier=2, company="百川智能", title="数据策略产品经理 实习生", city="北京",
         jtype=3, direction="行业模型",
         source="牛客", url="https://www.nowcoder.com",
         note="百川智能数据策略产品经理实习，北京。"),
    dict(tier=2, company="百川智能", title="大模型算法工程师 实习", city="北京",
         jtype=3, direction="行业模型",
         source="百川智能招聘", url="https://www.baichuan-ai.com",
         note="百川智能大模型算法工程师实习，北京。"),
    dict(tier=2, company="百川智能", title="大模型算法工程师 社招", city="北京",
         jtype=2, direction="行业模型",
         source="百川智能招聘", url="https://www.baichuan-ai.com",
         note="百川智能大模型算法工程师社招，北京。"),

    # 商汤
    dict(tier=2, company="商汤", title="多模态大模型算法实习生-GUI Agent", city="北京",
         jtype=3, direction="多模态",
         source="商汤招聘", url="https://hr.sensetime.com",
         note="商汤多模态大模型算法实习，GUI Agent 方向，北京。"),
    dict(tier=2, company="商汤", title="2026 校招 通用智能体研究员/Agent Harness", city="深圳",
         jtype=4, direction="多模态",
         source="商汤招聘", url="https://hr.sensetime.com",
         note="商汤 2026 校招，通用智能体研究员/Agent Harness，北京/上海/深圳/香港。"),
    dict(tier=2, company="商汤", title="AI 先锋 顶尖实习生", city="上海",
         jtype=3, direction="多模态",
         source="商汤招聘", url="https://hr.sensetime.com",
         note="商汤 AI 先锋顶尖实习生计划，多模态/智能体方向。"),

    # 阶跃星辰
    dict(tier=2, company="阶跃星辰", title="26 届 Agent RL 算法研究员（校招）", city="北京",
         jtype=4, direction="多模态 / Agent / 端侧",
         source="阶跃星辰官网", url="https://www.stepfun.com",
         note="阶跃星辰 26 届校招，Agent RL 算法研究员，北京。"),
    dict(tier=2, company="阶跃星辰", title="大模型算法工程师 实习", city="上海",
         jtype=3, direction="多模态 / Agent / 端侧",
         source="阶跃星辰官网", url="https://www.stepfun.com",
         note="阶跃星辰大模型算法工程师实习，上海。"),
    dict(tier=2, company="阶跃星辰", title="StepStar 计划 实习+校招", city="北京",
         jtype=3, direction="多模态 / Agent / 端侧",
         source="校招宣讲", url="https://career.buaa.edu.cn",
         note="阶跃星辰 StepStar 计划，北京/上海，实习+校招。"),

    # ===================== TIER 3 =====================
    # 宇树科技
    dict(tier=3, company="宇树科技", title="AI 算法工程师（大模型）社招", city="杭州",
         jtype=2, direction="具身 Agent 应用开发",
         source="宇树招聘", url="https://www.unitree.com/cn/position",
         note="宇树科技 AI 算法工程师（大模型）/深度强化学习，杭州。"),
    dict(tier=3, company="宇树科技", title="26 春招 算法岗（校招）", city="杭州",
         jtype=4, direction="具身 Agent 应用开发",
         source="宇树招聘", url="https://www.unitree.com/cn/position",
         note="宇树科技 26 春招，校招+社招，杭州。"),
    dict(tier=3, company="宇树科技", title="运动控制/视觉 SLAM 实习", city="上海",
         jtype=3, direction="具身 Agent 应用开发",
         source="宇树招聘", url="https://www.unitree.com/cn/position",
         note="宇树科技实习，运动控制/视觉 SLAM，杭州/上海。"),

    # 智元机器人
    dict(tier=3, company="智元机器人", title="2026 实习 具身智能基础模型/Agent 算法", city="深圳",
         jtype=3, direction="具身 Agent 应用开发",
         source="智元招聘", url="https://www.zhiyuan-robot.com/join_us",
         note="智元机器人 2026 实习，具身智能基础模型/Agent 算法，上海/深圳/北京。"),
    dict(tier=3, company="智元机器人", title="灵巧手模型算法 实习生", city="深圳",
         jtype=3, direction="具身 Agent 应用开发",
         source="智元招聘", url="https://www.zhiyuan-robot.com/join_us",
         note="智元机器人灵巧手模型算法实习，深圳。"),
    dict(tier=3, company="智元机器人", title="校招 具身智能算法", city="上海",
         jtype=4, direction="具身 Agent 应用开发",
         source="智元招聘", url="https://www.zhiyuan-robot.com/join_us",
         note="智元机器人校招，具身智能算法，上海。"),

    # 银河通用
    dict(tier=3, company="银河通用", title="具身领航者计划 校招", city="苏州",
         jtype=4, direction="具身 Agent 应用开发",
         source="银河通用招聘", url="https://www.galbot.com",
         note="银河通用具身领航者计划校招，北京/深圳/苏州。"),
    dict(tier=3, company="银河通用", title="2026 届实习 具身 VLA/感知/控制算法", city="北京",
         jtype=3, direction="具身 Agent 应用开发",
         source="银河通用招聘", url="https://www.galbot.com",
         note="银河通用 2026 届实习，具身 VLA/感知/控制算法，北京/深圳。"),

    # 星海图
    dict(tier=3, company="星海图", title="日常实习 27 届 VLA/具身智能算法", city="苏州",
         jtype=3, direction="具身",
         source="实习僧/wondercv", url="https://www.wondercv.com",
         note="星海图 27 届日常实习，VLA/具身智能算法，北京/深圳/苏州。"),
    dict(tier=3, company="星海图", title="深度学习/具身智能预训练 社招", city="北京",
         salary="35-65K", jtype=2, direction="具身",
         source="星海图招聘", url="https://www.wondercv.com",
         note="星海图社招，深度学习/具身智能预训练，北京，35-65K。"),

    # 星动纪元
    dict(tier=3, company="星动纪元", title="星航计划 26 届 校招", city="北京",
         jtype=4, direction="具身",
         source="星动纪元招聘", url="https://www.robotera.com",
         note="星动纪元星航计划 26 届校招，北京。"),
    dict(tier=3, company="星动纪元", title="具身大模型/MPC/运动控制算法 社招", city="北京",
         salary="35-65K", jtype=2, direction="具身",
         source="星动纪元招聘", url="https://www.robotera.com",
         note="星动纪元社招，具身大模型/MPC/运动控制算法，北京，35-65K。"),

    # 灵初智能
    dict(tier=3, company="灵初智能", title="多模态大模型算法工程师 校招", city="北京",
         salary="40-50K", jtype=4, direction="具身 Agent 应用开发",
         source="灵初招聘", url="https://www.psibot.ai/careers_zh",
         note="灵初智能多模态大模型算法工程师校招，北京，40-50K。"),
    dict(tier=3, company="灵初智能", title="机器人开发工程师(ROS)/视觉算法 校招", city="北京",
         jtype=4, direction="具身 Agent 应用开发",
         source="灵初招聘", url="https://www.psibot.ai/careers_zh",
         note="灵初智能机器人开发工程师(ROS)/视觉算法校招，北京。"),
    dict(tier=3, company="灵初智能", title="训练平台研发/机器人测试 社招", city="北京",
         jtype=2, direction="具身 Agent 应用开发",
         source="灵初招聘", url="https://www.psibot.ai/careers_zh",
         note="灵初智能社招，训练平台研发/机器人测试，北京。"),
]


def dedup_key(r):
    # 同一公司+同一岗位标题即视为重复（官方 careers 页面常多个岗位共用一个 URL，
    # 不能拿 url 当唯一键，否则会误杀同公司不同岗位）。
    return ("C", r["company"], r["title"])


def main():
    db = SessionLocal()
    existing = {dedup_key({
        "url": row.url, "company": row.company, "title": row.title, "city": row.city
    }) for row in db.query(RecruitIntel).all()}

    added = 0
    skipped = 0
    for item in COLLECTED:
        k = dedup_key(item)
        if k in existing:
            skipped += 1
            continue
        row = RecruitIntel(
            tier=item["tier"],
            company=item["company"],
            title=item["title"],
            salary=item.get("salary", ""),
            city=item["city"],
            exp=item.get("exp", ""),
            edu=item.get("edu", ""),
            jtype=item["jtype"],
            direction=item["direction"],
            source=item["source"],
            url=item.get("url", ""),
            matched=item["company"],  # 直接归属到跟踪厂
            note=item.get("note", ""),
            raw=item.get("note", ""),
            date=DATE,
        )
        db.add(row)
        existing.add(k)
        added += 1

    db.commit()
    total = db.query(RecruitIntel).count()
    db.close()
    print(f"新增 {added} 条，跳过重复 {skipped} 条，当前情报总数 {total}。")


if __name__ == "__main__":
    main()
