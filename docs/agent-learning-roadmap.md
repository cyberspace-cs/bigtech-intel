# Agent 学习路线 · 分支 A（算法 / 后训练 / RL）

> 配套「大厂情报站」。面向 **工作 1 年的社招**选手，主线 = **Agent 应用开发 → 后训练把能力固化进模型 → RL（GRPO/DPO）对齐**，
> 目标厂锁定 **智谱GLM / DeepSeek / 百川智能 / 商汤** 的算法 / 后训练 / Agent 岗。
> 路线映射自 [datawhalechina/Agent-Learning-Hub](https://github.com/datawhalechina/Agent-Learning-Hub)（9 Stage + 11 级项目阶梯），
> 每周对口岗位均来自本站真实招聘情报（bigtech-intel 库的 `recruit_intel` 表）。
> 更新于 2026-07-26。

---

## 〇、需求信号（为什么是这条主线）

来自本站 65 条招聘情报的关键词统计（决定主线权重）：

| 关键词 | 全库命中 | 说明 |
|--------|---------|------|
| Agent | 168 | 最 dominant 的社招需求 |
| 算法 | 70 | 算法工程是 1 年经验的主入口 |
| 后训练 | 8 | 集中出现在 Branch A 四厂 JD |
| 预训练 | 3 | 智谱 / DeepSeek 核心岗要求 |
| GRPO / DPO | 4 | RL 对齐硬通货 |
| 强化 | 2 | 与后训练强绑定 |
| **Branch A 真实情报** | **12 条** | 智谱GLM / DeepSeek / 百川智能 / 商汤 |

**结论**：「后训练 / GRPO / DPO / 预训练 / 强化」集中出现在 Branch A 四厂 JD，是 1 年经验最值得追加投入的**差异化方向**——平台工程线容易被应届 flooded，后训练/RL 反而有稀缺性。

---

## 一、为什么走分支 A（而非平台工程线）

1. **壁垒更高**：后训练 / RL 是算法岗硬通货，1 年社招卷平台工程线易和应届竞争，卷后训练/RL 有稀缺性。
2. **对口明确**：智谱（后训练/Agent/推理 Infra）、DeepSeek（大模型算法/Agent Harness）、百川（大模型算法）、商汤（通用智能体/Agent Harness）均在招。
3. **作品可量化**：GRPO 成功率、自建 trajectory 规模、eval 指标——简历里能写死的"数字资产"。

**Branch A 四厂在本站的真实条目（12 条）：**

| 公司 | 类型 | 岗位 | 城市 | 来源 |
|------|------|------|------|------|
| 智谱GLM | 校招 | 后训练/Agent/推理 Infra | 北京 | 智谱招聘(飞书) |
| 智谱GLM | 实习 | 27届 后训练算法工程师 | 北京 | 实习僧/wondercv |
| 智谱GLM | 实习 | 2027 实习（大模型/Agent） | 北京 | 智谱招聘(飞书) |
| DeepSeek | 社招 | 大模型算法工程师 | 杭州 | DeepSeek 官网 |
| DeepSeek | 实习 | Agent Harness 团队 | 北京 | DeepSeek 官网 |
| DeepSeek | 社招 | 研究员/工程师 扩招（全岗） | 杭州 | DeepSeek 官网 |
| 百川智能 | 实习 | 大模型算法工程师 | 北京 | 百川智能招聘 |
| 百川智能 | 社招 | 大模型算法工程师 | 北京 | 百川智能招聘 |
| 百川智能 | 实习 | 数据策略产品经理 | 北京 | 牛客 |
| 商汤 | 实习 | 多模态大模型算法-GUI Agent | 北京 | 商汤招聘 |
| 商汤 | 校招 | 通用智能体研究员/Agent Harness | 深圳 | 商汤招聘 |
| 商汤 | 实习 | AI 先锋 顶尖实习生 | 上海 | 商汤招聘 |

---

## 二、10 周路线图（每周对标真实岗位）

| 周 | Hub Stage | Branch A 聚焦 | 交付物（作品集） | 对口岗位 | 资源 |
|----|-----------|--------------|------------------|----------|------|
| W0 | 0 认知对齐 | 为什么大模型需要 Agent；后训练如何把 Agent 能力"固化"进模型（SFT→RL 数据飞轮）；建立「Agent vs Workflow」边界 | 一页笔记：Agent 与 Workflow 边界 + 后训练在 Agent 闭环里的位置（面试必问） | 全部（面试必问） | Anthropic/OpenAI 官方 Agent 指南；Hub Stage 0 |
| W1–2 | 1 最小 Loop + ReAct | 从 ReAct（Thought-Action-Observation）入手，手写一个能调工具的 Agent loop，不依赖框架；理解「模型决策↔环境反馈」最小闭环 | 150 行 ReAct Agent + 工具集（搜索/计算/DB），可跑通可调试 | DeepSeek 大模型算法（社招/杭州）；百川智能 大模型算法（社招/北京） | ReAct 原论文；Hub L1/L2 |
| W3 | 2 RAG & 记忆 + Reflexion | Reflexion：用「自我反思」替代微调提升 Agent；配套记忆机制；理解"轨迹→反思→改进"如何成为 RL 的 reward 信号雏形 | Reflexion demo（失败→反思→重试），带记忆持久化 | 商汤 多模态大模型-GUI Agent（北京） | Reflexion 论文；mem0 |
| W4–5 | 3 深读 Harness + Agent Infra | 读 DeepSeek/Agent Harness 思路：模型如何被"用起来"产生 agentic 训练数据；搭建可调试 harness，产出自建 trajectory 数据集 | 可调试 harness + 一份 agentic trajectory 数据集（自建，后续喂后训练） | DeepSeek Agent Harness 实习（北京）；智谱GLM 后训练/Agent/推理 Infra（校招/北京） | claw0；learn-claude-code（从 0 复刻） |
| W6 | 4 多 Agent + 训练数据构造 | 多 Agent 协作产出的轨迹 → 变成 SFT/RL 训练数据（数据飞轮）。这是 Branch A 与平台工程线的分水岭：你造数据，不只是用数据 | 一份「多 Agent 对话→trajectory」pipeline，可批量产出训练样本 | 智谱GLM 后训练算法实习（北京）；商汤 通用智能体研究员/Agent Harness（校招/深圳） | LangGraph；后训练数据管线实践 |
| W7 | 5 Skills/MCP + 对齐入门 | 把 MCP/Skills 当作 RL 环境里"可控、可验证"的工具；入门奖励建模（reward modeling）——可验证奖励是 GRPO 的关键 | 一个带可验证奖励的小任务 + 手写 reward 函数 | 腾讯/字节 平台岗（差异化加分项） | MCP 官方 servers；RLHF/奖励建模教程 |
| W8 | 6/7 评测 + 强化学习入门（核心周） | RL for LLM 主线：SFT → RM → RLHF(PPO) → DPO → GRPO；自写 GRPO 训练 loop（小模型即可），配 20+ 任务 eval 表 | 一个可跑的 GRPO 训练脚本（小模型）+ eval 表（成功率/失败分类） | 智谱GLM/DeepSeek 后训练岗；全部大模型算法岗 | DPO/GRPO 论文；TRL；OpenAI Evals |
| W9 | 8 Ship | 把前 8 周产出拼成「Agent + 后训练」作品集项目（Production 级、可 clone 跑），简历核心资产 | 作品集核心 repo（ReAct + Reflexion + trajectory→后训练 + GRPO 闭环） | 投递时直接展示，对应各厂后训练/Agent 职责 | 复用前 8 周所有产出 |
| W10 | 冲刺 · 对标投递 | 用站里 Branch A 12 条情报筛目标厂，写简历 bullet，锚定"后训练/Agent/推理 Infra"关键词 | 简历定稿（含固定数字资产：GRPO 成功率、trajectory 规模、eval 指标） | 智谱GLM / DeepSeek / 百川智能 / 商汤 | 你自己的 bigtech 站·招聘情报（仅社招/实习筛选） |

---

## 三、核心作品集指标（简历固定数字资产）

- `GRPO 成功率`：在 20+ 任务上的成功率（与基线 SFT 对比，如 +X%）
- `trajectory 规模`：自建 agentic trajectory 数据集条数（如 5k+）
- `citation_rate` / `hallucination_rate`：RAG 环节的引用率 / 幻觉率（如 1.0 / 0.0，若含 RAG 模块）
- `eval 覆盖率`：20+ 任务中可自动化评估的比例

每版简历复用同一组数字，避免临场编造。

---

## 四、面试准备（Branch A 向）

### 4.1 必考知识点
- **Agent 基础**：ReAct、Reflexion、Function Calling、多 Agent 编排（LangGraph）、失败模式与防环。
- **后训练**：SFT → RM → RLHF(PPO) → DPO → GRPO 全链路；数据构造（trajectory → 训练样本）；奖励建模。
- **RL 对齐**：GRPO 的 group-relative 优势估计、DPO 的偏好损失、可验证奖励（verifiable reward）。
- **推理/Infra**：vLLM、continuous batching、KV cache、量化（与 Agent 落地相关）。

### 4.2 各厂简历 hook
- **智谱GLM**：后训练 + Agent + 推理 Infra；强调 trajectory 数据飞轮与 eval 闭环。
- **DeepSeek**：系统/可观测 → 极致优化 → 开源复用 → 评测；强调 GRPO/DPO 实操与 harness 经验。
- **百川智能**：大模型算法工程；强调 SFT/RL 全流程与工程落地。
- **商汤**：通用智能体 / Agent Harness；强调多模态 + GUI Agent + 多 Agent 协作数据。

### 4.3 答题框架（STAR + 数字）
每道题用「情境 → 任务 → 行动 → 结果（带上面固定数字）」收口；把作品集项目当万能案例库，按厂 hook 切换侧重点。

---

## 五、本周就能开始的 3 件事

1. 通读 Agent-Learning-Hub 的 Stage 0 两篇官方指南，写那页「为什么需要 Agent + 后训练在哪」笔记。
2. 跑通一个 150 行 ReAct Agent loop（参考 Hub L1/L2），先不碰框架。
3. 在本站把「智谱GLM / DeepSeek」的后训练 / 大模型算法 JD 各存一条，作为 W1–W9 的对照基线（去「招聘情报」粘贴即结构化）。

---

## 六、落地说明

- 本站「学习路线」Tab 已内置本路线图，并实时拉取 Branch A 四厂的对口岗位（调用 `/api/jd` 过滤）。
- 路线依据本站 65 条真实情报 + Agent-Learning-Hub 课程结构设计；对口岗位随情报库更新而动态变化。
- 若转投平台工程线（分支 B 具身智能 / 平台应用），可在站内另建视图，复用同一套 Stage 框架。
