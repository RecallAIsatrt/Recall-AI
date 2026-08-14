import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/mistakes' },
    {
      path: '/mistakes',
      name: 'mistakes',
      component: () => import('@/views/MistakeView.vue'),
      meta: { title: '错题集' },
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('@/views/ChatView.vue'),
      meta: { title: 'AI答疑' },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: { title: '数据看板' },
    },
    {
      path: '/help',
      name: 'help',
      component: () => import('@/views/HelpView.vue'),
      meta: { title: '帮助' },
    },
  ],
})

router.beforeEach((to) => {
  document.title = `Recall · ${to.meta.title || 'AI 智能错题本'}`
})

export default router
