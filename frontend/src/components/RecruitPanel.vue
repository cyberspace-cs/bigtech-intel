<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api.js'
const rows = ref([])
onMounted(async () => { try { rows.value = await api.recruit() } catch (e) {} })
</script>

<template>
  <div class="panel">
    <h2>招聘入口速查表</h2>
    <p class="desc">各厂官方招聘入口。投递前以官网最新 JD 为准。</p>
    <table class="rectable">
      <thead>
        <tr><th>梯队</th><th>公司</th><th>方向</th><th>官方入口</th></tr>
      </thead>
      <tbody>
        <tr v-for="r in rows" :key="r.company">
          <td>{{ r.tier === 1 ? '第一梯队' : r.tier === 2 ? '第二梯队' : '第三梯队' }}</td>
          <td>{{ r.company }}</td>
          <td>{{ r.direction }}</td>
          <td><a :href="r.url" target="_blank" rel="noopener">{{ r.url }}</a></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
