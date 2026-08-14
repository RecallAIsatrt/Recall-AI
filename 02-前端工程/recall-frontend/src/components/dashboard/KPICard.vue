<script setup lang="ts">
import { computed } from 'vue'
import type { DashboardStats } from '@/types'

const props = defineProps<{
  stats: DashboardStats
}>()

const cards = computed(() => [
  {
    label: '总错题',
    value: props.stats.total,
    icon: 'book',
    color: '#A78BFA',
    trend: null as string | null,
  },
  {
    label: '已掌握',
    value: props.stats.mastered,
    icon: 'check',
    color: '#34D399',
    trend: props.stats.total > 0 ? `${Math.round((props.stats.mastered / props.stats.total) * 100)}%` : null,
  },
  {
    label: '待复习',
    value: props.stats.pending,
    icon: 'clock',
    color: '#FBBF24',
    trend: null,
  },
  {
    label: '平均复习',
    value: props.stats.avg_reviews,
    icon: 'repeat',
    color: '#818CF8',
    suffix: '次',
    trend: null,
  },
])
</script>

<template>
  <div class="grid grid-cols-2 lg:grid-cols-4 gap-lg">
    <div v-for="card in cards" :key="card.label" class="mac-card p-lg animate-fade-in">
      <div class="flex items-center gap-sm mb-sm">
        <div class="w-8 h-8 rounded-btn flex items-center justify-center" :style="{ background: card.color + '15' }">
          <svg class="w-4 h-4" :style="{ color: card.color }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <template v-if="card.icon === 'book'"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></template>
            <template v-else-if="card.icon === 'check'"><polyline points="20 6 9 17 4 12"/></template>
            <template v-else-if="card.icon === 'clock'"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></template>
            <template v-else><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></template>
          </svg>
        </div>
        <span class="text-xs text-ink-secondary">{{ card.label }}</span>
      </div>
      <div class="flex items-baseline gap-1">
        <span class="text-2xl font-semibold text-ink-primary dark:text-white">{{ card.value }}</span>
        <span v-if="card.suffix" class="text-sm text-ink-tertiary">{{ card.suffix }}</span>
        <span v-if="card.trend" class="ml-auto text-xs font-medium text-success">{{ card.trend }}</span>
      </div>
    </div>
  </div>
</template>
