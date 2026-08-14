<script setup lang="ts">
import { ref } from 'vue'

const faqs = [
  { q: '如何录入错题？', a: '支持四种方式：拍照识别（PaddleOCR）、截图粘贴、文本输入、AI 对话录入。点击「录入」按钮即可开始。' },
  { q: 'AI 如何分析错题？', a: 'Recall 使用 DeepSeek 大模型自动识别学科、知识点、错因，并生成详细的解题思路和复习建议。' },
  { q: '复习计划是如何生成的？', a: '基于 SM-2 间隔重复算法，根据你对每道题的回忆质量动态调整复习间隔，确保在遗忘曲线关键节点复习。' },
  { q: '如何导出错题？', a: '支持导出为 PDF 和 Markdown 格式，可按学科筛选后导出。' },
  { q: '数据存储在哪里？', a: '所有数据存储在本地 SQLite 数据库，向量索引存储在 ChromaDB，确保隐私安全。' },
  { q: '如何切换深色模式？', a: '点击顶部导航栏右侧的月亮/太阳图标即可切换，设置会自动保存。' },
]

const openIdx = ref<number | null>(null)

const shortcuts = [
  { icon: 'camera', label: '拍照录入', desc: 'PaddleOCR 识别题目' },
  { icon: 'chat', label: 'AI 对话', desc: '自然语言提问' },
  { icon: 'chart', label: '数据看板', desc: '学习趋势分析' },
  { icon: 'export', label: '导出分享', desc: 'PDF / Markdown' },
]
</script>

<template>
  <div class="max-w-3xl mx-auto py-3xl">
    <h1 class="text-2xl font-semibold text-ink-primary dark:text-white mb-xl">帮助中心</h1>

    <!-- 功能入口 -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-lg mb-2xl">
      <div v-for="item in shortcuts" :key="item.label" class="mac-card p-lg text-center hover:scale-[1.02] transition-transform cursor-pointer">
        <div class="w-10 h-10 rounded-card bg-primary-light dark:bg-primary/20 flex items-center justify-center mx-auto mb-sm">
          <svg v-if="item.icon === 'camera'" class="w-5 h-5 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
          <svg v-else-if="item.icon === 'chat'" class="w-5 h-5 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          <svg v-else-if="item.icon === 'chart'" class="w-5 h-5 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/></svg>
          <svg v-else class="w-5 h-5 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        </div>
        <p class="text-sm font-medium text-ink-primary dark:text-white">{{ item.label }}</p>
        <p class="text-xs text-ink-tertiary mt-1">{{ item.desc }}</p>
      </div>
    </div>

    <!-- FAQ -->
    <div class="space-y-sm">
      <h2 class="text-lg font-semibold text-ink-primary dark:text-white mb-md">常见问题</h2>
      <div
        v-for="(faq, i) in faqs"
        :key="i"
        class="mac-card overflow-hidden"
      >
        <button
          @click="openIdx = openIdx === i ? null : i"
          class="w-full flex items-center justify-between p-lg text-left"
        >
          <span class="text-sm font-medium text-ink-primary dark:text-white">{{ faq.q }}</span>
          <svg
            class="w-4 h-4 text-ink-tertiary transition-transform flex-shrink-0"
            :class="{ 'rotate-180': openIdx === i }"
            viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          >
            <polyline points="6 9 12 15 18 9"/>
          </svg>
        </button>
        <transition name="fade">
          <div v-if="openIdx === i" class="px-lg pb-lg text-sm text-ink-secondary leading-relaxed animate-slide-up">
            {{ faq.a }}
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: all 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; max-height: 0; }
</style>
