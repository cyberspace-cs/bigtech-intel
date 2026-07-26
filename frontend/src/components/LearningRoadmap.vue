<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../api.js'

// Branch A 目标厂（来自 bigtech 站 20 厂跟踪名单，对应 算法/后训练/RL 主线）
const branchA = ['智谱GLM', 'DeepSeek', '百川智能', '商汤']
const loading = ref(false)
const livePostings = ref([])

// 需求信号（来自 bigtech 站真实 65 条情报的关键词统计，决定主线权重）
const signal = [
  { k: 'Agent', v: 168, c: '#1d4ed8' },
  { k: '算法', v: 70, c: '#0ea5e9' },
  { k: '后训练', v: 8, c: '#7c3aed' },
  { k: '预训练', v: 3, c: '#7c3aed' },
  { k: 'GRPO/DPO', v: 4, c: '#a855f7' },
  { k: '强化', v: 2, c: '#a855f7' },
]

// 4 个可点击学习仓库
const repos = [
  {
    name: 'Agent-Learning-Hub',
    org: 'datawhalechina',
    url: 'https://github.com/datawhalechina/Agent-Learning-Hub',
    desc: '9 个 Stage（认知→最小 Loop→RAG/记忆→Harness→多 Agent→Skills/MCP→评测→Ship）+ 11 级项目阶梯。Agent 应用开发主线权威路径。',
    tags: ['Stage 0-8', '11 级项目阶梯', 'Agent 工程'],
  },
  {
    name: 'AgentGuide · 算法路线图',
    org: 'cyberspace-cs',
    url: 'https://github.com/cyberspace-cs/AgentGuide/blob/main/docs/05-roadmaps/learning-roadmap-algorithm.md',
    desc: '9 周研究型 AI Agent 算法工程师路线：Transformer 手撕 → ReAct/Reflexion/ToT → RAG 算法 → Memory → RL/DPO/GRPO → 论文/开源产出。Branch A 算法主线。',
    tags: ['9 周算法路线', 'RL/DPO/GRPO', '论文产出'],
  },
  {
    name: 'diy-llm',
    org: 'datawhalechina',
    url: 'https://github.com/datawhalechina/diy-llm',
    desc: 'CS336 中文版（15 章 + 6 作业）。含第 10 章「推理」(KV Cache/投机解码/量化 GPTQ·AWQ/PagedAttention/Continuous Batching)、第 13 章训练流程(Pre-training/SFT/DPO/RLHF PPO)、第 14 章可验证奖励 RL(GRPO/RLVR/R1)。推理优化 + 后训练硬核教材。',
    tags: ['CS336 中文', '推理优化 Ch10', '后训练 Ch13/14'],
  },
  {
    name: 'llm-algo-leetcode',
    org: 'datawhalechina',
    url: 'https://github.com/datawhalechina/llm-algo-leetcode',
    desc: 'PyTorch 算法实战 + Triton + CUDA。覆盖 Transformer/Attention/KV Cache/PagedAttention/对齐/微调/分布式/显存/推理优化，底层算子与面试算法题首选。',
    tags: ['PyTorch 实战', 'Triton/CUDA', '推理优化专题'],
  },
]

// 三大技术栈（Agent 开发 / 算法 / 大模型推理优化），每条带可点击链接
const stacks = [
  {
    key: 'agent',
    title: 'Agent 开发技术栈',
    color: '#1d4ed8',
    desc: '把「模型决策 ↔ 环境反馈」做成可落地、可观测、可评测的系统。',
    items: [
      { t: '编排框架', links: [
        { l: 'LangGraph', u: 'https://langchain-ai.github.io/langgraph/' },
        { l: 'hello-agents (datawhale)', u: 'https://github.com/datawhalechina/hello-agents' },
        { l: 'claw0', u: 'https://github.com/shareAI-lab/claw0' },
        { l: 'learn-claude-code', u: 'https://github.com/shareAI-lab/learn-claude-code' },
      ] },
      { t: '工具 / MCP', links: [
        { l: 'Model Context Protocol', u: 'https://modelcontextprotocol.io/' },
        { l: 'MCP Servers', u: 'https://github.com/modelcontextprotocol/servers' },
        { l: 'Claude Code Skills', u: 'https://code.claude.com/docs/en/skills' },
      ] },
      { t: 'RAG / 记忆', links: [
        { l: 'mem0', u: 'https://github.com/mem0ai/mem0' },
        { l: 'Letta', u: 'https://github.com/letta-ai/letta' },
        { l: 'RAGFlow', u: 'https://github.com/infiniflow/ragflow' },
        { l: 'LlamaIndex', u: 'https://docs.llamaindex.ai/en/stable/use_cases/agents/' },
      ] },
      { t: '多 Agent / 协议', links: [
        { l: 'Claude Subagents', u: 'https://code.claude.com/docs/en/sub-agents' },
        { l: 'A2A Protocol', u: 'https://a2a-protocol.org/latest/specification/' },
        { l: 'Agent Client Protocol', u: 'https://agentclientprotocol.com/' },
      ] },
      { t: '评测 / 可观测', links: [
        { l: 'OpenAI Evals', u: 'https://platform.openai.com/docs/guides/evals' },
        { l: 'SWE-bench', u: 'https://arxiv.org/abs/2310.06770' },
        { l: 'LangSmith', u: 'https://docs.smith.langchain.com/' },
        { l: 'AgentBench', u: 'https://arxiv.org/abs/2308.03688' },
      ] },
      { t: '必读范式', links: [
        { l: 'Anthropic: Building effective agents', u: 'https://www.anthropic.com/engineering/building-effective-agents' },
        { l: 'OpenAI: Practical guide', u: 'https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/' },
        { l: 'GPT Researcher', u: 'https://github.com/assafelovic/gpt-researcher' },
      ] },
    ],
  },
  {
    key: 'algo',
    title: '算法技术栈（Branch A 主线）',
    color: '#7c3aed',
    desc: '从 Transformer 手撕到后训练对齐（SFT/DPO/GRPO），把 Agent 能力固化进模型。',
    items: [
      { t: '基础 / 架构', links: [
        { l: 'nanoGPT (Karpathy)', u: 'https://github.com/karpathy/nanoGPT' },
        { l: 'LLMs from scratch', u: 'https://github.com/rasbt/LLMs-from-scratch' },
        { l: 'Attention Is All You Need', u: 'https://arxiv.org/abs/1706.03762' },
        { l: 'llm-algo-leetcode · Transformer', u: 'https://github.com/datawhalechina/llm-algo-leetcode' },
      ] },
      { t: 'Agent 算法', links: [
        { l: 'ReAct', u: 'https://arxiv.org/abs/2210.03629' },
        { l: 'Reflexion', u: 'https://arxiv.org/abs/2303.11366' },
        { l: 'Tree of Thoughts', u: 'https://arxiv.org/abs/2305.10601' },
        { l: 'AgentGuide 算法路线', u: 'https://github.com/cyberspace-cs/AgentGuide/blob/main/docs/05-roadmaps/learning-roadmap-algorithm.md' },
      ] },
      { t: 'RAG 算法', links: [
        { l: 'BM25 / DPR', u: 'https://arxiv.org/abs/2004.04906' },
        { l: 'Self-RAG', u: 'https://arxiv.org/abs/2310.11511' },
        { l: 'GraphRAG', u: 'https://www.microsoft.com/en-us/research/project/graphrag/' },
        { l: 'RAGAs', u: 'https://github.com/explodinggradients/ragas' },
      ] },
      { t: '记忆 / 上下文工程', links: [
        { l: 'MemGPT', u: 'https://arxiv.org/abs/2310.08560' },
        { l: 'Generative Agents', u: 'https://arxiv.org/abs/2304.03442' },
        { l: 'diy-llm Ch5 MoE', u: 'https://github.com/datawhalechina/diy-llm' },
      ] },
      { t: '后训练 / 对齐', links: [
        { l: 'LLaMA-Factory (SFT/LoRA)', u: 'https://github.com/hiyouga/LLaMA-Factory' },
        { l: 'TRL (DPO/GRPO)', u: 'https://github.com/huggingface/trl' },
        { l: 'OpenRLHF (PPO)', u: 'https://github.com/OpenLLMAI/OpenRLHF' },
        { l: 'diy-llm Ch13/14', u: 'https://github.com/datawhalechina/diy-llm' },
      ] },
      { t: '评估 / 对齐基准', links: [
        { l: 'lm-evaluation-harness', u: 'https://github.com/EleutherAI/lm-evaluation-harness' },
        { l: 'OpenCompass', u: 'https://github.com/open-compass/opencompass' },
        { l: 'DPO 论文', u: 'https://arxiv.org/abs/2305.18290' },
        { l: 'GRPO 论文', u: 'https://arxiv.org/pdf/2402.03300' },
        { l: 'DeepSeek-R1', u: 'https://github.com/deepseek-ai/DeepSeek-R1' },
      ] },
    ],
  },
  {
    key: 'infer',
    title: '大模型推理优化技术栈',
    color: '#0ea5e9',
    desc: '降本提吞吐：量化 / 蒸馏 / KV Cache / 投机解码 / 推理框架，直接对标本站推理优化岗。',
    items: [
      { t: '推理框架', links: [
        { l: 'vLLM (PagedAttention)', u: 'https://github.com/vllm-project/vllm' },
        { l: 'SGLang (radix cache)', u: 'https://github.com/sgl-project/sglang' },
        { l: 'diy-llm Ch10 推理', u: 'https://github.com/datawhalechina/diy-llm' },
      ] },
      { t: '量化', links: [
        { l: 'GPTQ', u: 'https://arxiv.org/abs/2210.17323' },
        { l: 'AWQ', u: 'https://arxiv.org/abs/2306.00978' },
        { l: 'Unsloth', u: 'https://github.com/unslothai/unsloth' },
        { l: 'llm-algo-leetcode 推理优化', u: 'https://github.com/datawhalechina/llm-algo-leetcode' },
      ] },
      { t: 'KV Cache / 注意力', links: [
        { l: 'PagedAttention', u: 'https://github.com/vllm-project/vllm' },
        { l: 'FlashAttention', u: 'https://arxiv.org/abs/2205.14135' },
        { l: 'MQA/GQA', u: 'https://arxiv.org/abs/2305.13245' },
        { l: 'diy-llm Ch6 GPU 优化', u: 'https://github.com/datawhalechina/diy-llm' },
      ] },
      { t: '投机解码', links: [
        { l: 'Speculative Decoding', u: 'https://arxiv.org/abs/2211.17192' },
        { l: 'diy-llm Ch10', u: 'https://github.com/datawhalechina/diy-llm' },
      ] },
      { t: '上下文压缩 / 蒸馏', links: [
        { l: 'LLMLingua', u: 'https://github.com/microsoft/LLMLingua' },
        { l: '知识蒸馏 KD', u: 'https://arxiv.org/abs/1503.02531' },
        { l: 'nanochat (Karpathy)', u: 'https://github.com/karpathy/nanochat' },
      ] },
      { t: '工程落地参考', links: [
        { l: '本项目 inference.py 实战', u: 'https://github.com/cyberspace-cs/personal-portfolio' },
        { l: 'Continuous Batching', u: 'https://github.com/vllm-project/vllm' },
      ] },
    ],
  },
]

// 10 周路线图（Branch A），每条资源可点击
const weeks = [
  {
    w: 'W0', stage: 'Stage 0 · 认知对齐',
    focus: '为什么大模型需要 Agent；后训练如何把 Agent 能力"固化"进模型（SFT→RL 的数据飞轮）。建立「Agent vs Workflow」边界认知。',
    deliver: '一页笔记：Agent 与 Workflow 的边界 + 后训练在 Agent 闭环里的位置（面试必问）',
    post: ['全部（面试必问）'],
    links: [
      { l: 'Anthropic: Building effective agents', u: 'https://www.anthropic.com/engineering/building-effective-agents' },
      { l: 'OpenAI: Practical guide', u: 'https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/' },
      { l: 'Agent-Learning-Hub Stage 0', u: 'https://github.com/datawhalechina/Agent-Learning-Hub' },
    ],
  },
  {
    w: 'W1–2', stage: 'Stage 1 · 最小 Loop + ReAct',
    focus: '从 ReAct（Thought-Action-Observation）入手，手写一个能调工具的 Agent loop，不依赖框架。理解「模型决策 ↔ 环境反馈」的最小闭环。',
    deliver: '150 行 ReAct Agent + 工具集（搜索/计算/DB），可跑通、可调试',
    post: ['DeepSeek · 大模型算法工程师（社招/杭州）', '百川智能 · 大模型算法工程师（社招/北京）'],
    links: [
      { l: 'ReAct 原论文', u: 'https://arxiv.org/abs/2210.03629' },
      { l: 'Hub L1/L2 最小 Loop', u: 'https://github.com/datawhalechina/Agent-Learning-Hub' },
      { l: 'OpenAI Function Calling', u: 'https://platform.openai.com/docs/guides/function-calling' },
    ],
  },
  {
    w: 'W3', stage: 'Stage 2 · RAG & 记忆 + Reflexion',
    focus: 'Reflexion：用「自我反思」替代微调来提升 Agent；配套记忆机制。理解"轨迹→反思→改进"如何成为后续 RL 的 reward 信号雏形。',
    deliver: 'Reflexion demo（失败→反思→重试），带记忆持久化',
    post: ['商汤 · 多模态大模型算法实习生-GUI Agent（北京）'],
    links: [
      { l: 'Reflexion 论文', u: 'https://arxiv.org/abs/2303.11366' },
      { l: 'mem0 记忆', u: 'https://github.com/mem0ai/mem0' },
      { l: 'Hub Stage 2 RAG/记忆', u: 'https://github.com/datawhalechina/Agent-Learning-Hub' },
    ],
  },
  {
    w: 'W4–5', stage: 'Stage 3 · 深读 Harness + Agent Infra',
    focus: '读 DeepSeek / Agent Harness 思路：模型如何被"用起来"产生 agentic 训练数据；搭建一个可调试的 harness，并产出自建 trajectory 数据集。',
    deliver: '可调试 harness + 一份 agentic trajectory 数据集（自建，后续喂后训练）',
    post: ['DeepSeek · Agent Harness 团队 实习（北京）', '智谱GLM · 后训练/Agent/推理 Infra（校招/北京）'],
    links: [
      { l: 'claw0', u: 'https://github.com/shareAI-lab/claw0' },
      { l: 'learn-claude-code', u: 'https://github.com/shareAI-lab/learn-claude-code' },
      { l: 'Hub Stage 3 Harness', u: 'https://github.com/datawhalechina/Agent-Learning-Hub' },
    ],
  },
  {
    w: 'W6', stage: 'Stage 4 · 多 Agent + 训练数据构造',
    focus: '多 Agent 协作产出的轨迹 → 变成 SFT/RL 训练数据（数据飞轮）。这是 Branch A 与平台工程线的分水岭：你造数据，不只是用数据。',
    deliver: '一份「多 Agent 对话 → trajectory」pipeline，可批量产出训练样本',
    post: ['智谱GLM · 27届 后训练算法工程师 实习（北京）', '商汤 · 通用智能体研究员/Agent Harness（校招/深圳）'],
    links: [
      { l: 'LangGraph', u: 'https://langchain-ai.github.io/langgraph/' },
      { l: 'Claude Subagents', u: 'https://code.claude.com/docs/en/sub-agents' },
      { l: 'AgentGuide 多 Agent 周', u: 'https://github.com/cyberspace-cs/AgentGuide/blob/main/docs/05-roadmaps/learning-roadmap-algorithm.md' },
    ],
  },
  {
    w: 'W7', stage: 'Stage 5 · Skills/MCP + 对齐入门',
    focus: '把 MCP / Skills 当作 RL 环境里"可控、可验证"的工具；入门奖励建模（reward modeling）——可验证奖励是 GRPO 的关键。',
    deliver: '一个带可验证奖励的小任务 + 手写 reward 函数',
    post: ['腾讯/字节 平台岗（差异化加分项）'],
    links: [
      { l: 'Model Context Protocol', u: 'https://modelcontextprotocol.io/' },
      { l: 'AgentGuide 对齐/RL 周', u: 'https://github.com/cyberspace-cs/AgentGuide/blob/main/docs/05-roadmaps/learning-roadmap-algorithm.md' },
      { l: 'RLHF 奖励建模', u: 'https://github.com/OpenLLMAI/OpenRLHF' },
    ],
  },
  {
    w: 'W8', stage: 'Stage 6/7 · 评测 + 强化学习入门（核心周）',
    focus: 'RL for LLM 主线：SFT → RM → RLHF(PPO) → DPO → GRPO。自写一个 GRPO 训练 loop（小模型即可），配 20+ 任务 eval 表（成功率 / 失败分类）。',
    deliver: '一个可跑的 GRPO 训练脚本（小模型）+ eval 表（成功率/失败分类）',
    post: ['智谱GLM / DeepSeek · 后训练岗', '全部大模型算法岗'],
    links: [
      { l: 'DPO 论文', u: 'https://arxiv.org/abs/2305.18290' },
      { l: 'GRPO 论文', u: 'https://arxiv.org/pdf/2402.03300' },
      { l: 'TRL (Transformer RL)', u: 'https://github.com/huggingface/trl' },
      { l: 'diy-llm Ch13/14', u: 'https://github.com/datawhalechina/diy-llm' },
      { l: 'OpenAI Evals', u: 'https://platform.openai.com/docs/guides/evals' },
    ],
  },
  {
    w: 'W9', stage: 'Stage 8 · Ship',
    focus: '把前 8 周的产出拼成「Agent + 后训练」作品集项目（Production 级、可 clone 跑），简历核心资产。',
    deliver: '作品集核心 repo（ReAct + Reflexion + trajectory→后训练 + GRPO 闭环）',
    post: ['投递时直接展示，对应各厂后训练/Agent 职责'],
    links: [
      { l: 'Hub Stage 8 Ship', u: 'https://github.com/datawhalechina/Agent-Learning-Hub' },
      { l: '11 级项目阶梯 L11', u: 'https://github.com/datawhalechina/Agent-Learning-Hub' },
    ],
  },
  {
    w: 'W10', stage: '冲刺 · 对标投递',
    focus: '用站里 Branch A 12 条情报筛目标厂，写简历 bullet，锚定"后训练/Agent/推理 Infra"关键词。',
    deliver: '简历定稿（含固定数字资产：GRPO 成功率、trajectory 规模、eval 指标）',
    post: ['智谱GLM / DeepSeek / 百川智能 / 商汤'],
    links: [
      { l: '本站招聘情报', u: 'http://localhost:8031/#/recruit' },
    ],
  },
]

// 官方招聘入口（可点击，来自《招聘调研与适配策略》速查表）
const jobLinks = [
  { c: '字节 Seed', u: 'https://jobs.bytedance.com/', t: '大模型 Agent 框架 / AI 搜索' },
  { c: '腾讯混元', u: 'https://careers.tencent.com/', t: '混元 Agent 应用开发' },
  { c: '智谱 GLM', u: 'https://zhipu-ai.jobs.feishu.cn/', t: 'GLM Agent / 后训练' },
  { c: 'Kimi', u: 'https://careers.kimi.com/', t: '推理框架 / Agent' },
  { c: 'DeepSeek', u: 'https://talent.deepseek.com/', t: '大模型全栈 / 算法' },
  { c: '京东', u: 'https://zhaopin.jd.com/', t: 'AI Agent 产品经理' },
  { c: '快手', u: 'https://zhaopin.kuaishou.cn/', t: '大模型 Agent 研发' },
  { c: '阶跃星辰', u: 'https://www.stepfun.com/', t: '多模态 / Agent' },
  { c: '宇树科技', u: 'https://www.unitree.com/cn/position', t: '具身 Agent' },
  { c: '智元机器人', u: 'https://www.agibot.com/', t: '具身 Agent' },
  { c: '银河通用', u: 'https://www.galbot.com/', t: '具身 Agent' },
  { c: '阿里通义', u: 'https://talent.alibaba.com/', t: '通义 Agent' },
  { c: '百度', u: 'https://talent.baidu.com/', t: '文心 / 千帆 Agent' },
  { c: 'MiniMax', u: 'https://www.minimax.io/', t: '对话 / Agent' },
  { c: '百川智能', u: 'https://www.baichuan-ai.com/', t: '行业大模型 Agent' },
  { c: '商汤', u: 'https://www.sensetime.com/', t: '多模态 Agent' },
  { c: '美团', u: 'https://zhaopin.meituan.com/', t: '本地生活 Agent' },
  { c: '星海图', u: 'https://galaxea.zhiye.com/', t: '具身 Agent' },
  { c: '星动纪元', u: 'https://www.robotera.com/', t: '具身 Agent' },
  { c: '灵初智能', u: 'https://www.psibot.ai/careers_zh/', t: '具身 Agent' },
]

// 静态兜底对口岗位（与实时拉取一致；API 失败时用）
const fallbackPostings = [
  { company: '智谱GLM', jtype: 4, title: '校招 后训练/Agent/推理 Infra', city: '北京' },
  { company: '智谱GLM', jtype: 3, title: '27届 后训练算法工程师 实习', city: '北京' },
  { company: 'DeepSeek', jtype: 2, title: '大模型算法工程师 社招', city: '杭州' },
  { company: 'DeepSeek', jtype: 3, title: 'Agent Harness 团队 实习', city: '北京' },
  { company: 'DeepSeek', jtype: 2, title: '研究员/工程师 扩招（全岗）', city: '杭州' },
  { company: '百川智能', jtype: 3, title: '大模型算法工程师 实习', city: '北京' },
  { company: '百川智能', jtype: 2, title: '大模型算法工程师 社招', city: '北京' },
  { company: '商汤', jtype: 3, title: '多模态大模型算法实习生-GUI Agent', city: '北京' },
  { company: '商汤', jtype: 4, title: '2026 校招 通用智能体研究员/Agent Harness', city: '深圳' },
  { company: '商汤', jtype: 3, title: 'AI 先锋 顶尖实习生', city: '上海' },
]

const jtypeLabel = (j) => (j === 1 ? '急招' : j === 3 ? '实习' : j === 4 ? '校招' : '社招')
const jtypeClass = (j) => (j === 1 ? 'urgent' : j === 3 ? 'intern' : j === 4 ? 'campus' : 'social')

onMounted(async () => {
  loading.value = true
  try {
    const all = await api.jdList(0, 0, '')
    livePostings.value = all.filter((r) => branchA.includes(r.company))
  } catch (e) {
    livePostings.value = []
  } finally {
    loading.value = false
  }
})

const postings = computed(() => (livePostings.value.length ? livePostings.value : fallbackPostings))
</script>

<template>
  <div>
    <!-- 概览 -->
    <div class="panel">
      <h2>Agent 学习路线 · 分支 A（算法 / 后训练 / RL）</h2>
      <p class="desc">
        面向 <b>工作 1 年的社招</b>选手。主线 = <b>Agent 应用开发 → 后训练把能力固化进模型 → RL（GRPO/DPO）对齐</b>，
        目标厂锁定 <b>智谱GLM / DeepSeek / 百川智能 / 商汤</b> 的算法 / 后训练 / Agent 岗。
        路线综合自 4 个开源仓库，每周对口岗位均来自本站的真实招聘情报。
      </p>

      <!-- 需求信号条 -->
      <div class="signal">
        <div class="sig" v-for="s in signal" :key="s.k">
          <div class="sv" :style="{ color: s.c }">{{ s.v }}</div>
          <div class="sl">{{ s.k }}</div>
        </div>
        <div class="sig">
          <div class="sv" style="color:#7c3aed">12</div>
          <div class="sl">Branch A 真实情报</div>
        </div>
      </div>
      <p class="hint">数据来自本站 65 条招聘情报的关键词统计：「后训练 / GRPO / DPO / 预训练 / 强化」集中出现在 Branch A 四厂 JD，是 1 年经验最值得追加投入的差异化方向。</p>
    </div>

    <!-- 4 个学习仓库（可点击） -->
    <div class="section-title">📚 学习资源库（4 个可点击仓库）</div>
    <div class="repo-grid">
      <a v-for="r in repos" :key="r.url" class="repo" :href="r.url" target="_blank" rel="noopener">
        <div class="repo-head">
          <span class="repo-name">{{ r.name }}</span>
          <span class="repo-org">{{ r.org }}</span>
        </div>
        <div class="repo-desc">{{ r.desc }}</div>
        <div class="repo-tags">
          <span v-for="(t, i) in r.tags" :key="i" class="chip">{{ t }}</span>
        </div>
        <div class="repo-go">打开仓库 ↗</div>
      </a>
    </div>

    <!-- 三大技术栈 -->
    <div class="section-title">🧱 三大技术栈（Agent 开发 / 算法 / 推理优化）</div>
    <div class="stacks">
      <div v-for="s in stacks" :key="s.key" class="stack" :style="{ borderTopColor: s.color }">
        <h3 :style="{ color: s.color }">{{ s.title }}</h3>
        <p class="stack-desc">{{ s.desc }}</p>
        <div v-for="(g, gi) in s.items" :key="gi" class="stack-g">
          <span class="stack-gt">{{ g.t }}</span>
          <span class="stack-links">
            <a v-for="(lk, li) in g.links" :key="li" class="lk2" :href="lk.u" target="_blank" rel="noopener">{{ lk.l }} ↗</a>
          </span>
        </div>
      </div>
    </div>

    <!-- 为什么选 Branch A -->
    <div class="panel" style="margin-top:22px;">
      <h2>为什么走分支 A（而非平台工程线）</h2>
      <ul class="why">
        <li><b>壁垒更高：</b>后训练 / RL 是算法岗硬通货，1 年社招卷平台工程线容易和应届 flooded，卷后训练/RL 反而有稀缺性。</li>
        <li><b>对口明确：</b>智谱（后训练/Agent/推理 Infra）、DeepSeek（大模型算法/Agent Harness）、百川（大模型算法）、商汤（通用智能体/Agent Harness）均在招。</li>
        <li><b>作品可量化：</b>GRPO 成功率、自建 trajectory 规模、eval 指标——都是简历里能写死的"数字资产"。</li>
      </ul>
    </div>

    <!-- 10 周路线图 -->
    <div class="section-title">10 周路线图（每周对标真实岗位 + 可点击资源）</div>
    <div class="roadmap">
      <div class="week" v-for="(wk, i) in weeks" :key="i">
        <div class="wk-bar">{{ wk.w }}</div>
        <div class="wk-body">
          <div class="wk-stage">{{ wk.stage }}</div>
          <div class="wk-focus">{{ wk.focus }}</div>
          <div class="wk-row"><span class="k">交付物</span><span class="v">{{ wk.deliver }}</span></div>
          <div class="wk-row"><span class="k">对口岗位</span><span class="v">
            <span v-for="(p, j) in wk.post" :key="j" class="tag blue">{{ p }}</span>
          </span></div>
          <div class="wk-row"><span class="k">资源</span><span class="v links">
            <a v-for="(lk, j) in wk.links" :key="j" class="lk2" :href="lk.u" target="_blank" rel="noopener">{{ lk.l }} ↗</a>
          </span></div>
        </div>
      </div>
    </div>

    <!-- 对口岗位（实时） -->
    <div class="panel" style="margin-top:24px;">
      <h2>对口岗位（实时 · 来自招聘情报）</h2>
      <p class="desc">下列为 Branch A 四厂在本站招聘情报中的真实条目；点导航「招聘情报 → 仅社招/实习」可看完整 JD 与链接。</p>
      <p v-if="loading" class="empty">加载中…</p>
      <div class="grid" v-else>
        <div v-for="(r, i) in postings" :key="i" class="card" :class="r.tier === 2 ? 't2' : r.tier === 3 ? 't3' : ''">
          <div class="head">
            <div class="name">{{ r.company }}</div>
            <span class="tier-tag">{{ r.tier === 2 ? '第二梯队' : r.tier === 3 ? '第三梯队' : '通用' }}</span>
          </div>
          <div class="jd-meta">
            <span class="jt" :class="jtypeClass(r.jtype)">{{ jtypeLabel(r.jtype) }}</span>
            <span v-if="r.city" class="m">{{ r.city }}</span>
          </div>
          <div class="dir">{{ r.title }}</div>
          <div v-if="r.salary" class="jd-salary">{{ r.salary }}</div>
          <div class="jd-actions">
            <a v-if="r.url" class="lk" :href="r.url" target="_blank" rel="noopener">查看原帖 ↗</a>
            <span v-else class="nolink">前往「招聘情报」看链接</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 官方招聘入口（可点击） -->
    <div class="panel" style="margin-top:22px;">
      <h2>官方招聘入口（一键投递 · 20 厂）</h2>
      <p class="desc">来自《招聘调研与适配策略》速查表，全部可点击直达官网招聘页。Branch A 四厂已加粗。</p>
      <div class="job-grid">
        <a v-for="(j, i) in jobLinks" :key="i" class="job" :href="j.u" target="_blank" rel="noopener"
           :class="['智谱 GLM','DeepSeek','百川智能','商汤'].includes(j.c) ? 'hot' : ''">
          <span class="job-c">{{ j.c }}</span>
          <span class="job-t">{{ j.t }}</span>
          <span class="job-go">↗</span>
        </a>
      </div>
    </div>

    <!-- 本周就能开始 -->
    <div class="panel" style="margin-top:22px;">
      <h2>本周就能开始的 3 件事</h2>
      <ol class="start">
        <li>通读 <a href="https://github.com/datawhalechina/Agent-Learning-Hub" target="_blank" rel="noopener">Agent-Learning-Hub</a> 的 Stage 0 两篇官方指南，写那页「为什么需要 Agent + 后训练在哪」笔记。</li>
        <li>跑通一个 150 行 ReAct Agent loop（参考 Hub L1/L2），先不碰框架。</li>
        <li>在本站把「智谱GLM / DeepSeek」的后训练 / 大模型算法 JD 各存一条，作为 W1–W9 的对照基线（去「招聘情报」粘贴即结构化）。</li>
      </ol>
    </div>

    <p class="footer-note">
      完整版路线已存档 <code>docs/agent-learning-roadmap.md</code>。路线依据本站 65 条真实情报 + 4 个开源仓库（Agent-Learning-Hub / AgentGuide / diy-llm / llm-algo-leetcode）设计；对口岗位随情报库更新而动态变化。
    </p>
  </div>
</template>

<style scoped>
.signal { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 16px; }
.sig { flex: 1; min-width: 90px; border: 1px solid var(--border); border-radius: 12px; padding: 12px 14px; background: #f8fafc; text-align: center; }
.sig .sv { font-size: 26px; font-weight: 800; }
.sig .sl { font-size: 12px; color: var(--muted); margin-top: 2px; }
.hint { font-size: 12.5px; color: #475569; line-height: 1.6; margin: 14px 0 0; background: #f8fbff; border-left: 3px solid var(--accent); padding: 8px 12px; border-radius: 6px; }

/* 仓库卡片 */
.repo-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; margin-top: 8px; }
.repo { display: block; text-decoration: none; border: 1px solid var(--border); border-radius: var(--radius); padding: 16px; background: var(--panel); box-shadow: var(--shadow); color: inherit; transition: transform .12s, box-shadow .12s; }
.repo:hover { transform: translateY(-2px); box-shadow: 0 8px 22px rgba(29,78,216,.14); border-color: var(--accent); }
.repo-head { display: flex; align-items: baseline; gap: 8px; }
.repo-name { font-weight: 800; color: var(--primary); font-size: 15px; }
.repo-org { font-size: 12px; color: var(--muted); }
.repo-desc { font-size: 12.8px; color: #334155; line-height: 1.65; margin: 8px 0; }
.repo-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.chip { font-size: 11px; background: #eef2ff; color: #4338ca; padding: 2px 8px; border-radius: 999px; }
.repo-go { margin-top: 10px; font-size: 12.5px; font-weight: 700; color: var(--accent); }

/* 技术栈 */
.stacks { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 8px; }
.stack { border: 1px solid var(--border); border-top: 3px solid; border-radius: var(--radius); padding: 14px 16px; background: var(--panel); box-shadow: var(--shadow); }
.stack h3 { font-size: 15px; margin: 0 0 6px; }
.stack-desc { font-size: 12.5px; color: #475569; line-height: 1.6; margin: 0 0 10px; }
.stack-g { margin-top: 8px; padding-top: 8px; border-top: 1px dashed var(--border); }
.stack-gt { display: inline-block; font-size: 12px; font-weight: 700; color: #0f172a; min-width: 92px; vertical-align: top; }
.stack-links { display: inline-flex; flex-wrap: wrap; gap: 5px 10px; max-width: calc(100% - 96px); }
.lk2 { font-size: 12px; color: var(--primary); text-decoration: none; white-space: nowrap; }
.lk2:hover { text-decoration: underline; }

.why { margin: 0; padding-left: 20px; line-height: 1.8; color: #334155; font-size: 14px; }
.why li { margin-bottom: 8px; }

.roadmap { display: flex; flex-direction: column; gap: 14px; margin-top: 6px; }
.week { display: flex; gap: 14px; background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius); box-shadow: var(--shadow); overflow: hidden; }
.wk-bar {
  flex: 0 0 84px; display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 15px; color: #fff;
  background: linear-gradient(180deg, var(--tier3-a), var(--tier3-b));
}
.week:nth-child(even) .wk-bar { background: linear-gradient(180deg, var(--primary), var(--accent)); }
.wk-body { flex: 1; padding: 16px 18px; }
.wk-stage { font-weight: 800; color: var(--primary); font-size: 14px; margin-bottom: 6px; }
.wk-focus { font-size: 13.5px; color: #334155; line-height: 1.7; margin-bottom: 10px; }
.wk-row { display: flex; gap: 10px; font-size: 13px; margin-top: 6px; align-items: flex-start; }
.wk-row .k { flex: 0 0 56px; color: var(--muted); font-weight: 700; }
.wk-row .v { flex: 1; color: #334155; line-height: 1.6; }
.wk-row .v.links { display: flex; flex-wrap: wrap; gap: 4px 10px; }
.wk-row .tag { margin: 0 6px 4px 0; }

/* 对口岗位 */
.jd-meta { display: flex; align-items: center; gap: 8px; margin: 10px 0 6px; flex-wrap: wrap; }
.jd-meta .m { font-size: 13px; color: var(--muted); }
.jt { font-size: 12px; font-weight: 700; padding: 2px 9px; border-radius: 6px; }
.jt.urgent { background: #fee2e2; color: #dc2626; }
.jt.social { background: #f1f5f9; color: #475569; }
.jt.intern { background: #ecfdf5; color: #059669; }
.jt.campus { background: #eff6ff; color: #2563eb; }
.grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.card { border: 1px solid var(--border); border-radius: 12px; padding: 14px; background: #fff; box-shadow: var(--shadow); }
.card.t2 { border-left: 3px solid var(--tier2-a); }
.card.t3 { border-left: 3px solid var(--tier3-a); }
.head { display: flex; justify-content: space-between; align-items: center; }
.name { font-weight: 800; color: #0f172a; font-size: 14px; }
.tier-tag { font-size: 11px; color: var(--muted); background: #f1f5f9; padding: 2px 7px; border-radius: 6px; }
.dir { font-size: 13px; color: #334155; margin-top: 6px; line-height: 1.5; }
.jd-salary { font-size: 15px; font-weight: 800; color: #0f172a; margin: 4px 0; }
.jd-actions { display: flex; gap: 10px; align-items: center; margin-top: 8px; }
.jd-actions .lk { color: var(--primary); font-weight: 700; font-size: 12.5px; text-decoration: none; }
.jd-actions .nolink { font-size: 12px; color: #b45309; background: #fffbeb; border: 1px solid #fde68a; padding: 2px 8px; border-radius: 6px; }

/* 官方招聘入口 */
.job-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 8px; }
.job { display: flex; align-items: center; gap: 6px; text-decoration: none; border: 1px solid var(--border); border-radius: 10px; padding: 10px 12px; background: #fff; color: inherit; transition: border-color .12s, transform .12s; }
.job:hover { border-color: var(--accent); transform: translateY(-1px); }
.job.hot { border-color: #7c3aed; background: #faf5ff; }
.job-c { font-weight: 800; font-size: 13px; color: #0f172a; }
.job-t { flex: 1; font-size: 11px; color: var(--muted); line-height: 1.3; }
.job-go { color: var(--accent); font-weight: 700; }

.start { margin: 0; padding-left: 22px; line-height: 1.9; color: #334155; font-size: 14px; }
.start li { margin-bottom: 8px; }
.footer-note { font-size: 12.5px; color: var(--muted); margin-top: 22px; line-height: 1.7; }
.footer-note code { background: #f1f5f9; padding: 1px 6px; border-radius: 5px; color: var(--primary); }
.empty { color: var(--muted); font-size: 13px; }

@media (max-width: 900px) {
  .repo-grid, .stacks, .grid, .job-grid { grid-template-columns: 1fr; }
  .job-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
