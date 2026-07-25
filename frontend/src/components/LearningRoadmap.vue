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

// 10 周路线图（Branch A：算法 / 后训练 / RL，映射 datawhalechina/Agent-Learning-Hub 的 Stage 体系）
// 每条都锚定你站里的真实对口岗位
const weeks = [
  {
    w: 'W0', stage: 'Stage 0 · 认知对齐',
    focus: '为什么大模型需要 Agent；后训练如何把 Agent 能力"固化"进模型（SFT→RL 的数据飞轮）。建立「Agent vs Workflow」边界认知。',
    deliver: '一页笔记：Agent 与 Workflow 的边界 + 后训练在 Agent 闭环里的位置（面试必问）',
    post: ['全部（面试必问）'],
    res: 'Anthropic / OpenAI 官方 Agent 指南；Agent-Learning-Hub Stage 0',
  },
  {
    w: 'W1–2', stage: 'Stage 1 · 最小 Loop + ReAct',
    focus: '从 ReAct（Thought-Action-Observation）入手，手写一个能调工具的 Agent loop，不依赖框架。理解「模型决策 ↔ 环境反馈」的最小闭环。',
    deliver: '150 行 ReAct Agent + 工具集（搜索/计算/DB），可跑通、可调试',
    post: ['DeepSeek · 大模型算法工程师（社招/杭州）', '百川智能 · 大模型算法工程师（社招/北京）'],
    res: 'ReAct 原论文；Hub L1/L2',
  },
  {
    w: 'W3', stage: 'Stage 2 · RAG & 记忆 + Reflexion',
    focus: 'Reflexion：用「自我反思」替代微调来提升 Agent；配套记忆机制。理解"轨迹→反思→改进"如何成为后续 RL 的 reward 信号雏形。',
    deliver: 'Reflexion demo（失败→反思→重试），带记忆持久化',
    post: ['商汤 · 多模态大模型算法实习生-GUI Agent（北京）'],
    res: 'Reflexion 论文；mem0',
  },
  {
    w: 'W4–5', stage: 'Stage 3 · 深读 Harness + Agent Infra',
    focus: '读 DeepSeek / Agent Harness 思路：模型如何被"用起来"产生 agentic 训练数据；搭建一个可调试的 harness，并产出自建 trajectory 数据集。',
    deliver: '可调试 harness + 一份 agentic trajectory 数据集（自建，后续喂后训练）',
    post: ['DeepSeek · Agent Harness 团队 实习（北京）', '智谱GLM · 后训练/Agent/推理 Infra（校招/北京）'],
    res: 'claw0；learn-claude-code（从 0 复刻）',
  },
  {
    w: 'W6', stage: 'Stage 4 · 多 Agent + 训练数据构造',
    focus: '多 Agent 协作产出的轨迹 → 变成 SFT/RL 训练数据（数据飞轮）。这是 Branch A 与平台工程线的分水岭：你造数据，不只是用数据。',
    deliver: '一份「多 Agent 对话 → trajectory」pipeline，可批量产出训练样本',
    post: ['智谱GLM · 27届 后训练算法工程师 实习（北京）', '商汤 · 通用智能体研究员/Agent Harness（校招/深圳）'],
    res: 'LangGraph；后训练数据管线实践',
  },
  {
    w: 'W7', stage: 'Stage 5 · Skills/MCP + 对齐入门',
    focus: '把 MCP / Skills 当作 RL 环境里"可控、可验证"的工具；入门奖励建模（reward modeling）——可验证奖励是 GRPO 的关键。',
    deliver: '一个带可验证奖励的小任务 + 手写 reward 函数',
    post: ['腾讯/字节 平台岗（差异化加分项）'],
    res: 'MCP 官方 servers；RLHF / 奖励建模教程',
  },
  {
    w: 'W8', stage: 'Stage 6/7 · 评测 + 强化学习入门（核心周）',
    focus: 'RL for LLM 主线：SFT → RM → RLHF(PPO) → DPO → GRPO。自写一个 GRPO 训练 loop（小模型即可），配 20+ 任务 eval 表（成功率 / 失败分类）。',
    deliver: '一个可跑的 GRPO 训练脚本（小模型）+ eval 表（成功率/失败分类）',
    post: ['智谱GLM / DeepSeek · 后训练岗', '全部大模型算法岗'],
    res: 'DPO / GRPO 论文；TRL (Transformer Reinforcement Learning)；OpenAI Evals',
  },
  {
    w: 'W9', stage: 'Stage 8 · Ship',
    focus: '把前 8 周的产出拼成「Agent + 后训练」作品集项目（Production 级、可 clone 跑），简历核心资产。',
    deliver: '作品集核心 repo（ReAct + Reflexion + trajectory→后训练 + GRPO 闭环）',
    post: ['投递时直接展示，对应各厂后训练/Agent 职责'],
    res: '复用前 8 周所有产出',
  },
  {
    w: 'W10', stage: '冲刺 · 对标投递',
    focus: '用站里 Branch A 12 条情报筛目标厂，写简历 bullet，锚定"后训练/Agent/推理 Infra"关键词。',
    deliver: '简历定稿（含固定数字资产：GRPO 成功率、trajectory 规模、eval 指标）',
    post: ['智谱GLM / DeepSeek / 百川智能 / 商汤'],
    res: '你自己的 bigtech 站 · 招聘情报（仅社招/实习筛选）',
  },
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
        路线映射自 <a href="https://github.com/datawhalechina/Agent-Learning-Hub" target="_blank" rel="noopener">datawhalechina/Agent-Learning-Hub</a>（9 Stage + 11 级项目阶梯），
        每周对口岗位均来自本站的真实招聘情报。
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
    <div class="section-title">10 周路线图（每周对标真实岗位）</div>
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
          <div class="wk-row"><span class="k">资源</span><span class="v res">{{ wk.res }}</span></div>
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

    <!-- 本周就能开始 -->
    <div class="panel" style="margin-top:22px;">
      <h2>本周就能开始的 3 件事</h2>
      <ol class="start">
        <li>通读 Agent-Learning-Hub 的 Stage 0 两篇官方指南，写那页「为什么需要 Agent + 后训练在哪」笔记。</li>
        <li>跑通一个 150 行 ReAct Agent loop（参考 Hub L1/L2），先不碰框架。</li>
        <li>在本站把「智谱GLM / DeepSeek」的后训练 / 大模型算法 JD 各存一条，作为 W1–W9 的对照基线（去「招聘情报」粘贴即结构化）。</li>
      </ol>
    </div>

    <p class="footer-note">
      完整版路线已存档 <code>docs/agent-learning-roadmap.md</code>。路线依据本站 65 条真实情报 + Agent-Learning-Hub 课程结构设计；对口岗位随情报库更新而动态变化。
    </p>
  </div>
</template>

<style scoped>
.signal { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 16px; }
.sig { flex: 1; min-width: 90px; border: 1px solid var(--border); border-radius: 12px; padding: 12px 14px; background: #f8fafc; text-align: center; }
.sig .sv { font-size: 26px; font-weight: 800; }
.sig .sl { font-size: 12px; color: var(--muted); margin-top: 2px; }
.hint { font-size: 12.5px; color: #475569; line-height: 1.6; margin: 14px 0 0; background: #f8fbff; border-left: 3px solid var(--accent); padding: 8px 12px; border-radius: 6px; }

.why { margin: 0; padding-left: 20px; line-height: 1.8; color: #334155; font-size: 14px; }
.why li { margin-bottom: 8px; }

.roadmap { display: flex; flex-direction: column; gap: 14px; margin-top: 6px; }
.week { display: flex; gap: 14px; background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius); box-shadow: var(--shadow); overflow: hidden; }
.wk-bar {
  flex: 0 0 84px; display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 15px; color: #fff;
  background: linear-gradient(180deg, var(--tier3-a), var(--tier3-b));
  writing-mode: horizontal-tb;
}
.week:nth-child(even) .wk-bar { background: linear-gradient(180deg, var(--primary), var(--accent)); }
.wk-body { flex: 1; padding: 16px 18px; }
.wk-stage { font-weight: 800; color: var(--primary); font-size: 14px; margin-bottom: 6px; }
.wk-focus { font-size: 13.5px; color: #334155; line-height: 1.7; margin-bottom: 10px; }
.wk-row { display: flex; gap: 10px; font-size: 13px; margin-top: 6px; align-items: flex-start; }
.wk-row .k { flex: 0 0 56px; color: var(--muted); font-weight: 700; }
.wk-row .v { flex: 1; color: #334155; line-height: 1.6; }
.wk-row .v.res { color: var(--primary); }
.wk-row .tag { margin: 0 6px 4px 0; }

.jd-meta { display: flex; align-items: center; gap: 8px; margin: 10px 0 6px; flex-wrap: wrap; }
.jd-meta .m { font-size: 13px; color: var(--muted); }
.jt { font-size: 12px; font-weight: 700; padding: 2px 9px; border-radius: 6px; }
.jt.urgent { background: #fee2e2; color: #dc2626; }
.jt.social { background: #f1f5f9; color: #475569; }
.jt.intern { background: #ecfdf5; color: #059669; }
.jt.campus { background: #eff6ff; color: #2563eb; }
.jd-salary { font-size: 15px; font-weight: 800; color: #0f172a; margin: 4px 0; }
.jd-actions { display: flex; gap: 10px; align-items: center; margin-top: 8px; }
.jd-actions .lk { color: var(--primary); font-weight: 700; font-size: 12.5px; text-decoration: none; }
.jd-actions .nolink { font-size: 12px; color: #b45309; background: #fffbeb; border: 1px solid #fde68a; padding: 2px 8px; border-radius: 6px; }

.start { margin: 0; padding-left: 22px; line-height: 1.9; color: #334155; font-size: 14px; }
.start li { margin-bottom: 8px; }
.footer-note { font-size: 12.5px; color: var(--muted); margin-top: 22px; line-height: 1.7; }
.footer-note code { background: #f1f5f9; padding: 1px 6px; border-radius: 5px; color: var(--primary); }
</style>
