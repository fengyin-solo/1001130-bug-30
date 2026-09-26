import { defineStore } from 'pinia'

import { fetchJson } from '@/api/client'

export type OverviewCard = { label: string; value: number }
export type OverviewModule = {
  key: string
  name: string
  created: number
  pending: number
  abnormal: number
}

type OverviewPayload = { cards: OverviewCard[]; modules: OverviewModule[] }

/** 运营概览数据：看板卡片与各模块页统计卡共用这一份，保证两处数字一致。
 *
 * 刷新成功后缓存结果，返回看板时直接沿用，数字不会清零重排；
 * 取数失败时保留已拿到的数字，只把错误说明亮出来，由页面提供重试入口。
 */
export const useOverviewStore = defineStore('overview', {
  state: () => ({
    cards: [] as OverviewCard[],
    modules: [] as OverviewModule[],
    loaded: false,
    loading: false,
    error: '',
  }),
  actions: {
    async refresh(force = false) {
      if (this.loading || (this.loaded && !force)) {
        return
      }
      this.loading = true
      this.error = ''
      try {
        const payload = await fetchJson<OverviewPayload>('/api/overview')
        this.cards = payload.cards ?? []
        this.modules = payload.modules ?? []
        this.loaded = true
      } catch (error) {
        this.error = error instanceof Error ? error.message : '运营概览读取失败，请稍后重试'
      } finally {
        this.loading = false
      }
    },
  },
})
