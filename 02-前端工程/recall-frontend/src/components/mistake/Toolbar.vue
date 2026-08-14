<script setup lang="ts">
import { ref } from 'vue'
import { useMistakeStore } from '@/stores/mistake'

const store = useMistakeStore()
const emit = defineEmits<{
  (e: 'import'): void
  (e: 'review'): void
  (e: 'export'): void
}>()
</script>

<template>
  <div class="flex items-center gap-md flex-wrap mb-lg">
    <!-- 左侧主操作 -->
    <div class="flex items-center gap-sm">
      <button @click="emit('import')" class="mac-btn-primary">
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        录入
      </button>
      <button @click="emit('review')" class="mac-btn-secondary">
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></svg>
        开始复习
      </button>
      <button @click="emit('export')" class="mac-btn-secondary">
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        导出
      </button>
    </div>

    <!-- 右侧搜索与筛选 -->
    <div class="flex items-center gap-sm ml-auto">
      <div class="relative">
        <svg class="w-4 h-4 text-ink-tertiary absolute left-3 top-1/2 -translate-y-1/2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input
          v-model="store.searchKeyword"
          placeholder="搜索错题..."
          class="mac-input pl-10 w-56"
        />
      </div>
    </div>
  </div>
</template>
