/** AI 答疑 Store */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ChatSession, ChatMessage } from '@/types'
import { chatApi } from '@/api'

export const useChatStore = defineStore('chat', () => {
  const sessions = ref<ChatSession[]>([])
  const activeSessionId = ref<number | null>(null)
  const messages = ref<ChatMessage[]>([])
  const sending = ref(false)

  async function fetchSessions() {
    sessions.value = await chatApi.listSessions()
    if (!activeSessionId.value && sessions.value.length > 0) {
      activeSessionId.value = sessions.value[0].id
    }
  }

  async function createSession() {
    const s = await chatApi.createSession()
    sessions.value.unshift(s)
    activeSessionId.value = s.id
    messages.value = []
    return s
  }

  async function selectSession(id: number) {
    activeSessionId.value = id
    messages.value = await chatApi.getMessages(id)
  }

  async function sendMessage(content: string) {
    if (!activeSessionId.value) {
      await createSession()
    }
    const sid = activeSessionId.value!

    // 乐观更新 - 先显示用户消息
    const tempUserMsg: ChatMessage = {
      id: Date.now(),
      session_id: sid,
      role: 'user',
      content,
      created_at: new Date().toISOString(),
    }
    messages.value.push(tempUserMsg)

    sending.value = true
    try {
      const aiMsg = await chatApi.sendMessage(sid, content)
      messages.value.push(aiMsg)
      // 更新会话标题
      const session = sessions.value.find(s => s.id === sid)
      if (session && messages.value.filter(m => m.role === 'user').length <= 1) {
        session.title = content.slice(0, 30)
      }
    } finally {
      sending.value = false
    }
  }

  async function deleteSession(id: number) {
    await chatApi.deleteSession(id)
    sessions.value = sessions.value.filter(s => s.id !== id)
    if (activeSessionId.value === id) {
      activeSessionId.value = sessions.value[0]?.id ?? null
      if (activeSessionId.value) {
        messages.value = await chatApi.getMessages(activeSessionId.value)
      } else {
        messages.value = []
      }
    }
  }

  return {
    sessions, activeSessionId, messages, sending,
    fetchSessions, createSession, selectSession, sendMessage, deleteSession,
  }
})
