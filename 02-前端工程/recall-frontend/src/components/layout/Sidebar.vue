<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <aside class="glass-sidebar w-60 flex-shrink-0 flex flex-col overflow-y-auto">
    <!-- 桌面隐喻：文件夹导航 -->
    <div class="p-lg">
      <div class="flex items-center gap-2 mb-md">
        <svg class="w-5 h-5 text-ink-tertiary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
        </svg>
        <span class="text-sm font-semibold text-ink-secondary dark:text-ink-tertiary uppercase tracking-wider">
          {{ route.name === 'chat' ? '对话' : '错题本' }}
        </span>
      </div>

      <!-- 由各页面自行填充侧栏内容 -->
      <slot />
    </div>

    <!-- 底部废纸篓 -->
    <div class="mt-auto p-lg border-t border-black/5 dark:border-white/10">
      <div class="folder-item text-ink-tertiary hover:text-error">
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
        </svg>
        <span class="text-sm">回收站</span>
      </div>
    </div>
  </aside>
</template>
