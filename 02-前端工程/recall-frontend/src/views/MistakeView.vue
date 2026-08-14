<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useMistakeStore } from '@/stores/mistake'
import CategoryNav from '@/components/mistake/CategoryNav.vue'
import Toolbar from '@/components/mistake/Toolbar.vue'
import MistakeList from '@/components/mistake/MistakeList.vue'
import type { Mistake } from '@/types'
import { SUBJECT_COLORS, CATEGORY_COLORS } from '@/types'

const store = useMistakeStore()
const showImportModal = ref(false)
const showReviewModal = ref(false)

// 录入表单
const importForm = ref({
  title: '',
  content: '',
  subject: '数学',
  knowledge_point: '',
  source: '',
  category_id: null as number | null,
})

const subjects = Object.keys(SUBJECT_COLORS)

onMounted(async () => {
  await Promise.all([store.fetchMistakes(), store.fetchCategories()])
})

async function handleImport() {
  if (!importForm.value.content.trim()) return
  await store.addMistake(importForm.value)
  showImportModal.value = false
  importForm.value = { title: '', content: '', subject: '数学', knowledge_point: '', source: '', category_id: null }
}

function handleExport() {
  // 简单 toast 提示
  alert('导出功能需后端支持，请启动 FastAPI 服务')
}
</script>

<template>
  <div class="flex h-full">
    <!-- 左侧分类导航 -->
    <Sidebar>
      <CategoryNav />
    </Sidebar>

    <!-- 右侧内容区 -->
    <div class="flex-1 overflow-y-auto">
      <div class="max-w-4xl mx-auto">
        <Toolbar @import="showImportModal = true" @review="showReviewModal = true" @export="handleExport" />
        <MistakeList />
      </div>
    </div>
  </div>

  <!-- 录入模态框 -->
  <Teleport to="body">
    <transition name="fade">
      <div v-if="showImportModal" class="fixed inset-0 z-50 flex items-center justify-center p-lg">
        <!-- 遮罩 -->
        <div class="absolute inset-0 bg-black/30 backdrop-blur-sm" @click="showImportModal = false" />

        <!-- 模态面板 -->
        <div class="relative w-full max-w-lg mac-card p-2xl animate-scale-in">
          <h2 class="text-lg font-semibold text-ink-primary dark:text-white mb-lg">录入错题</h2>

          <div class="space-y-md">
            <div>
              <label class="text-xs text-ink-secondary mb-1 block">学科</label>
              <select v-model="importForm.subject" class="mac-input">
                <option v-for="s in subjects" :key="s" :value="s">{{ s }}</option>
              </select>
            </div>
            <div>
              <label class="text-xs text-ink-secondary mb-1 block">题目内容</label>
              <textarea v-model="importForm.content" class="mac-input h-32 resize-none py-2" placeholder="输入或粘贴题目..." />
            </div>
            <div>
              <label class="text-xs text-ink-secondary mb-1 block">知识点</label>
              <input v-model="importForm.knowledge_point" class="mac-input" placeholder="如：二次函数" />
            </div>
            <div>
              <label class="text-xs text-ink-secondary mb-1 block">来源</label>
              <input v-model="importForm.source" class="mac-input" placeholder="如：2024高考全国卷" />
            </div>
          </div>

          <div class="flex justify-end gap-sm mt-xl">
            <button @click="showImportModal = false" class="mac-btn-secondary">取消</button>
            <button @click="handleImport" class="mac-btn-primary">录入</button>
          </div>
        </div>
      </div>
    </transition>
  </Teleport>

  <!-- 复习模态框 -->
  <Teleport to="body">
    <transition name="fade">
      <div v-if="showReviewModal" class="fixed inset-0 z-50 flex items-center justify-center p-lg">
        <div class="absolute inset-0 bg-black/30 backdrop-blur-sm" @click="showReviewModal = false" />
        <div class="relative w-full max-w-md mac-card p-2xl animate-scale-in text-center">
          <svg class="w-12 h-12 mx-auto text-primary mb-md" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></svg>
          <h2 class="text-lg font-semibold text-ink-primary dark:text-white mb-sm">SM-2 智能复习</h2>
          <p class="text-sm text-ink-secondary mb-lg">基于间隔重复算法，今日待复习错题将在此展示</p>
          <button @click="showReviewModal = false" class="mac-btn-primary">开始复习</button>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
