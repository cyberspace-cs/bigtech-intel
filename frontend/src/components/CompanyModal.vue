<script setup>
const props = defineProps({ company: Object })
const emit = defineEmits(['close'])
</script>

<template>
  <div class="modal-mask" @click.self="emit('close')">
    <div class="modal">
      <button class="close" @click="emit('close')">×</button>
      <h2>{{ company.emoji }} {{ company.name }}</h2>
      <div class="sub">{{ company.priority }} · {{ company.direction }}</div>

      <div class="sec">
        <h3>JD 画像 · 能力要求</h3>
        <div class="kv">
          <div class="k">代表岗位</div>
          <div>{{ (company.jd_positions || []).join(' / ') }}</div>
          <div class="k">能力画像</div>
          <div class="muted-text">{{ company.jd_capability }}</div>
          <div class="k">适配钩子</div>
          <div class="muted-text">{{ company.jd_hook }}</div>
        </div>
      </div>

      <div class="sec">
        <h3>分厂定制（简历重排）</h3>
        <div class="kv">
          <div class="k">求职意向</div>
          <div>{{ company.intent }}</div>
          <div class="k">技术栈置顶</div>
          <div class="pill-row">
            <span v-for="s in (company.stack || [])" :key="s" class="tag blue">{{ s }}</span>
          </div>
          <div class="k">Phase 置顶</div>
          <div>{{ company.phase_focus }}</div>
        </div>
      </div>

      <div class="sec" v-if="company.bg_summary">
        <h3>团队背景</h3>
        <p class="muted-text">{{ company.bg_summary }}</p>
        <div v-for="p in (company.key_people || [])" :key="p.name" class="person">
          <div class="pn">{{ p.name }} <span class="mc">· {{ p.school }}</span></div>
          <div class="pr">{{ p.role }}</div>
          <div class="pd">{{ p.detail }}</div>
        </div>
      </div>

      <div class="sec" v-if="company.bg_strategy">
        <h3>战略方向</h3>
        <p class="muted-text">{{ company.bg_strategy }}</p>
      </div>

      <div class="sec" v-if="company.bg_product">
        <h3>产品设计 / 核心产品</h3>
        <p class="muted-text">{{ company.bg_product }}</p>
      </div>

      <div class="sec" v-if="company.recent_developments && company.recent_developments.length">
        <h3>近期进展（发布的大模型 / 产品）</h3>
        <ul class="timeline">
          <li v-for="(r, i) in company.recent_developments" :key="i">
            <span class="tl-date">{{ r.date }}</span>
            <div class="tl-body">
              <div class="tl-title">{{ r.title }}</div>
              <div class="tl-detail muted-text">{{ r.detail }}</div>
            </div>
          </li>
        </ul>
      </div>

      <div class="sec" v-if="company.tech_architecture && company.tech_architecture.length">
        <h3>目前的技术架构</h3>
        <div class="arch-grid">
          <div class="arch" v-for="(t, i) in company.tech_architecture" :key="i">
            <div class="arch-name">{{ t.name }}</div>
            <div class="arch-desc muted-text">{{ t.desc }}</div>
          </div>
        </div>
      </div>

      <div class="sec" v-if="company.crawl_facts && company.crawl_facts.length">
        <h3>公开资料补充（爬虫抓取）</h3>
        <div v-for="f in company.crawl_facts" :key="f.id" class="fact">
          <div class="ft">{{ f.title }} <span class="src">· {{ f.source }}</span></div>
          <div class="fs">{{ f.summary }}</div>
          <a v-if="f.url" :href="f.url" target="_blank" rel="noopener">查看来源 ↗</a>
        </div>
      </div>

      <div class="sec" v-if="company.bg_sources && company.bg_sources.length">
        <h3>参考来源</h3>
        <ul class="muted-text">
          <li v-for="s in company.bg_sources" :key="s">{{ s }}</li>
        </ul>
      </div>

      <div class="sec">
        <a class="btn" :href="company.recruit_url" target="_blank" rel="noopener">官方招聘入口 ↗ {{ company.recruit_label }}</a>
      </div>
    </div>
  </div>
</template>
