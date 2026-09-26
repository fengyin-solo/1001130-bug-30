import { defineStore } from 'pinia'

import { fetchJson } from '@/api/client'

export type OverviewCard = { label: string; value: number }
export type OverviewModuleRow = { name: string; created: number; pending: number; abnormal: number }

type OverviewPayload = { cards: OverviewCard[]; modules: OverviewModuleRow[] }

/** 运营概览数据：放在全局 store 里，路由来回切换数字不丢；
 * 刷新失败时保留上一版数字，只给出说明并允许重试。
 */
export const useOverviewStore = defineStore('overview', {
  state: () => ({
    cards: [] as OverviewCard[],
    modules: [] as OverviewModuleRow[],
    error: '',
    loading: false,
  }),
  actions: {
    async refresh() {
      if (this.loading) {
        return
      }
      this.loading = true
      try {
        const payload = await fetchJson<OverviewPayload>('/api/overview')
        this.cards = payload.cards ?? []
        this.modules = payload.modules ?? []
        this.error = ''
      } catch (error) {
        // 不清空已拿到的数字，避免刷新失败后看板被置空或错位
        this.error = error instanceof Error ? error.message : '概览数据读取失败，请稍后重试'
      } finally {
        this.loading = false
      }
    },
  },
})
