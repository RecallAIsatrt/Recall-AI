<script setup lang="ts">
import { useChatStore } from '@/stores/chat'
import { onMounted } from 'vue'

const store = useChatStore()

onMounted(() => {
  store.fetchSessions()
})

function formatTime(dateStr: string) {
  const d = new Date(dateStr)
  const now = new Date()
  if (d.toDateString() === now.toDateString()) return d.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  return d.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}
</script>

<template>
  <div>
    <!-- 新建对话 -->
    <button
      @click="store.createSession()"
      class="mac-btn-primary w-full mb-md"
    >
      <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
      新建对话
    </button>

    <!-- 对话列表 -->
    <div class="space-y-xs">
      <div
        v-for="session in store.sessions"
        :key="session.id"
        class="folder-item"
        :class="{ active: store.activeSessionId === session.id }"
        @click="store.selectSession(session.id)"
      >
        <svg class="w-4 h-4 flex-shrink-0 text-ink-tertiary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        <div class="flex-1 min-w-0">
          <p class="text-sm truncate">{{ session.title }}</p>
          <p class="text-xs text-ink-tertiary">{{ formatTime(session.updated_at) }}</p>
        </div>
        <!-- 删除 -->
        <button
          @click.stop="store.deleteSession(session.id)"
          class="hidden group-hover:flex w-5 h-5 items-center justify-center rounded text-ink-tertiary hover:text-error"
        >
          <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>
    </div>
  </div>
</template>
