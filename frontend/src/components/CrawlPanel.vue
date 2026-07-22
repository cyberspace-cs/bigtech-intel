<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api.js'

const query = ref('')
const adapter = ref('wikipedia')
const logs = ref([])
const busy = ref(false)
const msg = ref('')

async function loadLogs() {
  try { logs.value = await api.crawlLogs() } catch (e) {}
}

async function trigger() {
  if (!query.value) { msg.value = '请输入要抓取的公司 / 关键词'; return }
  busy.value = true
  msg.value = '抓取中…'
  try {
    const res = await api.crawlTrigger({ query: query.value, adapter: adapter.value, link_to_company: true })
    const ok = (res.logs || []).filter((l) => l.status === 'success').length
    msg.value = `触发完成：成功 ${ok} 条 / 共 ${res.triggered} 条`
    await loadLogs()
  } catch (e) {
    msg.value = '抓取失败：' + e.message
  } finally {
    busy.value = false
  }
}

async function refreshAll() {
  busy.value = true
  msg.value = '已提交全量刷新（后台执行）…'
  try {
    await fetch('/api/crawl/refresh-all', { method: 'POST' })
    msg.value = '全量刷新已在后台启动，可在日志中查看进度。'
    await loadLogs()
  } catch (e) {
    msg.value = '失败：' + e.message
  } finally {
    busy.value = false
  }
}

onMounted(loadLogs)
</script>

<template>
  <div class="panel">
    <h2>爬虫 / 数据源</h2>
    <p class="desc">
      调用后端可扩展爬虫（Wikipedia / 百度百科 / 官网适配器），把公开资料写入数据库，持续完善大小厂情报。
      触发结果见下方日志。
    </p>

    <div class="crawl-row">
      <input v-model="query" placeholder="要抓取的公司或关键词，如 月之暗面 / DeepSeek" />
      <select v-model="adapter" class="chip">
        <option value="wikipedia">Wikipedia</option>
        <option value="baidu_baike">百度百科</option>
        <option value="official">官网</option>
        <option value="all">全部</option>
      </select>
      <button class="btn" :disabled="busy" @click="trigger">抓取</button>
      <button class="btn ghost" :disabled="busy" @click="refreshAll">全量刷新（全部公司）</button>
    </div>

    <p v-if="msg" class="muted-text">{{ msg }}</p>

    <div class="section-title">抓取日志</div>
    <div v-if="!logs.length" class="empty">暂无日志，先抓一条试试。</div>
    <div v-for="l in logs" :key="l.id" class="log" :class="l.status">
      <span class="ls" :class="l.status">{{ l.status === 'success' ? '成功' : '失败' }}</span>
      · {{ l.target }} · {{ l.adapter }} — {{ l.message }}
    </div>
  </div>
</template>
