<script setup lang="ts">
import { useMistakeStore } from '@/stores/mistake'
import { ref } from 'vue'

const store = useMistakeStore()
const showAddForm = ref(false)
const newCatName = ref('')

async function handleAdd() {
  const name = newCatName.value.trim()
  if (!name) return
  await store.addCategory(name)
  newCatName.value = ''
  showAddForm.value = false
}
</script>

<template>
  <div>
    <!-- 全部错题 -->
    <div
      class="folder-item"
      :class="{ active: store.activeCategory === null }"
      @click="store.activeCategory = null"
    >
      <svg class="w-4 h-4 text-ink-tertiary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
      <span class="flex-1 text-sm">全部错题</span>
      <span class="text-xs text-ink-tertiary">{{ store.mistakes.length }}</span>
    </div>

    <div class="h-px bg-black/5 dark:bg-white/10 my-sm" />

    <!-- 学科分类 -->
    <div
      v-for="cat in store.categories"
      :key="cat.id"
      class="folder-item group"
      :class="{ active: store.activeCategory === cat.id }"
      @click="store.activeCategory = cat.id"
    >
      <span class="w-3 h-3 rounded-full flex-shrink-0" :style="{ background: cat.color }" />
      <span class="flex-1 text-sm truncate">{{ cat.name }}</span>
      <span class="text-xs text-ink-tertiary">{{ cat.mistake_count }}</span>
      <!-- 删除按钮 -->
      <button
        @click.stop="store.removeCategory(cat.id)"
        class="hidden group-hover:flex w-5 h-5 items-center justify-center rounded text-ink-tertiary hover:text-error hover:bg-error/10"
      >
        <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>

    <!-- 新建分类 -->
    <div v-if="!showAddForm" class="mt-sm">
      <button
        @click="showAddForm = true"
        class="w-full flex items-center gap-2 px-3 py-2 rounded-btn border border-dashed border-black/10 dark:border-white/10 text-primary text-sm hover:bg-primary-light transition-colors"
      >
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        新建错题本
      </button>
    </div>
    <div v-else class="mt-sm flex gap-1">
      <input
        v-model="newCatName"
        @keyup.enter="handleAdd"
        @keyup.escape="showAddForm = false"
        placeholder="分类名称"
        class="mac-input flex-1 h-8 text-sm"
        autofocus
      />
      <button @click="handleAdd" class="mac-btn-primary h-8 text-xs px-3">添加</button>
      <button @click="showAddForm = false" class="mac-btn-secondary h-8 text-xs px-3">取消</button>
    </div>
  </div>
</template>
