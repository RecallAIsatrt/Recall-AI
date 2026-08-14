/** Recall 前端类型定义 */
export interface Category {
  id: number
  name: string
  color: string
  icon?: string
  mistake_count: number
  created_at: string
}

export interface Mistake {
  id: number
  title: string
  content: string
  source?: string
  subject: string
  knowledge_point?: string
  error_type?: string
  ai_analysis?: string
  image_url?: string
  category_id?: number
  review_count: number
  mastery_level: number
  next_review?: string
  is_archived: boolean
  created_at: string
  updated_at: string
}

export interface ChatSession {
  id: number
  title: string
  is_pinned: boolean
  created_at: string
  updated_at: string
}

export interface ChatMessage {
  id: number
  session_id: number
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

export interface ReviewRecord {
  id: number
  mistake_id: number
  quality: number
  easiness: number
  interval: number
  repetition: number
  review_at: string
}

export interface DashboardStats {
  total: number
  mastered: number
  pending: number
  avg_reviews: number
  subject_distribution: Record<string, number>
  weekly_trend: Array<{ date: string; count: number }>
  weak_points: Array<{ point: string; count: number }>
}

/** 学科配色映射（霓虹） */
export const SUBJECT_COLORS: Record<string, string> = {
  数学: '#60A5FA',
  物理: '#22D3EE',
  英语: '#FBBF24',
  化学: '#34D399',
  生物: '#C084FC',
  语文: '#F472B6',
  历史: '#818CF8',
  地理: '#FACC15',
}

/** 错题本 8 色列表（霓虹） */
export const CATEGORY_COLORS = [
  '#60A5FA', '#34D399', '#FBBF24', '#C084FC',
  '#F472B6', '#22D3EE', '#FACC15', '#818CF8',
]
