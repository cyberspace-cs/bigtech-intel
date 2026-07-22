<script setup>
import { ref, onMounted } from 'vue'
import { api } from './api.js'
import CompanyCard from './components/CompanyCard.vue'
import CompanyModal from './components/CompanyModal.vue'
import LineagePanel from './components/LineagePanel.vue'
import ResumePanel from './components/ResumePanel.vue'
import RecruitPanel from './components/RecruitPanel.vue'
import RecruitIntel from './components/RecruitIntel.vue'
import CrawlPanel from './components/CrawlPanel.vue'

const tab = ref('companies')
const q = ref('')
const tier = ref(0)
const companies = ref([])
const selected = ref(null)
const loading = ref(false)

const tabs = [
  { key: 'companies', label: '公司画像' },
  { key: 'lineage', label: '团队背景图谱' },
  { key: 'resume', label: '简历策略' },
  { key: 'recruit', label: '招聘情报' },
  { key: 'crawl', label: '爬虫 / 数据源' },
]

async function loadCompanies() {
  loading.value = true
  try {
    companies.value = await api.companies(q.value, tier.value)
  } catch (e) {
    companies.value = []
  } finally {
    loading.value = false
  }
}

function onSearch() { loadCompanies() }
function setTier(t) { tier.value = t; loadCompanies() }
function open(c) { selected.value = c }
function close() { selected.value = null }

onMounted(loadCompanies)
</script>

<template>
  <header class="topbar">
    <div class="logo">大厂情报站 <small>AI 大模型厂求职参谋</small></div>
    <div class="spacer"></div>
    <div class="meta">实习 / 校招 / 社招 · 产品设计 × 架构 × 战略 × JD 画像 × 团队背景</div>
  </header>

  <nav class="tabs">
    <button v-for="t in tabs" :key="t.key" class="tab" :class="{ active: tab === t.key }" @click="tab = t.key">
      {{ t.label }}
    </button>
  </nav>

  <main class="wrap">
    <!-- 公司画像 -->
    <section v-if="tab === 'companies'">
      <div class="searchbar">
        <input v-model="q" @keyup.enter="onSearch" placeholder="搜索公司 / 方向 / 能力画像 / 关键人物（如 姚顺雨、清华、RAG、推理优化）" />
        <button class="btn" @click="onSearch">搜索</button>
        <div class="chips">
          <button class="chip" :class="{ active: tier === 0 }" @click="setTier(0)">全部</button>
          <button class="chip" :class="{ active: tier === 1 }" @click="setTier(1)">第一梯队</button>
          <button class="chip" :class="{ active: tier === 2 }" @click="setTier(2)">第二梯队</button>
          <button class="chip" :class="{ active: tier === 3 }" @click="setTier(3)">第三梯队</button>
        </div>
      </div>

      <p v-if="loading" class="empty">加载中…</p>
      <p v-else-if="!companies.length" class="empty">没有匹配结果，换个关键词试试。</p>
      <div class="grid" v-else>
        <CompanyCard v-for="c in companies" :key="c.id" :company="c" @open="open" />
      </div>
    </section>

    <!-- 团队背景 -->
    <LineagePanel v-else-if="tab === 'lineage'" />

    <!-- 简历策略 -->
    <ResumePanel v-else-if="tab === 'resume'" />

    <!-- 招聘情报 -->
    <RecruitIntel v-else-if="tab === 'recruit'" />

    <!-- 爬虫 -->
    <CrawlPanel v-else-if="tab === 'crawl'" />
  </main>

  <CompanyModal v-if="selected" :company="selected" @close="close" />
</template>
