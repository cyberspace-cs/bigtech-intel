# Agent 学习路线 · 分支 A（算法 / 后训练 / RL）

> 配套「大厂情报站」。面向 **工作 1 年的社招**选手，主线 = **Agent 应用开发 → 后训练把能力固化进模型 → RL（GRPO/DPO）对齐**，
> 目标厂锁定 **智谱GLM / DeepSeek / 百川智能 / 商汤** 的算法 / 后训练 / Agent 岗。
> 路线综合自 4 个开源仓库（[Agent-Learning-Hub](https://github.com/datawhalechina/Agent-Learning-Hub) / [AgentGuide 算法路线](https://github.com/cyberspace-cs/AgentGuide/blob/main/docs/05-roadmaps/learning-roadmap-algorithm.md) / [diy-llm](https://github.com/datawhalechina/diy-llm) / [llm-algo-leetcode](https://github.com/datawhalechina/llm-algo-leetcode)），
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

## 一、学习资源库（4 个可点击仓库）

| 仓库 | 地址 | 用途 |
|------|------|------|
| **Agent-Learning-Hub** | https://github.com/datawhalechina/Agent-Learning-Hub | 9 Stage（认知→最小 Loop→RAG/记忆→Harness→多 Agent→Skills/MCP→评测→Ship）+ 11 级项目阶梯。**Agent 应用开发主线权威路径**。 |
| **AgentGuide · 算法路线图** | https://github.com/cyberspace-cs/AgentGuide/blob/main/docs/05-roadmaps/learning-roadmap-algorithm.md | 9 周研究型 AI Agent 算法工程师路线：Transformer 手撕 → ReAct/Reflexion/ToT → RAG 算法 → Memory → RL/DPO/GRPO → 论文/开源产出。**Branch A 算法主线**。 |
| **diy-llm** | https://github.com/datawhalechina/diy-llm（在线阅读 https://datawhalechina.github.io/diy-llm/） | CS336 中文版 15 章。**第 10 章「推理」**(KV Cache/投机解码/量化 GPTQ·AWQ/PagedAttention/Continuous Batching)、**第 13 章训练流程**(Pre-training/SFT/DPO/RLHF PPO)、**第 14 章可验证奖励 RL**(GRPO/RLVR/R1)。推理优化 + 后训练硬核教材。 |
| **llm-algo-leetcode** | https://github.com/datawhalechina/llm-algo-leetcode（在线阅读 https://datawhalechina.github.io/llm-algo-leetcode/） | PyTorch 算法实战 + Triton + CUDA。覆盖 Transformer/Attention/KV Cache/PagedAttention/对齐/微调/分布式/显存/推理优化，底层算子与面试算法题首选。 |

---

## 二、三大技术栈（Agent 开发 / 算法 / 大模型推理优化）

### 2.1 Agent 开发技术栈
- **编排框架**：[LangGraph](https://langchain-ai.github.io/langgraph/) · [hello-agents](https://github.com/datawhalechina/hello-agents) · [claw0](https://github.com/shareAI-lab/claw0) · [learn-claude-code](https://github.com/shareAI-lab/learn-claude-code)
- **工具 / MCP**：[Model Context Protocol](https://modelcontextprotocol.io/) · [MCP Servers](https://github.com/modelcontextprotocol/servers) · [Claude Code Skills](https://code.claude.com/docs/en/skills)
- **RAG / 记忆**：[mem0](https://github.com/mem0ai/mem0) · [Letta](https://github.com/letta-ai/letta) · [RAGFlow](https://github.com/infiniflow/ragflow) · [LlamaIndex](https://docs.llamaindex.ai/en/stable/use_cases/agents/)
- **多 Agent / 协议**：[Claude Subagents](https://code.claude.com/docs/en/sub-agents) · [A2A Protocol](https://a2a-protocol.org/latest/specification/) · [Agent Client Protocol](https://agentclientprotocol.com/)
- **评测 / 可观测**：[OpenAI Evals](https://platform.openai.com/docs/guides/evals) · [SWE-bench](https://arxiv.org/abs/2310.06770) · [LangSmith](https://docs.smith.langchain.com/) · [AgentBench](https://arxiv.org/abs/2308.03688)
- **必读范式**：[Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) · [OpenAI: Practical guide](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) · [GPT Researcher](https://github.com/assafelovic/gpt-researcher)

### 2.2 算法技术栈（Branch A 主线）
- **基础 / 架构**：[nanoGPT](https://github.com/karpathy/nanoGPT) · [LLMs from scratch](https://github.com/rasbt/LLMs-from-scratch) · [Attention Is All You Need](https://arxiv.org/abs/1706.03762) · [llm-algo-leetcode · Transformer](https://github.com/datawhalechina/llm-algo-leetcode)
- **Agent 算法**：[ReAct](https://arxiv.org/abs/2210.03629) · [Reflexion](https://arxiv.org/abs/2303.11366) · [Tree of Thoughts](https://arxiv.org/abs/2305.10601) · [AgentGuide 算法路线](https://github.com/cyberspace-cs/AgentGuide/blob/main/docs/05-roadmaps/learning-roadmap-algorithm.md)
- **RAG 算法**：[BM25/DPR](https://arxiv.org/abs/2004.04906) · [Self-RAG](https://arxiv.org/abs/2310.11511) · [GraphRAG](https://www.microsoft.com/en-us/research/project/graphrag/) · [RAGAs](https://github.com/explodinggradients/ragas)
- **记忆 / 上下文工程**：[MemGPT](https://arxiv.org/abs/2310.08560) · [Generative Agents](https://arxiv.org/abs/2304.03442) · [diy-llm Ch5 MoE](https://github.com/datawhalechina/diy-llm)
- **后训练 / 对齐**：[LLaMA-Factory (SFT/LoRA)](https://github.com/hiyouga/LLaMA-Factory) · [TRL (DPO/GRPO)](https://github.com/huggingface/trl) · [OpenRLHF (PPO)](https://github.com/OpenLLMAI/OpenRLHF) · [diy-llm Ch13/14](https://github.com/datawhalechina/diy-llm)
- **评估 / 对齐基准**：[lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) · [OpenCompass](https://github.com/open-compass/opencompass) · [DPO 论文](https://arxiv.org/abs/2305.18290) · [GRPO 论文](https://arxiv.org/pdf/2402.03300) · [DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1)

### 2.3 大模型推理优化技术栈
- **推理框架**：[vLLM (PagedAttention)](https://github.com/vllm-project/vllm) · [SGLang (radix cache)](https://github.com/sgl-project/sglang) · [diy-llm Ch10 推理](https://github.com/datawhalechina/diy-llm)
- **量化**：[GPTQ](https://arxiv.org/abs/2210.17323) · [AWQ](https://arxiv.org/abs/2306.00978) · [Unsloth](https://github.com/unslothai/unsloth) · [llm-algo-leetcode 推理优化](https://github.com/datawhalechina/llm-algo-leetcode)
- **KV Cache / 注意力**：[PagedAttention](https://github.com/vllm-project/vllm) · [FlashAttention](https://arxiv.org/abs/2205.14135) · [MQA/GQA](https://arxiv.org/abs/2305.13245) · [diy-llm Ch6 GPU 优化](https://github.com/datawhalechina/diy-llm)
- **投机解码**：[Speculative Decoding](https://arxiv.org/abs/2211.17192) · [diy-llm Ch10](https://github.com/datawhalechina/diy-llm)
- **上下文压缩 / 蒸馏**：[LLMLingua](https://github.com/microsoft/LLMLingua) · [知识蒸馏 KD](https://arxiv.org/abs/1503.02531) · [nanochat](https://github.com/karpathy/nanochat)
- **工程落地参考**：本项目 inference.py 实战（[personal-portfolio](https://github.com/cyberspace-cs/personal-portfolio)）· [Continuous Batching](https://github.com/vllm-project/vllm)

---

## 三、为什么走分支 A（而非平台工程线）

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
| 商汤 | 实习 | 多模态大模型-GUI Agent | 北京 | 商汤招聘 |
| 商汤 | 校招 | 通用智能体研究员/Agent Harness | 深圳 | 商汤招聘 |
| 商汤 | 实习 | AI 先锋 顶尖实习生 | 上海 | 商汤招聘 |

---

## 四、10 周路线图（每周对标真实岗位 + 可点击资源）

| 周 | Hub Stage | Branch A 聚焦 | 交付物（作品集） | 对口岗位 | 资源（可点击） |
|----|-----------|--------------|------------------|----------|------|
| W0 | 0 认知对齐 | 为什么大模型需要 Agent；后训练如何把 Agent 能力"固化"进模型（SFT→RL 数据飞轮）；建立「Agent vs Workflow」边界 | 一页笔记：Agent 与 Workflow 边界 + 后训练在 Agent 闭环里的位置（面试必问） | 全部（面试必问） | [Anthropic 指南](https://www.anthropic.com/engineering/building-effective-agents) · [OpenAI 指南](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) · [Hub Stage 0](https://github.com/datawhalechina/Agent-Learning-Hub) |
| W1–2 | 1 最小 Loop + ReAct | 手写能调工具的 Agent loop，不依赖框架；理解「模型决策↔环境反馈」最小闭环 | 150 行 ReAct Agent + 工具集，可跑通可调试 | DeepSeek 大模型算法（社招/杭州）；百川智能 大模型算法（社招/北京） | [ReAct 论文](https://arxiv.org/abs/2210.03629) · [Hub L1/L2](https://github.com/datawhalechina/Agent-Learning-Hub) · [Function Calling](https://platform.openai.com/docs/guides/function-calling) |
| W3 | 2 RAG & 记忆 + Reflexion | Reflexion 替代微调提升 Agent；"轨迹→反思→改进"成为 RL reward 雏形 | Reflexion demo（失败→反思→重试），带记忆持久化 | 商汤 多模态大模型-GUI Agent（北京） | [Reflexion 论文](https://arxiv.org/abs/2303.11366) · [mem0](https://github.com/mem0ai/mem0) · [Hub Stage 2](https://github.com/datawhalechina/Agent-Learning-Hub) |
| W4–5 | 3 深读 Harness + Agent Infra | 读 Agent Harness 思路：模型被"用起来"产生 agentic 训练数据；搭建可调试 harness，产出自建 trajectory 数据集 | 可调试 harness + 一份 agentic trajectory 数据集（后续喂后训练） | DeepSeek Agent Harness 实习（北京）；智谱GLM 后训练/Agent/推理 Infra（校招/北京） | [claw0](https://github.com/shareAI-lab/claw0) · [learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) · [Hub Stage 3](https://github.com/datawhalechina/Agent-Learning-Hub) |
| W6 | 4 多 Agent + 训练数据构造 | 多 Agent 轨迹 → SFT/RL 训练数据（数据飞轮）。分水岭：你造数据，不只是用数据 | 「多 Agent 对话→trajectory」pipeline，可批量产出训练样本 | 智谱GLM 后训练算法实习（北京）；商汤 通用智能体研究员/Agent Harness（校招/深圳） | [LangGraph](https://langchain-ai.github.io/langgraph/) · [Claude Subagents](https://code.claude.com/docs/en/sub-agents) · [AgentGuide 多 Agent 周](https://github.com/cyberspace-cs/AgentGuide/blob/main/docs/05-roadmaps/learning-roadmap-algorithm.md) |
| W7 | 5 Skills/MCP + 对齐入门 | 把 MCP/Skills 当作 RL 环境里"可控、可验证"的工具；入门奖励建模 | 一个带可验证奖励的小任务 + 手写 reward 函数 | 腾讯/字节 平台岗（差异化加分项） | [MCP](https://modelcontextprotocol.io/) · [AgentGuide 对齐/RL 周](https://github.com/cyberspace-cs/AgentGuide/blob/main/docs/05-roadmaps/learning-roadmap-algorithm.md) · [OpenRLHF](https://github.com/OpenLLMAI/OpenRLHF) |
| W8 | 6/7 评测 + 强化学习入门（核心周） | RL for LLM：SFT → RM → RLHF(PPO) → DPO → GRPO；自写 GRPO loop + 20+ 任务 eval 表 | 可跑的 GRPO 训练脚本（小模型）+ eval 表 | 智谱GLM/DeepSeek 后训练岗；全部大模型算法岗 | [DPO 论文](https://arxiv.org/abs/2305.18290) · [GRPO 论文](https://arxiv.org/pdf/2402.03300) · [TRL](https://github.com/huggingface/trl) · [diy-llm Ch13/14](https://github.com/datawhalechina/diy-llm) · [OpenAI Evals](https://platform.openai.com/docs/guides/evals) |
| W9 | 8 Ship | 拼成「Agent + 后训练」作品集项目（Production 级、可 clone 跑） | 作品集核心 repo（ReAct + Reflexion + trajectory→后训练 + GRPO 闭环） | 投递时直接展示 | [Hub Stage 8](https://github.com/datawhalechina/Agent-Learning-Hub) · [L11 项目阶梯](https://github.com/datawhalechina/Agent-Learning-Hub) |
| W10 | 冲刺 · 对标投递 | 用站里 Branch A 12 条情报筛目标厂，写简历 bullet，锚定"后训练/Agent/推理 Infra"关键词 | 简历定稿（含 GRPO 成功率、trajectory 规模、eval 指标） | 智谱GLM / DeepSeek / 百川智能 / 商汤 | [本站招聘情报](http://localhost:8031/#/recruit) |

---

## 五、核心作品集指标（简历固定数字资产）

- `GRPO 成功率`：在 20+ 任务上的成功率（与基线 SFT 对比，如 +X%）
- `trajectory 规模`：自建 agentic trajectory 数据集条数（如 5k+）
- `citation_rate` / `hallucination_rate`：RAG 环节的引用率 / 幻觉率（如 1.0 / 0.0，若含 RAG 模块）
- `eval 覆盖率`：20+ 任务中可自动化评估的比例

每版简历复用同一组数字，避免临场编造。

---

## 六、面试准备（Branch A 向）

### 6.1 必考知识点
- **Agent 基础**：ReAct、Reflexion、Function Calling、多 Agent 编排（LangGraph）、失败模式与防环。
- **后训练**：SFT → RM → RLHF(PPO) → DPO → GRPO 全链路；数据构造（trajectory → 训练样本）；奖励建模。
- **RL 对齐**：GRPO 的 group-relative 优势估计、DPO 的偏好损失、可验证奖励（verifiable reward）。
- **推理/Infra**：vLLM、continuous batching、KV cache、量化（与 Agent 落地相关）。

### 6.2 各厂简历 hook
- **智谱GLM**：后训练 + Agent + 推理 Infra；强调 trajectory 数据飞轮与 eval 闭环。
- **DeepSeek**：系统/可观测 → 极致优化 → 开源复用 → 评测；强调 GRPO/DPO 实操与 harness 经验。
- **百川智能**：大模型算法工程；强调 SFT/RL 全流程与工程落地。
- **商汤**：通用智能体 / Agent Harness；强调多模态 + GUI Agent + 多 Agent 协作数据。

### 6.3 答题框架（STAR + 数字）
每道题用「情境 → 任务 → 行动 → 结果（带上面固定数字）」收口；把作品集项目当万能案例库，按厂 hook 切换侧重点。

---

## 七、官方招聘入口（一键投递 · 20 厂）

| 公司 | 招聘入口 | 方向 |
|------|----------|------|
| 字节 Seed | https://jobs.bytedance.com/ | 大模型 Agent 框架 / AI 搜索 |
| 腾讯混元 | https://careers.tencent.com/ | 混元 Agent 应用开发 |
| **智谱 GLM** | https://zhipu-ai.jobs.feishu.cn/ | GLM Agent / 后训练 |
| Kimi | https://careers.kimi.com/ | 推理框架 / Agent |
| **DeepSeek** | https://talent.deepseek.com/ | 大模型全栈 / 算法 |
| 京东 | https://zhaopin.jd.com/ | AI Agent 产品经理 |
| 快手 | https://zhaopin.kuaishou.cn/ | 大模型 Agent 研发 |
| 阶跃星辰 | https://www.stepfun.com/ | 多模态 / Agent |
| 宇树科技 | https://www.unitree.com/cn/position | 具身 Agent |
| 智元机器人 | https://www.agibot.com/ | 具身 Agent |
| 银河通用 | https://www.galbot.com/ | 具身 Agent |
| 阿里通义 | https://talent.alibaba.com/ | 通义 Agent |
| 百度 | https://talent.baidu.com/ | 文心 / 千帆 Agent |
| MiniMax | https://www.minimax.io/ | 对话 / Agent |
| **百川智能** | https://www.baichuan-ai.com/ | 行业大模型 Agent |
| **商汤** | https://www.sensetime.com/ | 多模态 Agent |
| 美团 | https://zhaopin.meituan.com/ | 本地生活 Agent |
| 星海图 | https://galaxea.zhiye.com/ | 具身 Agent |
| 星动纪元 | https://www.robotera.com/ | 具身 Agent |
| 灵初智能 | https://www.psibot.ai/careers_zh/ | 具身 Agent |

（Branch A 四厂已加粗。完整速查与分厂策略见《招聘调研与适配策略.md》。）

---

## 八、本周就能开始的 3 件事

1. 通读 [Agent-Learning-Hub](https://github.com/datawhalechina/Agent-Learning-Hub) 的 Stage 0 两篇官方指南，写那页「为什么需要 Agent + 后训练在哪」笔记。
2. 跑通一个 150 行 ReAct Agent loop（参考 Hub L1/L2），先不碰框架。
3. 在本站把「智谱GLM / DeepSeek」的后训练 / 大模型算法 JD 各存一条，作为 W1–W9 的对照基线（去「招聘情报」粘贴即结构化）。

---

## 九、落地说明

- 本站「学习路线」Tab 已内置本路线图，含 4 仓库可点击卡片、三大技术栈、每周可点击资源、20 厂官方招聘入口，并实时拉取 Branch A 四厂对口岗位（调用 `/api/jd` 过滤）。
- 路线依据本站 65 条真实情报 + 4 个开源仓库设计；对口岗位随情报库更新而动态变化。
- 若转投平台工程线（分支 B 具身智能 / 平台应用），可在站内另建视图，复用同一套 Stage 框架。
