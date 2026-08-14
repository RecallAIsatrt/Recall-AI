<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { dashboardApi } from '@/api'
import type { DashboardStats } from '@/types'
import KPICard from '@/components/dashboard/KPICard.vue'

const stats = ref<DashboardStats>({
  total: 128, mastered: 82, pending: 23, avg_reviews: 4.2,
  subject_distribution: { 数学: 42, 物理: 31, 英语: 27, 化学: 18, 生物: 10 },
  weekly_trend: [],
  weak_points: [
    { point: '二次函数', count: 8 },
    { point: '牛顿定律', count: 6 },
    { point: '定语从句', count: 5 },
    { point: '化学平衡', count: 4 },
    { point: '光合作用', count: 3 },
  ],
})

onMounted(async () => {
  try {
    stats.value = await dashboardApi.stats()
  } catch { /* 使用 mock 数据 */ }
})

const subjectColors: Record<string, string> = {
  数学: '#60A5FA', 物理: '#22D3EE', 英语: '#FBBF24', 化学: '#34D399', 生物: '#C084FC',
}
</script>

<template>
  <div class="max-w-5xl mx-auto">
    <h1 class="text-2xl font-semibold text-ink-primary dark:text-white mb-xl">数据看板</h1>

    <!-- KPI 卡片 -->
    <KPICard :stats="stats" class="mb-2xl" />

    <!-- 图表区 2×2 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-lg">
      <!-- 学科分布 -->
      <div class="mac-card p-lg">
        <h3 class="text-sm font-semibold text-ink-primary dark:text-white mb-lg">学科分布</h3>
        <div class="space-y-sm">
          <div v-for="(count, subject) in stats.subject_distribution" :key="subject" class="flex items-center gap-sm">
            <span class="text-xs text-ink-secondary w-10">{{ subject }}</span>
            <div class="flex-1 h-6 bg-surface-secondary dark:bg-white/5 rounded-btn overflow-hidden">
              <div
                class="h-full rounded-btn transition-all duration-mac ease-mac"
                :style="{ width: (count / 42 * 100) + '%', background: subjectColors[subject] || '#A78BFA' }"
              />
            </div>
            <span class="text-xs text-ink-tertiary w-8 text-right">{{ count }}</span>
          </div>
        </div>
      </div>

      <!-- 薄弱知识点 -->
      <div class="mac-card p-lg">
        <h3 class="text-sm font-semibold text-ink-primary dark:text-white mb-lg">薄弱知识点</h3>
        <div class="space-y-sm">
          <div v-for="(item, i) in stats.weak_points" :key="i" class="flex items-center gap-sm">
            <span class="text-xs text-ink-tertiary w-5">{{ i + 1 }}</span>
            <span class="text-sm text-ink-primary dark:text-white flex-1">{{ item.point }}</span>
            <span class="mac-tag text-xs">{{ item.count }} 题</span>
          </div>
        </div>
      </div>

      <!-- 掌握率环形图 -->
      <div class="mac-card p-lg flex flex-col items-center justify-center">
        <h3 class="text-sm font-semibold text-ink-primary dark:text-white mb-lg self-start">掌握率</h3>
        <svg viewBox="0 0 120 120" class="w-32 h-32">
          <circle cx="60" cy="60" r="50" fill="none" stroke="currentColor" stroke-width="8" class="text-surface-tertiary dark:text-white/10" />
          <circle
            cx="60" cy="60" r="50" fill="none" stroke="#34D399" stroke-width="8"
            stroke-linecap="round"
            :stroke-dasharray="`${(stats.mastered / Math.max(stats.total, 1)) * 314} 314`"
            transform="rotate(-90 60 60)"
          />
          <text x="60" y="55" text-anchor="middle" class="text-2xl font-semibold" fill="currentColor">
            {{ Math.round((stats.mastered / Math.max(stats.total, 1)) * 100) }}%
          </text>
          <text x="60" y="72" text-anchor="middle" class="text-xs" fill="#A8A4CC">已掌握</text>
        </svg>
      </div>

      <!-- 复习统计 -->
      <div class="mac-card p-lg">
        <h3 class="text-sm font-semibold text-ink-primary dark:text-white mb-lg">复习统计</h3>
        <div class="space-y-md">
          <div class="flex items-center justify-between">
            <span class="text-sm text-ink-secondary">平均复习次数</span>
            <span class="text-lg font-semibold text-ink-primary dark:text-white">{{ stats.avg_reviews }}</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-sm text-ink-secondary">待复习</span>
            <span class="text-lg font-semibold text-warning">{{ stats.pending }}</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-sm text-ink-secondary">已掌握</span>
            <span class="text-lg font-semibold text-success">{{ stats.mastered }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
