/* =========================================================================
 * 大厂信息资源站 —— 数据层
 * 数据来源：公开报道 + 用户提供的 JD 画像（第一/第二梯队、简历策略、招聘入口）
 * 团队背景资料基于公开检索（截至 2026-07，含腾讯混元/智谱/月之暗面/DeepSeek/
 * 清华系/北大系），用于面试前的业务线摸底，非官方口径，投递以官网最新 JD 为准。
 * ========================================================================= */

const META = {
  title: "大厂情报站 · AI 大模型厂求职参谋",
  subtitle: "面向实习 / 校招 / 社招 · 产品设计 × 架构 × 战略方向 × JD 画像 × 团队背景",
  updated: "2026-07-22",
  note: "投递优先级与 JD 画像由用户原始策略整理；团队背景为公开资料摘编，面试前请以官方最新 JD 复核。",
};

/* ----------------------------- 第一梯队：五大模型厂 ----------------------------- */
const TIER1 = [
  {
    id: "tencent-hunyuan",
    name: "腾讯混元",
    tier: 1,
    priority: "第一梯队 · 先投",
    emoji: "🐧",
    direction: "Agent 应用开发 / 应用算法",
    featured: true,
    jd: {
      positions: ["混元大模型应用算法工程师", "混元 Agent 开发工程师"],
      capability:
        "Post-training 研发与应用；Agent 构建与强化、多轮对话；业务场景落地；AI PaaS；数据/环境平台。",
      hook:
        "突出 Phase C RAG 防幻觉（事实核查）+ Phase B 记忆/多轮 + Phase G 多厂商注册表（混元优先）+ 反思节点（Agent 强化同构）。",
      intent: "混元大模型 Agent 应用开发工程师",
      stack: ["混元", "RAG事实核查", "多轮记忆", "Agent强化", "Post-training"],
      phaseFocus: "C(防幻觉) → B(记忆多轮) → G(混元优先) → D(反思强化)",
      recruit: { url: "https://careers.tencent.com/", label: "腾讯招聘官网" },
    },
    background: {
      summary:
        "腾讯技术工程事业群（TEG）旗下的 AI 研发团队。2023.2 以“混元助手”名义组建，先后由张正友（AI Lab 主任）、蒋杰（TEG 副总裁）负责；2025.9 前 OpenAI 研究员姚顺雨入职，12 月升任首席 AI 科学家、统筹 AI Infra 部与大语言模型部，直接向总裁刘炽平汇报；2026.3 撤销 AI Lab，核心力量并入混元，由姚顺雨统一指挥。坚持全栈自研，已接入腾讯内部 700+ 业务场景并通过开源与 API 对外输出。",
      keyPeople: [
        {
          name: "姚顺雨 (Shunyu Yao)",
          role: "腾讯集团首席 AI 科学家 / AI Infra 部 & 大语言模型部负责人",
          detail:
            "1998 年生，安徽人。清华大学计算机科学实验班（姚班，2015 级，高考 704 分、安徽省理科第三）本科；普林斯顿大学计算机博士，师从 GPT-1 第二作者 Karthik Narasimhan。Agent 领域奠基性人物：提出 ReAct（推理-行动）、Tree of Thoughts（思维树）、Reflexion、SWE-agent、CoALA。2024.8 加入 OpenAI，参与 Operator、Deep Research 等智能体产品；2025.12 入职腾讯，27 岁掌舵混元。其《AI 的下半场》主张“评价比训练更重要、像产品经理一样思考”。主导训练的混元 Hy3（295B 参数仅激活 21B）Agent 解决率 90%、幻觉率 5.4%，Apache 2.0 完全开源。",
          school: "清华姚班",
        },
        {
          name: "庞天宇",
          role: "混元大模型团队首席研究科学家",
          detail:
            "清华大学计算机系博士，可信机器学习与生成式模型方向学者。2026.1 加盟腾讯，负责多模态强化学习前沿探索。",
          school: "清华博士",
        },
        {
          name: "蒋杰 / 卢山",
          role: "前置负责人 / TEG 总裁",
          detail:
            "蒋杰（集团副总裁、TEG 副总裁、AI Lab 负责人）为姚顺雨之前的总负责人；TEG 总裁卢山温和放权，为混元重组提供空间。",
          school: "—",
        },
      ],
      strategy:
        "“守正出奇”：先回归常识把训练最基础的事做对（重构 Infra、清洗脏数据），再谈创新。提出“模型 × 产品 Co-Design”协同打法——以元宝 AI 助手、企业智能体等全系产品的真实交互数据反哺模型，形成“模型赋能产品、数据反哺模型”闭环。真实落地价值优先于榜单跑分。2025 年腾讯研发投入 857.5 亿元，其中混元及元宝约 180 亿元，并计划翻倍。目标 2027 年进入国内第一梯队。",
      product:
        "元宝 AI 助手、企业智能体、混元生文/文生图（图像 3.0 登 LMArena 文生图盲测第一）、混元视频、混元 3D 世界模型 HY-World 2.0、Agent 产品全景图。",
      sources: [
        "腾讯混元团队百科词条",
        "《当一个年轻人空降：改造腾讯混元的 300 天》（腾讯新闻 2026-07）",
        "《姚顺雨交卷，腾讯混元 Hy3 能力大突破》（腾讯云 2026-07）",
      ],
    },
  },
  {
    id: "bytedance-seed",
    name: "字节Seed",
    tier: 1,
    priority: "第一梯队 · 先投",
    emoji: "🎯",
    direction: "大模型 Agent 应用开发",
    featured: false,
    jd: {
      positions: ["大模型 Agent 框架工程师", "大语言模型 AI 搜索 Agent 算法工程师"],
      capability:
        "Planning/Execution、Tool-Use、Memory、Reflection 四大件；建设 Agent 评测能力（SWE-Bench / TAU-Bench 工程化）；多智能体；RAG + 搜索算法（倒排索引/语义检索）+ Prompt + 微调对齐 + Query 理解。",
      hook:
        "突出 Phase D 多 Agent 编排（LangGraph 同构 + 反思防环）+ Phase E 评测闭环 + Phase C 搜索式 RAG + Phase F 推理 Benchmark 化。",
      intent: "大模型 Agent 框架 / 搜索 Agent 算法工程师",
      stack: ["LangGraph", "Multi-Agent", "RAG", "评测(SWE-Bench同构)", "Function Calling"],
      phaseFocus: "D(编排) → E(评测) → C(搜索RAG) → F(推理Benchmark)",
      recruit: {
        url: "https://jobs.bytedance.com/experienced/position/7596960769942849845/detail",
        label: "字节招聘（Seed 岗位示例）",
      },
    },
    background: {
      summary:
        "字节跳动大模型核心团队，承载豆包等 C 端产品的底层 Agent 与推理能力。以高强度的工程化与评测体系著称，强调“可量化、可回归”的 Agent 研发闭环；在视频生成、多模态与推荐系统结合上具备集团数据/算力优势。",
      keyPeople: [
        {
          name: "Seed 团队",
          role: "字节大模型研发主体",
          detail:
            "对外以 Seed 品牌统一输出基座模型与 Agent 能力；岗位覆盖 Agent 框架、AI 搜索、推理优化、多模态。",
          school: "—",
        },
      ],
      strategy:
        "以“工程化评测 + 数据飞轮”驱动模型迭代，强调在真实搜索/生产力场景落地；大量吸纳头部 AI 人才（含从竞对挖角）。",
      product: "豆包、Coze（扣子低代码 Agent 平台）、即梦、Seed 系列基座模型。",
      sources: ["字节招聘官网 jobs.bytedance.com"],
    },
  },
  {
    id: "zhipu-glm",
    name: "智谱 GLM",
    tier: 1,
    priority: "第一梯队 · 先投",
    emoji: "📚",
    direction: "Agent / MultiAgent / 模型训练",
    featured: false,
    jd: {
      positions: ["GLM-4 agent 模型训练", "Agent 算法工程师", "行业应用方向"],
      capability:
        "LLM、SFT、Agent/MultiAgent、Tool Learning、RAG、RLHF；长文本；CodeGeeX；要求 PyTorch/DeepSpeed/Megatron/VeRL，硕士及以上。",
      hook:
        "突出 MultiAgent（Phase D）+ Tool Learning（Phase A 工具网关）+ 长文本（五段式上下文预算）+ 评测闭环 + 多厂商注册表含智谱。",
      intent: "GLM Agent / MultiAgent 应用开发工程师",
      stack: ["智谱GLM", "Multi-Agent", "Tool Learning", "长文本", "RLHF", "评测"],
      phaseFocus: "D(MultiAgent) → A(工具网关/Tool Learning) → B(长文本) → E(评测)",
      recruit: { url: "https://zhipu-ai.jobs.feishu.cn/", label: "智谱飞书招聘" },
    },
    background: {
      summary:
        "脱胎于清华大学知识工程实验室（KEG）。2006 年唐杰带队发布学术挖掘系统 AMiner，2019.6 成立智谱，2026.1.8 登陆港交所，成为全球“大模型第一股”。坚持原创 GLM 架构、不依赖海外开源底座，深耕 B 端大客户定制化，采用 MaaS（模型即服务）模式，私有化部署占营收约 84.5%。",
      keyPeople: [
        {
          name: "唐杰",
          role: "首席科学家 / 清华计算机系教授（2025.6 卸任董事回清华）",
          detail:
            "1977 年生于四川南充，燕山大学自动化本科、清华计算机博士。KEG 实验室负责人、AMiner 创始人，集 IEEE/ACM/AAAI 三会士。主持研发悟道 2.0、GLM 系列，是智谱技术灵魂人物，仍为最大自然人股东。",
          school: "清华",
        },
        {
          name: "张鹏",
          role: "CEO",
          detail:
            "清华创新领军工程博士，KEG 实验室核心成员，全程参与 AMiner 研发，主导多轮融资（引入腾讯、阿里、美团、小米、蚂蚁等）。",
          school: "清华",
        },
        {
          name: "刘德兵",
          role: "董事长",
          detail: "中科院计算所博士，曾任清华，负责公司战略与资本。与唐杰、张鹏并称“智谱三杰”。",
          school: "清华",
        },
      ],
      strategy:
        "对标 OpenAI，原创 GLM 架构、全栈自研；以 MaaS 输出通用智能能力，重点服务金融、能源、互联网等大客户；同时发力多模态、AI Agent 与出海（东南亚主权 AI）。2025 年 GLM-4.5（3550 亿参数）、GLM-4.6 代码能力登顶全球。",
      product: "ChatGLM、GLM-4 系列、CodeGeeX、智谱清言、MaaS 开放平台、Agent 产品线。",
      sources: [
        "《智谱市值万亿……》（腾讯新闻 2026-06）",
        "《超500亿，清华系智谱敲钟，“大模型第一股”诞生》（搜狐 2026-01）",
      ],
    },
  },
  {
    id: "kimi-moonshot",
    name: "Kimi / 月之暗面",
    tier: 1,
    priority: "第一梯队 · 先投",
    emoji: "🌙",
    direction: "推理框架 / Agentic",
    featured: false,
    jd: {
      positions: ["Kimi 推理框架研发", "Kimi Code 平台推理工程师", "Coding Agent 工程", "Agent Eval"],
      capability:
        "推理框架（vLLM 类）、高吞吐、高并发、系统优化；Agentic 能力；校招含 Agent Eval 研究与产品。",
      hook:
        "突出 Phase F 推理优化（vLLM/量化/continuous batching/speedup≈8x）+ 结构化输出 Function Calling（Phase G）+ 评测闭环 + 开源复用（两个 Trending 项目）。",
      intent: "大模型推理 / Agent 应用开发工程师",
      stack: ["推理优化(vLLM/量化)", "高并发", "Function Calling", "评测闭环", "开源"],
      phaseFocus: "F(推理优化) → G(结构化输出) → E(评测) → C(RAG)",
      recruit: { url: "https://careers.kimi.com/", label: "Kimi 招聘官网" },
    },
    background: {
      summary:
        "2023.4 由杨植麟等四位清华校友创立，以超长文本处理能力的智能助手 Kimi 出圈，公司估值一度冲上 315–500 亿美元并筹备赴港 IPO。核心团队被称为中国 AI 创业“清华梦之队”。2026.7 发布 Kimi K3（2.8 万亿参数开源模型），在 Frontend Code Arena 超越闭源模型登顶。",
      keyPeople: [
        {
          name: "杨植麟",
          role: "创始人 / CEO",
          detail:
            "1992 年生于广东汕头。清华计算机系（年级第一，姚班背景），CMU 博士仅用 4 年（常规 6 年），师从 Ruslan Salakhutdinov 与 William Cohen。读博期间提出 Transformer-XL、XLNet（合计被引超 2 万次）；曾任职 Google Brain、参与华为盘古/悟道、联合创立循环智能。主张“群体智能”（一个老板、一千个工人）。",
          school: "清华（姚班年级第一）",
        },
        {
          name: "周昕宇 / 吴育昕 / 张宇韬",
          role: "联合创始人（均为清华计算机系）",
          detail:
            "周昕宇主导 ShuffleNet；吴育昕参与提出 Group Normalization；张宇韬深耕知识图谱与异构数据融合。四人组成清华系核心技术架构班底。",
          school: "清华",
        },
      ],
      strategy:
        "以长上下文为起点，技术路径“规模优先、算法次之”；最新转向“群体智能”——依靠高质量基模 + 子智能体强化学习 + 长上下文实现 Agent 规模化。坚持开源（K2/K3 登 Hugging Face 榜首）并冲刺港股。",
      product: "Kimi 智能助手、Kimi K 系列基座模型（K2 万亿级、K3 2.8 万亿开源）。",
      sources: [
        "《Kimi创始人杨植麟 技惊全球AI圈》（香港商报 2026-07）",
        "《Kimi时刻到来：冲刺500亿美元估值奔赴港股》（腾讯新闻 2026-07）",
      ],
    },
  },
  {
    id: "deepseek",
    name: "DeepSeek",
    tier: 1,
    priority: "第一梯队 · 先投",
    emoji: "🔭",
    direction: "应用开发 / 全栈 / AI 产品",
    featured: false,
    jd: {
      positions: ["全栈开发工程师", "深度学习研发", "AI 产品经理", "产品运营（2026.6 最大规模招聘新增）"],
      capability:
        "既懂算法又懂系统；极致性能优化（榨干硬件/RDMA/InfiniBand/GPU 集群/算子编译器）；PyTorch/C++/Python/分布式；开源贡献优先；自驱 0→1。",
      hook:
        "工程：零依赖规则降级 + 可观测 + 编译全过 + 推理极致优化 + 成本自负盈亏 + 开源复用。产品：技术理解力 + 跨职能，PM 方向简历 + Agent 产品叙事。",
      intent: "大模型全栈 / 应用开发工程师（及 AI 产品经理）",
      stack: ["系统优化", "分布式", "零依赖", "开源", "成本自负盈亏"],
      phaseFocus: "系统/可观测 → F(极致优化) → 开源复用 → 评测",
      recruit: { url: "https://talent.deepseek.com/", label: "DeepSeek 招聘官网" },
    },
    background: {
      summary:
        "2023.7 由幻方量化创始人梁文锋创立（杭州深度求索）。以“低成本 + 高智能 + 全开源”颠覆行业，R1 论文登上《自然》封面。团队规模小、人才密度极高，工程师多来自清北等本土顶尖高校、鲜有海归，不看经验只看能力。",
      keyPeople: [
        {
          name: "梁文锋",
          role: "创始人",
          detail:
            "1985 年生于广东湛江吴川，17 岁以状元考入浙江大学电子信息工程，获信息与通信工程硕士。幻方量化（千亿私募“四大天王”）创始人，2023 年宣布进军 AGI 并创办 DeepSeek。技术理想主义者，主张“中国要从技术跟随者变成贡献者”。",
          school: "浙大（非清北系）",
        },
      ],
      strategy:
        "开源、技术普惠、AGI；MLA（多头潜在注意力）+ MoE 稀疏架构，用极少算力逼近顶尖模型（V3 训练成本约 557 万美元）。不做中庸的事，用最长期的眼光回答最大的问题。2026.6 大规模招聘重点布局 Agent 研发及产品团队（含 AI 产品经理）。",
      product: "DeepSeek-V 系列、R1 推理模型、DeepSeek-Coder、开源权重与 API。",
      sources: [
        "梁文锋百度百科",
        "《DeepSeek创始人，一个“技术理想主义者”》（京报网 2025-01）",
      ],
    },
  },
];

/* ----------------------------- 第二梯队：典型中小厂 ----------------------------- */
const TIER2 = [
  {
    id: "jd",
    name: "京东",
    tier: 2,
    priority: "第二梯队",
    emoji: "🛒",
    direction: "AI Agent 产品经理",
    jd: {
      positions: ["AI Agent 产品经理"],
      capability: "抹平技术鸿沟，让非技术人员用低代码/自然语言构建、部署、管理 AI Agent，建 AI 智能体生态。",
      hook: "PM 简历重「低代码生态 / 可解释 / 竞品 / 留存」。",
      intent: "AI Agent 产品经理",
      stack: ["低代码", "生态", "可解释", "竞品", "留存"],
      phaseFocus: "产品定义 → 竞品 → 指标 → AI 链路设计",
      recruit: { url: "https://zhaopin.jd.com/", label: "京东招聘（校招 campus.jd.com）" },
    },
  },
  {
    id: "kuaishou",
    name: "快手",
    tier: 2,
    priority: "第二梯队",
    emoji: "🎬",
    direction: "大模型 Agent 研发 / 大模型运营(Agent 搭建)",
    jd: {
      positions: ["大模型 Agent 研发", "大模型运营(Agent 搭建)"],
      capability:
        "企业应用级 Agent：构建可调用大模型服务+业务接口；Python/Go/Java+LangChain；对话/检索/自动决策；Prompt 优化；运营侧拆解违规场景+评估指标。",
      hook: "工程版重「业务接口/检索决策/Prompt」；运营版重「评估指标/策略」。",
      intent: "大模型 Agent 研发 / Agent 运营",
      stack: ["LangChain", "业务接口", "检索决策", "Prompt", "评估指标"],
      phaseFocus: "C(RAG) → 业务接口 → Prompt → 评测指标",
      recruit: { url: "https://zhaopin.kuaishou.cn/", label: "快手招聘（校招 campus.kuaishou.cn）" },
    },
  },
  {
    id: "stepfun",
    name: "阶跃星辰",
    tier: 2,
    priority: "第二梯队",
    emoji: "🪜",
    direction: "多模态 / Agent / 端侧",
    jd: {
      positions: ["多模态大模型与智能应用算法", "Agent 算法", "端侧 AI"],
      capability: "多模态大模型与智能应用（文本/图像/语音）；Agent 算法；端侧 AI；训练框架。",
      hook: "工程版重「多模态 RAG / 端侧量化蒸馏 / 移动答疑」。",
      intent: "多模态 / Agent 应用开发工程师",
      stack: ["多模态RAG", "端侧量化蒸馏", "移动答疑", "Agent"],
      phaseFocus: "C(多模态RAG) → F(端侧) → D(MultiAgent)",
      recruit: { url: "https://www.stepfun.com/", label: "阶跃星辰官网" },
    },
  },
  {
    id: "unitree",
    name: "宇树科技",
    tier: 2,
    priority: "第二梯队",
    emoji: "🤖",
    direction: "具身 Agent 应用开发",
    jd: {
      positions: ["具身 Agent 应用开发", "机器人任务规划"],
      capability: "人形机器人量产龙头（IPO 过会）；机器人任务规划/自然语言交互/具身 Agent。",
      hook: "重「机器人任务规划 / 端侧部署(量化蒸馏) / 低延迟 / 工具调用」。",
      intent: "具身 Agent 应用开发工程师",
      stack: ["机器人任务规划", "端侧部署", "低延迟", "工具调用", "数据飞轮"],
      phaseFocus: "任务规划 → 端侧量化蒸馏 → 工具调用 → 反思",
      recruit: { url: "https://www.unitree.com/cn/position", label: "宇树科技招贤纳士" },
    },
  },
  {
    id: "agibot",
    name: "智元机器人",
    tier: 2,
    priority: "第二梯队",
    emoji: "🦾",
    direction: "具身 Agent 应用开发",
    jd: {
      positions: ["具身 Agent 应用开发", "数据飞轮"],
      capability: "具身智能头部（香港布局/工业落地）；具身 Agent/数据飞轮。",
      hook: "同宇树，重「数据飞轮 / 工业场景落地」。",
      intent: "具身 Agent 应用开发工程师",
      stack: ["具身Agent", "数据飞轮", "工业场景落地", "端侧部署"],
      phaseFocus: "任务规划 → 端侧量化蒸馏 → 工具调用 → 反思",
      recruit: { url: "https://www.agibot.com/", label: "智元机器人官网" },
    },
  },
  {
    id: "galbot",
    name: "银河通用",
    tier: 2,
    priority: "第二梯队",
    emoji: "🌌",
    direction: "具身 Agent 应用开发",
    jd: {
      positions: ["具身 Agent 应用开发"],
      capability: "具身智能平台/工业落地头部。",
      hook: "同具身，重「平台化 / 多机器人编排」。",
      intent: "具身 Agent 应用开发工程师",
      stack: ["具身Agent", "平台化", "多机器人编排", "端侧部署"],
      phaseFocus: "任务规划 → 端侧量化蒸馏 → 工具调用 → 反思",
      recruit: { url: "https://www.galbot.com/", label: "银河通用官网" },
    },
  },
  {
    id: "alibaba-tongyi",
    name: "阿里通义",
    tier: 2,
    priority: "第二梯队",
    emoji: "☁️",
    direction: "大模型应用",
    jd: {
      positions: ["通义大模型 Agent 应用开发"],
      capability: "通义大模型/RAG 数据飞轮/企业落地/百炼平台。",
      hook: "重「RAG 数据飞轮 / 企业级落地 / 多厂商含千问」。",
      intent: "通义大模型 Agent 应用开发工程师",
      stack: ["通义", "RAG数据飞轮", "企业级落地", "百炼平台"],
      phaseFocus: "C(RAG数据飞轮) → 企业级落地 → 多厂商含千问",
      recruit: { url: "https://talent.alibaba.com/", label: "阿里巴巴人才官网" },
    },
  },
  {
    id: "baidu",
    name: "百度",
    tier: 2,
    priority: "第二梯队",
    emoji: "🅑",
    direction: "大模型应用",
    jd: {
      positions: ["文心 / 千帆 Agent 应用开发"],
      capability: "文心/千帆 AppBuilder/企业 Agent。",
      hook: "重「企业级 Agent 搭建 / 低代码 / 检索」。",
      intent: "文心 / 千帆 Agent 应用开发工程师",
      stack: ["文心", "千帆AppBuilder", "企业级Agent", "低代码", "检索"],
      phaseFocus: "企业级Agent搭建 → 低代码 → 检索",
      recruit: { url: "https://talent.baidu.com/", label: "百度人才官网" },
    },
  },
  {
    id: "minimax",
    name: "MiniMax",
    tier: 2,
    priority: "第二梯队",
    emoji: "💬",
    direction: "对话 / Agent",
    jd: {
      positions: ["对话与效率类产品 / abab 模型研发"],
      capability: "对话与效率类产品/abab 模型。",
      hook: "重「对话 Agent / 多轮记忆 / Prompt」。",
      intent: "对话 / Agent 应用开发工程师",
      stack: ["对话Agent", "多轮记忆", "Prompt", "abab模型"],
      phaseFocus: "对话Agent → 多轮记忆 → Prompt",
      recruit: { url: "https://www.minimax.io/", label: "MiniMax 官网" },
    },
  },
  {
    id: "baichuan",
    name: "百川智能",
    tier: 2,
    priority: "第二梯队",
    emoji: "🌊",
    direction: "行业模型",
    jd: {
      positions: ["医疗 / 行业大模型 / Agent 应用开发"],
      capability: "医疗/行业大模型/Agent。",
      hook: "重「行业 RAG / 事实核查 / 垂域」。",
      intent: "行业大模型 Agent 应用开发工程师",
      stack: ["行业RAG", "事实核查", "垂域模型", "医疗"],
      phaseFocus: "行业RAG → 事实核查 → 垂域落地",
      recruit: { url: "https://www.baichuan-ai.com/", label: "百川智能官网" },
    },
  },
  {
    id: "sensetime",
    name: "商汤",
    tier: 2,
    priority: "第二梯队",
    emoji: "🟠",
    direction: "多模态",
    jd: {
      positions: ["日日新多模态 / Agent 平台研发"],
      capability: "日日新多模态/Agent 平台。",
      hook: "重「多模态 RAG / 视觉 Agent」。",
      intent: "多模态 Agent 应用开发工程师",
      stack: ["日日新", "多模态RAG", "视觉Agent", "Agent平台"],
      phaseFocus: "多模态RAG → 视觉Agent → 平台",
      recruit: { url: "https://www.sensetime.com/", label: "商汤官网" },
    },
  },
  {
    id: "meituan",
    name: "美团",
    tier: 2,
    priority: "第二梯队",
    emoji: "🟡",
    direction: "本地生活 Agent",
    jd: {
      positions: ["本地生活业务 Agent / 调度研发"],
      capability: "本地生活业务 Agent/调度。",
      hook: "重「业务接口 / 高并发 / 落地指标」。",
      intent: "本地生活 Agent 应用开发工程师",
      stack: ["业务接口", "高并发", "落地指标", "调度"],
      phaseFocus: "业务接口 → 高并发 → 落地指标",
      recruit: { url: "https://zhaopin.meituan.com/", label: "美团招聘" },
    },
  },
  {
    id: "galaxea",
    name: "星海图",
    tier: 2,
    priority: "第二梯队",
    emoji: "🌠",
    direction: "具身",
    jd: {
      positions: ["具身 Agent 应用开发", "模仿学习数据"],
      capability: "具身模型与数据层创业公司。",
      hook: "重「具身 Agent / 模仿学习数据 / 端侧」。",
      intent: "具身 Agent 应用开发工程师",
      stack: ["具身Agent", "模仿学习数据", "端侧", "数据层"],
      phaseFocus: "具身Agent → 模仿学习数据 → 端侧",
      recruit: { url: "https://galaxea.zhiye.com/", label: "星海图招聘" },
    },
  },
  {
    id: "robotera",
    name: "星动纪元",
    tier: 2,
    priority: "第二梯队",
    emoji: "⭐",
    direction: "具身",
    jd: {
      positions: ["具身 Agent 应用开发"],
      capability: "具身模型与机器人创业公司（清华系背景）。",
      hook: "重「具身 Agent / 端侧部署 / 数据飞轮」。",
      intent: "具身 Agent 应用开发工程师",
      stack: ["具身Agent", "端侧部署", "数据飞轮", "机器人"],
      phaseFocus: "具身Agent → 端侧部署 → 数据飞轮",
      recruit: { url: "https://www.robotera.com/", label: "星动纪元官网" },
    },
  },
  {
    id: "psibot",
    name: "灵初智能",
    tier: 2,
    priority: "第二梯队",
    emoji: "🧠",
    direction: "具身",
    jd: {
      positions: ["具身 Agent 应用开发"],
      capability: "具身智能创业公司。",
      hook: "重「具身 Agent / 端侧 / 工具调用」。",
      intent: "具身 Agent 应用开发工程师",
      stack: ["具身Agent", "端侧", "工具调用", "灵巧操作"],
      phaseFocus: "具身Agent → 端侧 → 工具调用",
      recruit: { url: "https://www.psibot.ai/careers_zh/", label: "灵初智能招聘" },
    },
  },
];

/* ----------------------------- 团队背景图谱：清华系 / 北大系 ----------------------------- */
const LINEAGE = {
  qinghua: {
    title: "清华系 · AI 大模型“梦之队”",
    desc:
      "清华（尤其姚班 / KEG / 交叉信息研究院）在大模型创业中占据主导。从智谱、月之暗面到腾讯混元，核心创始人多为清华计算机系出身。",
    members: [
      { name: "姚顺雨", company: "腾讯混元", role: "首席 AI 科学家", school: "清华姚班 / 普林斯顿博士", note: "ReAct / ToT / Reflexion 作者，Agent 领域奠基人" },
      { name: "唐杰 · 张鹏 · 刘德兵", company: "智谱 GLM", role: "首席科学家 / CEO / 董事长（“智谱三杰”）", school: "清华 KEG", note: "脱胎于清华知识工程实验室，2026 港股“大模型第一股”" },
      { name: "杨植麟", company: "月之暗面 Kimi", role: "创始人 / CEO", school: "清华计算机系（姚班年级第一）/ CMU 博士", note: "Transformer-XL / XLNet 作者，清华“梦之队”" },
      { name: "周昕宇 · 吴育昕 · 张宇韬", company: "月之暗面 Kimi", role: "联合创始人", school: "清华计算机系", note: "ShuffleNet / Group Normalization / 知识图谱" },
      { name: "王小川", company: "百川智能", role: "创始人", school: "清华", note: "搜狗系，医疗/行业大模型" },
      { name: "刘知远", company: "面壁智能", role: "联合创始人 / 清华教授", school: "清华", note: "CPM / MiniCPM 端侧大模型" },
      { name: "夏立雪", company: "无问芯穹", role: "联合创始人 / CEO", school: "清华", note: "大模型推理与算力优化基础设施" },
      { name: "朱军", company: "生数科技 / Vidu", role: "首席科学家 / 清华教授", school: "清华", note: "多模态生成模型" },
      { name: "陈建宇", company: "星动纪元", role: "创始人 / 清华助理教授", school: "清华", note: "具身智能与人形机器人" },
    ],
  },
  beida: {
    title: "北大系 · 通用智能与 Agentic AI 路线",
    desc:
      "大模型时代北大未涌现智谱级头部基模公司，但北大系人才活跃在核心研发链与差异化赛道：通用智能、机器视觉、Agentic AI。百度李彦宏是互联网时代北大 AI 产业名片。",
    members: [
      { name: "吴明辉", company: "明略科技 (2718.HK)", role: "创始人 / CEO / CTO", school: "北大计算机硕士 / 博士", note: "2025.11 港交所上市，全球“Agentic AI 第一股”，DeepMiner 大模型" },
      { name: "林俊旸", company: "原阿里 Qwen → 新创业", role: "原 Qwen 核心研发", school: "北大", note: "2026.3 离职筹备 AI 创业，种子轮估值约 20 亿美元" },
      { name: "朱松纯", company: "北京通用人工智能研究院", role: "院长 / 北大讲席教授", school: "北大", note: "通用智能与机器人“通脑”引擎，强调“无限任务/自主产生任务/价值驱动”" },
      { name: "黄铁军", company: "脉冲视觉（原智源院长）", role: "北大教授", school: "北大", note: "机器视觉与神经形态计算、超高速脉冲相机产业化" },
      { name: "李彦宏", company: "百度", role: "创始人", school: "北大", note: "互联网时代北大 AI 产业名片；文心 / 千帆 Agent" },
      { name: "袁粒 · 董少灵", company: "兔展智能", role: "首席科学家 / 创始人", school: "北大（袁粒为北大助理教授）", note: "视觉 AI / 严肃商业图像生成，筹备港交所上市" },
    ],
  },
};

/* ----------------------------- 简历打磨：6 条具体改动 ----------------------------- */
const RESUME_TIPS = [
  {
    t: "ATS 关键词前置",
    d: "技术栈第一行放 LangChain/LangGraph、RAG、Multi-Agent、MCP、Function Calling、FastAPI（对齐统计高频词）。",
  },
  {
    t: "每条经历补「落地四件套」",
    d: "技术 + 规模 + 指标 + 上线。例：把“实现 RAG”改为“RAG（TF-IDF+2-gram+RRF）落地，citation_rate=1.0、hallucination_rate=0.0，已上线”。",
  },
  {
    t: "突出开源 / 复用",
    d: "把“两个 Trending 项目复用同一 core”提到技术总结首句，命中“开源贡献”高频关注点。",
  },
  {
    t: "补 2026 新标配词",
    d: "MCP（已落地）、Dify（低代码生态叙事）、AutoGen（多 Agent 同构）显式写入。",
  },
  {
    t: "量化统一口径",
    d: "hit_rate / citation_rate / reject_rate / hallucination_rate / speedup≈8x / kv_cache_hit_rate≈0.8 作为固定数字资产，每版复用。",
  },
  {
    t: "PM 方向补「低代码/生态/可解释」",
    d: "对齐京东/百度 AppBuilder 类岗位；工程方向补「系统/分布式/开源」对齐 DeepSeek/字节。",
  },
];

/* ----------------------------- 分厂定制策略表 ----------------------------- */
const RESUME_STRATEGY = [
  { company: "字节 Seed", intent: "大模型 Agent 框架 / 搜索 Agent 算法工程师", stack: "LangGraph·Multi-Agent·RAG·评测(SWE-Bench 同构)·Function Calling", phase: "D(编排)→E(评测)→C(搜索RAG)→F(推理Benchmark)" },
  { company: "腾讯混元", intent: "混元大模型 Agent 应用开发工程师", stack: "混元·RAG事实核查·多轮记忆·Agent强化·Post-training", phase: "C(防幻觉)→B(记忆多轮)→G(混元优先)→D(反思强化)" },
  { company: "智谱 GLM", intent: "GLM Agent / MultiAgent 应用开发工程师", stack: "智谱GLM·Multi-Agent·Tool Learning·长文本·RLHF·评测", phase: "D(MultiAgent)→A(工具网关/Tool Learning)→B(长文本)→E(评测)" },
  { company: "Kimi", intent: "大模型推理 / Agent 应用开发工程师", stack: "推理优化(vLLM/量化)·高并发·Function Calling·评测闭环·开源", phase: "F(推理优化)→G(结构化输出)→E(评测)→C(RAG)" },
  { company: "DeepSeek", intent: "大模型全栈 / 应用开发工程师（及 AI 产品经理）", stack: "系统优化·分布式·零依赖·开源·成本自负盈亏", phase: "系统/可观测→F(极致优化)→开源复用→评测" },
  { company: "京东(PM)", intent: "AI Agent 产品经理", stack: "低代码·生态·可解释·竞品·留存（技术弱显）", phase: "产品定义→竞品→指标→AI链路设计" },
  { company: "快手", intent: "大模型 Agent 研发 / Agent 运营", stack: "LangChain·业务接口·检索决策·Prompt·评估指标", phase: "C(RAG)→业务接口→Prompt→评测指标" },
  { company: "阶跃星辰", intent: "多模态 / Agent 应用开发工程师", stack: "多模态RAG·端侧量化蒸馏·移动答疑·Agent", phase: "C(多模态RAG)→F(端侧)→D(MultiAgent)" },
  { company: "宇树/智元/银河通用", intent: "具身 Agent 应用开发工程师", stack: "机器人任务规划·端侧部署·低延迟·工具调用·数据飞轮", phase: "任务规划→端侧量化蒸馏→工具调用→反思" },
];

/* ----------------------------- 招聘入口速查表 ----------------------------- */
const RECRUIT_TABLE = [
  { tier: 1, company: "字节 Seed", dir: "大模型 Agent 框架 / AI 搜索 Agent 算法", url: "https://jobs.bytedance.com/" },
  { tier: 1, company: "腾讯混元", dir: "混元大模型 Agent 应用开发 / 应用算法", url: "https://careers.tencent.com/" },
  { tier: 1, company: "智谱 GLM", dir: "GLM Agent / Multi-Agent 应用开发", url: "https://zhipu-ai.jobs.feishu.cn/" },
  { tier: 1, company: "Kimi（月之暗面）", dir: "大模型推理 / Agent 应用开发", url: "https://careers.kimi.com/" },
  { tier: 1, company: "DeepSeek", dir: "大模型全栈 / 应用开发 / AI 产品经理", url: "https://talent.deepseek.com/" },
  { tier: 2, company: "京东", dir: "AI Agent 产品经理", url: "https://zhaopin.jd.com/" },
  { tier: 2, company: "快手", dir: "大模型 Agent 研发 / Agent 运营", url: "https://zhaopin.kuaishou.cn/" },
  { tier: 2, company: "阶跃星辰", dir: "多模态 / Agent 应用开发", url: "https://www.stepfun.com/" },
  { tier: 2, company: "宇树科技", dir: "具身 Agent 应用开发", url: "https://www.unitree.com/cn/position" },
  { tier: 2, company: "智元机器人", dir: "具身 Agent 应用开发", url: "https://www.agibot.com/" },
  { tier: 2, company: "银河通用", dir: "具身 Agent 应用开发", url: "https://www.galbot.com/" },
  { tier: 2, company: "阿里通义", dir: "通义大模型 Agent 应用开发", url: "https://talent.alibaba.com/" },
  { tier: 2, company: "百度", dir: "文心 / 千帆 Agent 应用开发", url: "https://talent.baidu.com/" },
  { tier: 2, company: "MiniMax", dir: "对话 / Agent 应用开发", url: "https://www.minimax.io/" },
  { tier: 2, company: "百川智能", dir: "行业大模型 Agent 应用开发", url: "https://www.baichuan-ai.com/" },
  { tier: 2, company: "商汤", dir: "多模态 Agent 应用开发", url: "https://www.sensetime.com/" },
  { tier: 2, company: "美团", dir: "本地生活 Agent 应用开发", url: "https://zhaopin.meituan.com/" },
  { tier: 2, company: "星海图", dir: "具身 Agent 应用开发", url: "https://galaxea.zhiye.com/" },
  { tier: 2, company: "星动纪元", dir: "具身 Agent 应用开发", url: "https://www.robotera.com/" },
  { tier: 2, company: "灵初智能", dir: "具身 Agent 应用开发", url: "https://www.psibot.ai/careers_zh/" },
];

const ALL_COMPANIES = [...TIER1, ...TIER2];
