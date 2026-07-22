<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../api.js'

const rows = ref([])
const loading = ref(false)
const tierF = ref(0)
const jtypeF = ref(0)
const q = ref('')

const text = ref('')
const source = ref('BOSS直聘')
const url = ref('')
const preview = ref(null)
const adding = ref(false)

const sources = ref([])
const showSources = ref(false)

const stats = computed(() => {
  let urgent = 0, social = 0
  for (const r of rows.value) (r.jtype === 1 ? urgent++ : social++)
  return { urgent, social, total: rows.value.length }
})

const tierLabel = (t) => (t === 1 ? '第一梯队' : t === 2 ? '第二梯队' : t === 3 ? '第三梯队' : '通用')
const jtypeLabel = (j) => (j === 1 ? '急招' : '社招')

async function load() {
  loading.value = true
  try {
    rows.value = await api.jdList(tierF.value, jtypeF.value, q.value)
  } catch (e) {
    rows.value = []
  } finally {
    loading.value = false
  }
}

function setTier(t) { tierF.value = t; load() }
function setJtype(j) { jtypeF.value = j; load() }
function onSearch() { load() }

async function doParse() {
  if (!text.value.trim()) return
  try {
    preview.value = await api.jdParse({ text: text.value, source: source.value, url: url.value || undefined })
  } catch (e) {
    preview.value = null
  }
}

async function doAdd() {
  if (!text.value.trim()) return
  adding.value = true
  try {
    const payload = {
      text: text.value,
      source: source.value,
    }
    if (url.value) payload.url = url.value
    if (preview.value) {
      // 以预览结果作为覆盖项，保证入库与预览一致
      for (const k of ['company', 'title', 'salary', 'city', 'jtype', 'direction', 'matched', 'note']) {
        if (preview.value[k] !== undefined && preview.value[k] !== '') payload[k] = preview.value[k]
      }
    }
    await api.jdAdd(payload)
    text.value = ''
    url.value = ''
    preview.value = null
    await load()
  } finally {
    adding.value = false
  }
}

async function doDelete(id) {
  try {
    await api.jdDelete(id)
    await load()
  } catch (e) {}
}

async function toggleSources() {
  showSources.value = !showSources.value
  if (showSources.value && sources.value.length === 0) {
    try { sources.value = await api.recruit() } catch (e) { sources.value = [] }
  }
}

function matchTags(s) {
  return s ? s.split('·').filter(Boolean) : []
}

onMounted(load)
</script>

<template>
  <div>
    <div class="panel">
      <h2>招聘情报台</h2>
      <p class="desc">
        优先收集与我们 20 家跟踪厂 / 方向相关的 <b>急招</b> 与 <b>社招</b>。
        BOSS / 猎聘等第三方平台走「粘贴 JD 文本 → 自动结构化 → 入库」；官网招聘页为官方源。
      </p>

      <!-- 筛选 -->
      <div class="searchbar">
        <input v-model="q" @keyup.enter="onSearch" placeholder="搜索岗位 / 公司 / 方向 / 命中厂（如 Agent、智谱、具身）" />
        <button class="btn" @click="onSearch">搜索</button>
        <div class="chips">
          <button class="chip" :class="{ active: tierF === 0 }" @click="setTier(0)">全部</button>
          <button class="chip" :class="{ active: tierF === 1 }" @click="setTier(1)">第一梯队</button>
          <button class="chip" :class="{ active: tierF === 2 }" @click="setTier(2)">第二梯队</button>
          <button class="chip" :class="{ active: tierF === 3 }" @click="setTier(3)">第三梯队</button>
        </div>
        <div class="chips">
          <button class="chip" :class="{ active: jtypeF === 0 }" @click="setJtype(0)">急招+社招</button>
          <button class="chip" :class="{ active: jtypeF === 1 }" @click="setJtype(1)">仅急招</button>
          <button class="chip" :class="{ active: jtypeF === 2 }" @click="setJtype(2)">仅社招</button>
        </div>
      </div>

      <!-- 统计 -->
      <div class="jd-stats">
        <div class="jd-stat urgent"><div class="n">{{ stats.urgent }}</div><div class="l">急招</div></div>
        <div class="jd-stat social"><div class="n">{{ stats.social }}</div><div class="l">社招</div></div>
        <div class="jd-stat"><div class="n">{{ stats.total }}</div><div class="l">情报总数</div></div>
      </div>
    </div>

    <!-- JD 卡片 -->
    <p v-if="loading" class="empty">加载中…</p>
    <p v-else-if="!rows.length" class="empty">暂无情报。把下面的 JD 文本贴进来即可入库。</p>
    <div class="grid" v-else>
      <div v-for="r in rows" :key="r.id" class="card" :class="'t' + (r.tier || 0)">
        <div class="head">
          <div class="name">{{ r.title || '未命名岗位' }}</div>
          <span class="tier-tag">{{ tierLabel(r.tier) }}</span>
        </div>
        <div class="jd-meta">
          <span class="jt" :class="r.jtype === 1 ? 'urgent' : 'social'">{{ jtypeLabel(r.jtype) }}</span>
          <span v-if="r.company" class="m">{{ r.company }}</span>
          <span v-if="r.city" class="m">{{ r.city }}</span>
        </div>
        <div v-if="r.salary" class="jd-salary">{{ r.salary }}</div>
        <div v-if="r.direction" class="dir">方向：{{ r.direction }}</div>
        <div v-if="r.matched" class="jd-matched">
          <span class="ml">命中厂：</span>
          <span v-for="(m, i) in matchTags(r.matched)" :key="i" class="tag blue">{{ m }}</span>
        </div>
        <div v-if="r.note" class="jd-note">{{ r.note }}</div>
        <div class="jd-foot">
          <span class="src">{{ r.source }}<span v-if="r.date"> · {{ r.date }}</span></span>
          <button class="del" @click="doDelete(r.id)">删除</button>
        </div>
      </div>
    </div>

    <!-- 添加情报 -->
    <div class="panel" style="margin-top:22px;">
      <h2>+ 添加情报（粘贴即结构化）</h2>
      <p class="desc">把 BOSS / 官网 / 猎头的 JD 全文粘贴进来，点「解析预览」看结构化结果，再「确认入库」。</p>
      <textarea v-model="text" placeholder="粘贴 JD 文本，例如：Agent开发-大厂急招……职位描述 1）……职位要求……"></textarea>
      <div class="jd-form-row">
        <input class="src-in" v-model="source" placeholder="来源，如 BOSS直聘 / 官网 / 猎聘" />
        <input class="src-in" v-model="url" placeholder="来源链接（可选）" />
        <button class="btn ghost" @click="doParse" :disabled="!text.trim()">解析预览</button>
      </div>

      <div v-if="preview" class="jd-preview">
        <div class="pv-title">解析预览</div>
        <div class="pv-grid">
          <div><span class="k">岗位</span>{{ preview.title }}</div>
          <div><span class="k">公司</span>{{ preview.company || '—' }}</div>
          <div><span class="k">薪资</span>{{ preview.salary || '—' }}</div>
          <div><span class="k">城市</span>{{ preview.city || '—' }}</div>
          <div><span class="k">经验</span>{{ preview.exp || '—' }}</div>
          <div><span class="k">学历</span>{{ preview.edu || '—' }}</div>
          <div><span class="k">类型</span>{{ jtypeLabel(preview.jtype) }}</div>
          <div><span class="k">方向</span>{{ preview.direction }}</div>
        </div>
        <div v-if="preview.matched" class="pv-matched">
          <span class="k">命中厂：</span>
          <span v-for="(m, i) in matchTags(preview.matched)" :key="i" class="tag blue">{{ m }}</span>
        </div>
        <div v-if="preview.note" class="pv-note">{{ preview.note }}</div>
        <button class="btn" @click="doAdd" :disabled="adding">确认入库</button>
      </div>
    </div>

    <!-- 情报源 -->
    <div class="panel" style="margin-top:22px;">
      <button class="src-toggle" @click="toggleSources">
        {{ showSources ? '收起' : '展开' }}官方招聘源（20 厂 careers 入口）
      </button>
      <table v-if="showSources" class="rectable">
        <thead>
          <tr><th>梯队</th><th>公司</th><th>方向</th><th>官方入口</th></tr>
        </thead>
        <tbody>
          <tr v-for="s in sources" :key="s.company">
            <td>{{ s.tier === 1 ? '第一梯队' : s.tier === 2 ? '第二梯队' : '第三梯队' }}</td>
            <td>{{ s.company }}</td>
            <td>{{ s.direction }}</td>
            <td><a :href="s.url" target="_blank" rel="noopener">{{ s.url }}</a></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.jd-stats { display: flex; gap: 12px; margin-top: 16px; }
.jd-stat { flex: 1; border: 1px solid var(--border); border-radius: 12px; padding: 12px 16px; background: #f8fafc; }
.jd-stat .n { font-size: 24px; font-weight: 800; color: var(--ink); }
.jd-stat .l { font-size: 12px; color: var(--muted); margin-top: 2px; }
.jd-stat.urgent .n { color: #dc2626; }
.jd-stat.social .n { color: var(--primary); }

.jd-meta { display: flex; align-items: center; gap: 8px; margin: 10px 0 6px; flex-wrap: wrap; }
.jd-meta .m { font-size: 13px; color: var(--muted); }
.jt { font-size: 12px; font-weight: 700; padding: 2px 9px; border-radius: 6px; }
.jt.urgent { background: #fee2e2; color: #dc2626; }
.jt.social { background: #f1f5f9; color: #475569; }
.jd-salary { font-size: 15px; font-weight: 800; color: #0f172a; margin: 4px 0; }
.jd-matched { margin-top: 8px; display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.jd-matched .ml { font-size: 12px; color: var(--muted); }
.jd-note { font-size: 12.5px; color: #475569; line-height: 1.6; margin-top: 8px; background: #f8fbff; border-left: 3px solid var(--accent); padding: 8px 10px; border-radius: 6px; }
.jd-foot { display: flex; justify-content: space-between; align-items: center; margin-top: 10px; }
.jd-foot .src { font-size: 12px; color: var(--muted); }
.jd-foot .del { border: 1px solid var(--border); background: #fff; color: #b91c1c; border-radius: 8px; padding: 4px 10px; font-size: 12px; }

textarea { width: 100%; min-height: 130px; padding: 12px 14px; font-size: 14px; border: 1px solid var(--border); border-radius: 12px; outline: none; resize: vertical; font-family: inherit; }
textarea:focus { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(29,78,216,.12); }
.jd-form-row { display: flex; gap: 10px; margin-top: 10px; flex-wrap: wrap; }
.src-in { flex: 1; min-width: 180px; padding: 10px 14px; border: 1px solid var(--border); border-radius: 10px; outline: none; }
.src-in:focus { border-color: var(--primary); }

.jd-preview { margin-top: 14px; border: 1px dashed var(--primary); border-radius: 12px; padding: 14px 16px; background: #f8fbff; }
.pv-title { font-weight: 800; color: var(--primary); margin-bottom: 10px; }
.pv-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 8px 16px; font-size: 13.5px; }
.pv-grid .k, .pv-matched .k { display: inline-block; width: 44px; color: var(--muted); font-weight: 600; }
.pv-matched { margin-top: 10px; display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.pv-note { font-size: 12.5px; color: #475569; line-height: 1.6; margin: 10px 0; }
.jd-preview .btn { margin-top: 6px; }

.src-toggle { border: none; background: transparent; color: var(--primary); font-weight: 700; font-size: 14px; padding: 0; cursor: pointer; }
</style>
