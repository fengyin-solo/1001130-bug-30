import { computed, onMounted } from 'vue'

import { useOverviewStore } from '@/stores/overview'

/** 模块页统计卡：与运营概览同一份数据，按模块键取本模块的新增、待处理、异常量。
 *
 * 模块内执行状态流转动作后调用 refreshStats 强制重算，看板与模块页同步更新。
 */
export function useModuleStats(moduleKey: string) {
  const overview = useOverviewStore()

  const stats = computed(() => {
    const summary = overview.modules.find((item) => item.key === moduleKey)
    return [
      { label: '今日新增', value: summary?.created ?? 0 },
      { label: '待处理', value: summary?.pending ?? 0 },
      { label: '异常量', value: summary?.abnormal ?? 0 },
    ]
  })

  onMounted(() => {
    void overview.refresh()
  })

  return { stats, refreshStats: () => overview.refresh(true) }
}
