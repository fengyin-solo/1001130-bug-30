<template>
  <section class="page">
    <header class="page-head">
      <div>
        <h2>运营概览</h2>
        <p class="page-desc">汇总各业务模块的关键指标，先看总量再看异常。</p>
      </div>
    </header>
    <p v-if="store.error" class="error-text overview-error">
      <span>概览数据读取失败：{{ store.error }}</span>
      <button class="btn" type="button" @click="retry">重试</button>
    </p>
    <div class="stat-row">
      <article v-for="card in store.cards" :key="card.label" class="stat-card">
        <span class="stat-label">{{ card.label }}</span>
        <strong class="stat-value">{{ card.value }}</strong>
      </article>
    </div>
    <table class="data-table">
      <thead>
        <tr><th>业务模块</th><th>今日新增</th><th>待处理</th><th>异常量</th></tr>
      </thead>
      <tbody>
        <tr v-for="row in store.modules" :key="row.name">
          <td>{{ row.name }}</td>
          <td>{{ row.created }}</td>
          <td>{{ row.pending }}</td>
          <td>{{ row.abnormal }}</td>
        </tr>
        <tr v-if="!store.modules.length">
          <td colspan="4" class="empty-state">
            {{ store.error ? '概览数据暂时不可用，请点击上方重试' : '概览数据加载中…' }}
          </td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

import { useOverviewStore } from '@/stores/overview'

const store = useOverviewStore()

function retry() {
  void store.refresh()
}

onMounted(() => {
  void store.refresh()
})
</script>

<style scoped>
.overview-error {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 0 12px;
}
</style>
