<script setup lang="ts">
import MistakeCard from './MistakeCard.vue'
import { useMistakeStore } from '@/stores/mistake'

const store = useMistakeStore()
</script>

<template>
  <div>
    <!-- 空状态 -->
    <div v-if="store.filteredMistakes.length === 0" class="mac-card p-3xl text-center">
      <svg class="w-12 h-12 mx-auto text-ink-tertiary mb-md" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
        <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
      </svg>
      <p class="text-ink-secondary text-sm">该分类下暂无错题</p>
      <p class="text-ink-tertiary text-xs mt-1">点击「录入」添加新的错题</p>
    </div>

    <!-- 卡片列表 -->
    <div v-else class="flex flex-col gap-lg">
      <MistakeCard
        v-for="m in store.filteredMistakes"
        :key="m.id"
        :mistake="m"
        @edit="() => {}"
        @delete="store.removeMistake"
      />
    </div>
  </div>
</template>
