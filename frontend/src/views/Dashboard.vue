<template>
  <section class="page">
    <header class="page-head">
      <div>
        <h2>运营概览</h2>
        <p class="page-desc">汇总各业务模块的关键指标，先看总量再看异常。</p>
      </div>
    </header>
    <div class="stat-row">
      <article v-for="card in overview.cards" :key="card.label" class="stat-card">
        <span class="stat-label">{{ card.label }}</span>
        <strong class="stat-value">{{ card.value }}</strong>
      </article>
    </div>
    <table class="data-table">
      <thead>
        <tr><th>业务模块</th><th>今日新增</th><th>待处理</th><th>异常量</th></tr>
      </thead>
      <tbody>
        <tr v-for="row in overview.modules" :key="row.key">
          <td>{{ row.name }}</td>
          <td>{{ row.created }}</td>
          <td>{{ row.pending }}</td>
          <td>{{ row.abnormal }}</td>
        </tr>
        <tr v-if="!overview.modules.length">
          <td colspan="4" class="empty-state">暂无概览数据</td>
        </tr>
      </tbody>
    </table>
    <footer v-if="overview.error" class="page-foot">
      <span class="error-text">{{ overview.error }}</span>
      <button class="btn" type="button" @click="retry">重新加载</button>
    </footer>
  </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

import { useOverviewStore } from '@/stores/overview'

const overview = useOverviewStore()

function retry() {
  void overview.refresh(true)
}

onMounted(() => {
  void overview.refresh()
})
</script>
