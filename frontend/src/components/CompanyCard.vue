<script setup>
const props = defineProps({ company: Object })
const emit = defineEmits(['open'])
</script>

<template>
  <div class="card" :class="'t' + company.tier" @click="emit('open', company)">
    <div class="head">
      <span class="emoji">{{ company.emoji }}</span>
      <span class="name">{{ company.name }}</span>
      <span class="tier-tag">{{ company.tier === 1 ? '第一梯队' : company.tier === 2 ? '第二梯队' : '第三梯队' }}</span>
    </div>
    <div class="dir">{{ company.direction }}</div>
    <div class="stack">
      <span v-for="s in (company.stack || []).slice(0, 5)" :key="s" class="tag blue">{{ s }}</span>
    </div>
  </div>
</template>
