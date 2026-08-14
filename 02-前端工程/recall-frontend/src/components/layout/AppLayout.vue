<script setup lang="ts">
import TopBar from './TopBar.vue'
import Sidebar from './Sidebar.vue'
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <div class="flex flex-col h-screen bg-surface-secondary">
    <!-- Mac 风格顶部菜单栏 -->
    <TopBar />

    <div class="flex flex-1 overflow-hidden">
      <!-- 左侧边栏（桌面隐喻） -->
      <Sidebar v-if="route.name !== 'help'" />

      <!-- 主内容区 -->
      <main class="flex-1 overflow-y-auto p-2xl">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.fade-enter-from {
  opacity: 0;
  transform: translateY(4px);
}
.fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
