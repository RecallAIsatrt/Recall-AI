/** API 请求层 */
import axios from 'axios'
import type { Category, Mistake, ChatSession, ChatMessage, DashboardStats, ReviewRecord } from '@/types'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
})

// ── 错题 ──
export const mistakesApi = {
  list: (params?: { subject?: string; category_id?: number; keyword?: string }) =>
    api.get<Mistake[]>('/mistakes', { params }).then(r => r.data),
  get: (id: number) =>
    api.get<Mistake>(`/mistakes/${id}`).then(r => r.data),
  create: (data: Partial<Mistake>) =>
    api.post<Mistake>('/mistakes', data).then(r => r.data),
  update: (id: number, data: Partial<Mistake>) =>
    api.patch<Mistake>(`/mistakes/${id}`, data).then(r => r.data),
  delete: (id: number) =>
    api.delete(`/mistakes/${id}`).then(r => r.data),
  search: (q: string) =>
    api.get<Mistake[]>('/mistakes/search', { params: { q } }).then(r => r.data),
}

// ── 分类 ──
export const categoriesApi = {
  list: () =>
    api.get<Category[]>('/categories').then(r => r.data),
  create: (data: { name: string; color: string }) =>
    api.post<Category>('/categories', data).then(r => r.data),
  update: (id: number, data: Partial<Category>) =>
    api.patch<Category>(`/categories/${id}`, data).then(r => r.data),
  delete: (id: number) =>
    api.delete(`/categories/${id}`).then(r => r.data),
}

// ── AI 答疑 ──
export const chatApi = {
  listSessions: () =>
    api.get<ChatSession[]>('/chat/sessions').then(r => r.data),
  createSession: (title?: string) =>
    api.post<ChatSession>('/chat/sessions', { title }).then(r => r.data),
  deleteSession: (id: number) =>
    api.delete(`/chat/sessions/${id}`).then(r => r.data),
  getMessages: (sessionId: number) =>
    api.get<ChatMessage[]>(`/chat/sessions/${sessionId}/messages`).then(r => r.data),
  sendMessage: (sessionId: number, content: string) =>
    api.post<ChatMessage>(`/chat/sessions/${sessionId}/messages`, { content }).then(r => r.data),
}

// ── 复习 ──
export const reviewApi = {
  today: () =>
    api.get<Mistake[]>('/review/today').then(r => r.data),
  submit: (mistakeId: number, quality: number) =>
    api.post<ReviewRecord>(`/review/${mistakeId}`, { quality }).then(r => r.data),
}

// ── 数据看板 ──
export const dashboardApi = {
  stats: () =>
    api.get<DashboardStats>('/dashboard/stats').then(r => r.data),
}

// ── OCR ──
export const ocrApi = {
  recognize: (file: File) => {
    const fd = new FormData()
    fd.append('file', file)
    return api.post('/ocr/recognize', fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }).then(r => r.data)
  },
}

// ── 导出 ──
export const exportApi = {
  pdf: (subject?: string) =>
    api.get('/export/pdf', { params: { subject }, responseType: 'blob' }).then(r => r.data),
  markdown: (subject?: string) =>
    api.get('/export/markdown', { params: { subject }, responseType: 'text' }).then(r => r.data),
}
