<script setup lang="ts">
import { ref } from 'vue'
import { useChatStore } from '@/stores/chat'

const store = useChatStore()
const input = ref('')

function handleSend() {
  const text = input.value.trim()
  if (!text || store.sending) return
  input.value = ''
  store.sendMessage(text)
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSend()
  }
}

const suggestions = [
  '帮我分析这道错题的错因',
  '解释一下二次函数的顶点式',
  '如何提高英语阅读理解能力',
  '牛顿第二定律的应用场景',
]
</script>

<template>
  <div class="flex flex-col h-full">
    <!-- 消息区 -->
    <div class="flex-1 overflow-y-auto p-xl space-y-lg">
      <!-- 欢迎语 -->
      <div v-if="store.messages.length === 0" class="text-center py-3xl animate-fade-in">
        <div class="w-16 h-16 rounded-full bg-gradient-to-br from-primary to-cat-cyan flex items-center justify-center mx-auto mb-lg">
          <svg class="w-8 h-8 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
        </div>
        <h2 class="text-2xl font-semibold text-ink-primary dark:text-white mb-sm">你好，我是 Recall AI</h2>
        <p class="text-ink-secondary mb-lg">我可以帮你分析错题、解答疑问、制定复习计划</p>
        <div class="flex flex-wrap justify-center gap-sm">
          <button
            v-for="s in suggestions"
            :key="s"
            @click="input = s; handleSend()"
            class="mac-btn-secondary text-sm"
          >
            {{ s }}
          </button>
        </div>
      </div>

      <!-- 消息列表 -->
      <ChatMessage v-for="msg in store.messages" :key="msg.id" :message="msg" />

      <!-- 打字中 -->
      <div v-if="store.sending" class="flex items-center gap-sm text-ink-tertiary animate-fade-in">
        <div class="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-cat-cyan flex items-center justify-center flex-shrink-0">
          <svg class="w-4 h-4 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/></svg>
        </div>
        <div class="mac-card px-lg py-md text-sm text-ink-tertiary">
          <span class="inline-flex gap-1">
            <span class="w-1.5 h-1.5 rounded-full bg-ink-tertiary animate-bounce" style="animation-delay:0ms" />
            <span class="w-1.5 h-1.5 rounded-full bg-ink-tertiary animate-bounce" style="animation-delay:150ms" />
            <span class="w-1.5 h-1.5 rounded-full bg-ink-tertiary animate-bounce" style="animation-delay:300ms" />
          </span>
        </div>
      </div>
    </div>

    <!-- 输入区 -->
    <div class="border-t border-black/5 dark:border-white/10 p-lg">
      <div class="mac-card flex items-end gap-sm p-sm">
        <textarea
          v-model="input"
          @keydown="handleKeydown"
          placeholder="输入你的问题... (Enter 发送, Shift+Enter 换行)"
          class="flex-1 resize-none bg-transparent border-none outline-none text-sm text-ink-primary dark:text-white placeholder:text-ink-tertiary min-h-[36px] max-h-[120px] py-1.5 px-2"
          rows="1"
        />
        <button
          @click="handleSend"
          :disabled="!input.trim() || store.sending"
          class="w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center disabled:opacity-40 transition-all hover:bg-primary-hover active:scale-95"
        >
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
        </button>
      </div>
    </div>
  </div>
</template>
