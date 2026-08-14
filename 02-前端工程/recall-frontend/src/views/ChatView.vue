<script setup lang="ts">
import { onMounted } from 'vue'
import { useChatStore } from '@/stores/chat'
import HistoryList from '@/components/chat/HistoryList.vue'
import ChatWindow from '@/components/chat/ChatWindow.vue'

const store = useChatStore()

onMounted(() => {
  store.fetchSessions()
})
</script>

<template>
  <div class="flex h-full">
    <!-- 左侧对话列表 -->
    <Sidebar>
      <HistoryList />
    </Sidebar>

    <!-- 右侧聊天窗口 -->
    <div class="flex-1 overflow-hidden">
      <div class="mac-card h-full flex flex-col overflow-hidden">
        <ChatWindow />
      </div>
    </div>
  </div>
</template>
