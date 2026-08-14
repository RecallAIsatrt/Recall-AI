<script setup lang="ts">
import type { Mistake } from '@/types'
import { SUBJECT_COLORS } from '@/types'
import { ref } from 'vue'

const props = defineProps<{ mistake: Mistake }>()
const emit = defineEmits<{
  (e: 'edit', id: number): void
  (e: 'delete', id: number): void
}>()

const showAnalysis = ref(false)
const subjectColor = SUBJECT_COLORS[props.mistake.subject] || '#A78BFA'

function formatCount(n: number): string {
  return n === 0 ? '未复习' : `复习 ${n} 次`
}
</script>

<template>
  <div class="mac-card p-lg animate-fade-in">
    <!-- 顶部：来源 + 学科 + 知识点 + 操作 -->
    <div class="flex items-center gap-sm flex-wrap mb-md">
      <span class="mac-tag-primary" :style="{ background: subjectColor + '15', color: subjectColor, borderColor: subjectColor + '30' }">
        {{ mistake.subject }}
      </span>
      <span v-if="mistake.knowledge_point" class="mac-tag">
        {{ mistake.knowledge_point }}
      </span>
      <span v-if="mistake.source" class="text-xs text-ink-tertiary">
        {{ mistake.source }}
      </span>
      <div class="ml-auto flex items-center gap-xs">
        <!-- 复习次数 -->
        <span class="text-xs text-ink-tertiary flex items-center gap-1">
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></svg>
          {{ formatCount(mistake.review_count) }}
        </span>
        <!-- 编辑 -->
        <button
          @click="emit('edit', mistake.id)"
          class="w-7 h-7 rounded-btn flex items-center justify-center text-ink-tertiary hover:text-primary hover:bg-primary-light transition-colors"
        >
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
        </button>
        <!-- 删除 -->
        <button
          @click="emit('delete', mistake.id)"
          class="w-7 h-7 rounded-btn flex items-center justify-center text-ink-tertiary hover:text-error hover:bg-error/10 transition-colors"
        >
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
        </button>
      </div>
    </div>

    <!-- 题目区 -->
    <div class="region-question mb-sm">
      <div class="flex items-center gap-1 mb-1">
        <svg class="w-3.5 h-3.5 text-question" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/></svg>
        <span class="text-xs font-semibold text-question">题目</span>
      </div>
      <p class="text-sm text-ink-primary dark:text-white leading-relaxed">{{ mistake.content }}</p>
    </div>

    <!-- AI 解析区（可折叠） -->
    <div v-if="mistake.ai_analysis">
      <button
        @click="showAnalysis = !showAnalysis"
        class="flex items-center gap-1 text-xs font-semibold text-analysis hover:underline mb-1"
      >
        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
        AI 解析
        <svg class="w-3 h-3 transition-transform" :class="{ 'rotate-180': showAnalysis }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
      </button>
      <transition name="fade">
        <div v-if="showAnalysis" class="region-analysis animate-slide-up">
          <p class="text-sm text-ink-primary dark:text-white leading-relaxed">{{ mistake.ai_analysis }}</p>
        </div>
      </transition>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: all 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(-4px); }
</style>
