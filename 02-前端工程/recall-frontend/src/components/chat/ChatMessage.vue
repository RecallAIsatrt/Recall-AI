<script setup lang="ts">
import type { ChatMessage } from '@/types'

defineProps<{ message: ChatMessage }>()
</script>

<template>
  <div
    class="flex gap-sm animate-fade-in"
    :class="message.role === 'user' ? 'flex-row-reverse' : 'flex-row'"
  >
    <!-- 头像 -->
    <div
      v-if="message.role === 'assistant'"
      class="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-cat-cyan flex items-center justify-center flex-shrink-0"
    >
      <svg class="w-4 h-4 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
    </div>

    <!-- 消息气泡 -->
    <div
      class="max-w-[70%] rounded-card px-lg py-md text-sm leading-relaxed"
      :class="message.role === 'user'
        ? 'bg-primary text-white'
        : 'mac-card'"
    >
      {{ message.content }}
    </div>
  </div>
</template>
