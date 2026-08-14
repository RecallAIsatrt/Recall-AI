<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const navItems = [
  { name: 'mistakes', label: '错题集', icon: 'book' },
  { name: 'chat', label: 'AI答疑', icon: 'chat' },
  { name: 'dashboard', label: '数据看板', icon: 'chart' },
  { name: 'help', label: '帮助', icon: 'help' },
]

function navigate(name: string) {
  router.push({ name })
}
</script>

<template>
  <header class="glass-topbar sticky top-0 z-50 h-14 flex items-center px-xl">
    <!-- Logo -->
    <div class="flex items-center gap-sm cursor-pointer select-none" @click="navigate('mistakes')">
      <div class="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
        <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
          <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
        </svg>
      </div>
      <span class="text-lg font-semibold text-ink-primary dark:text-white">Recall</span>
    </div>

    <!-- 导航 -->
    <nav class="flex items-center gap-xs ml-lg">
      <button
        v-for="item in navItems"
        :key="item.name"
        @click="navigate(item.name)"
        class="mac-btn-ghost text-sm"
        :class="route.name === item.name ? 'bg-primary-light font-medium text-primary' : 'text-ink-secondary'"
      >
        <!-- 图标 -->
        <svg v-if="item.icon === 'book'" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
        <svg v-else-if="item.icon === 'chat'" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        <svg v-else-if="item.icon === 'chart'" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/></svg>
        <svg v-else class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/></svg>
        {{ item.label }}
      </button>
    </nav>

    <!-- 右侧操作 -->
    <div class="ml-auto flex items-center gap-md">
      <!-- 用户头像 -->
      <div class="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-cat-cyan flex items-center justify-center text-white text-xs font-semibold">
        R
      </div>
    </div>
  </header>
</template>
