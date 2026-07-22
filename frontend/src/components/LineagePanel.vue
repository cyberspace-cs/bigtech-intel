<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api.js'
const data = ref(null)
onMounted(async () => { try { data.value = await api.lineage() } catch (e) {} })
</script>

<template>
  <div v-if="data">
    <div class="lineage-grid">
      <div class="faction qinghua" v-for="(blk, key) in data" :key="key">
        <h3>{{ blk.title }}</h3>
        <p class="muted-text" style="margin-top: 0">{{ blk.desc }}</p>
        <div class="member" v-for="m in blk.members" :key="m.name">
          <div class="mn">{{ m.name }}</div>
          <div class="mc">{{ m.company }} · {{ m.role }}</div>
          <div class="mnote">{{ m.school }} — {{ m.note }}</div>
        </div>
      </div>
    </div>
  </div>
  <p v-else class="empty">加载中…</p>
</template>
