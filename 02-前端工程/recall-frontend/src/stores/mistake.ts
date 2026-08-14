/** 错题 Store */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Mistake, Category } from '@/types'
import { mistakesApi, categoriesApi } from '@/api'
import { CATEGORY_COLORS } from '@/types'

export const useMistakeStore = defineStore('mistake', () => {
  const mistakes = ref<Mistake[]>([])
  const categories = ref<Category[]>([])
  const activeCategory = ref<number | null>(null) // null = 全部
  const searchKeyword = ref('')
  const loading = ref(false)

  const filteredMistakes = computed(() => {
    let list = mistakes.value
    if (activeCategory.value !== null) {
      list = list.filter(m => m.category_id === activeCategory.value)
    }
    if (searchKeyword.value) {
      const kw = searchKeyword.value.toLowerCase()
      list = list.filter(m =>
        m.title.toLowerCase().includes(kw) ||
        m.content.toLowerCase().includes(kw) ||
        (m.knowledge_point || '').toLowerCase().includes(kw)
      )
    }
    return list
  })

  async function fetchMistakes() {
    loading.value = true
    try {
      mistakes.value = await mistakesApi.list()
    } finally {
      loading.value = false
    }
  }

  async function fetchCategories() {
    categories.value = await categoriesApi.list()
  }

  async function addMistake(data: Partial<Mistake>) {
    const m = await mistakesApi.create(data)
    mistakes.value.unshift(m)
    // 更新分类计数
    const cat = categories.value.find(c => c.id === m.category_id)
    if (cat) cat.mistake_count++
    return m
  }

  async function removeMistake(id: number) {
    const m = mistakes.value.find(x => x.id === id)
    await mistakesApi.delete(id)
    mistakes.value = mistakes.value.filter(x => x.id !== id)
    if (m) {
      const cat = categories.value.find(c => c.id === m.category_id)
      if (cat) cat.mistake_count = Math.max(0, cat.mistake_count - 1)
    }
  }

  async function updateMistake(id: number, data: Partial<Mistake>) {
    const m = await mistakesApi.update(id, data)
    const idx = mistakes.value.findIndex(x => x.id === id)
    if (idx >= 0) mistakes.value[idx] = m
    return m
  }

  async function addCategory(name: string) {
    const colorIdx = categories.value.length % CATEGORY_COLORS.length
    const cat = await categoriesApi.create({
      name,
      color: CATEGORY_COLORS[colorIdx],
    })
    categories.value.push(cat)
    return cat
  }

  async function removeCategory(id: number) {
    await categoriesApi.delete(id)
    categories.value = categories.value.filter(c => c.id !== id)
    if (activeCategory.value === id) activeCategory.value = null
  }

  return {
    mistakes, categories, activeCategory, searchKeyword, loading, filteredMistakes,
    fetchMistakes, fetchCategories, addMistake, removeMistake, updateMistake,
    addCategory, removeCategory,
  }
})
