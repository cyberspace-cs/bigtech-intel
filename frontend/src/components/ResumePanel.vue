<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api.js'
const tips = ref([])
const strategy = ref([])
onMounted(async () => {
  try {
    tips.value = await api.resumeTips()
    strategy.value = await api.resumeStrategy()
  } catch (e) {}
})
</script>

<template>
  <div class="panel">
    <h2>简历打磨 · 6 条具体改动</h2>
    <p class="desc">基于岗位统计高频词与 JD 画像，逐项落到简历上（应用到基础简历）。</p>
    <div class="tips">
      <div class="tip" v-for="t in tips" :key="t.title">
        <div class="tt">{{ t.title }}</div>
        <div class="td">{{ t.detail }}</div>
      </div>
    </div>

    <div class="section-title">分厂定制策略表</div>
    <table class="strat">
      <thead>
        <tr><th>公司</th><th>求职意向</th><th>技术栈置顶</th><th>Phase 置顶</th></tr>
      </thead>
      <tbody>
        <tr v-for="s in strategy" :key="s.company">
          <td>{{ s.company }}</td>
          <td>{{ s.intent }}</td>
          <td>{{ s.stack }}</td>
          <td>{{ s.phase }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
