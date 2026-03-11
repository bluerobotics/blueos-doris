<script setup lang="ts">
import { ref, computed } from 'vue'
import { Home, Wifi, Compass, Gauge, Database, Bell, HelpCircle, List, Menu, X } from 'lucide-vue-next'
import type { Screen } from '../types'

interface Props {
  currentScreen: Screen
  notificationCount?: number
}

const props = withDefaults(defineProps<Props>(), {
  notificationCount: 3
})

const emit = defineEmits<{
  navigate: [screen: Screen]
}>()

const mobileMenuOpen = ref(false)

const navItems = computed(() => [
  { id: 'home' as Screen, icon: Home, label: 'Dashboard', enabled: true },
  { id: 'dives' as Screen, icon: Compass, label: 'Configuration', enabled: true },
  { id: 'alldives' as Screen, icon: List, label: 'Previous Dives', enabled: true },
  { id: 'sensors' as Screen, icon: Gauge, label: 'Sensors', enabled: true },
  { id: 'media' as Screen, icon: Database, label: 'Data', enabled: true },
  { id: 'network' as Screen, icon: Wifi, label: 'Network', enabled: true },
  { id: 'notifications' as Screen, icon: Bell, label: 'Notifications', badge: props.notificationCount, enabled: true },
  { id: 'help' as Screen, icon: HelpCircle, label: 'Help', enabled: true },
])

const handleMobileNavigate = (screen: Screen) => {
  emit('navigate', screen)
  mobileMenuOpen.value = false
}
</script>

<template>
  <!-- Desktop Navigation -->
  <nav
    class="hidden md:flex items-center justify-between px-4 py-3 border-b"
    style="background-color: rgba(14, 36, 70, 0.8); backdrop-filter: blur(8px); border-color: rgba(65, 185, 195, 0.2)"
  >
    <button
      @click="emit('navigate', 'home')"
      class="flex items-center gap-6 hover:opacity-80 transition-opacity mr-12"
    >
      <h1 class="text-white text-2xl" style="font-weight: 700; font-family: 'Montserrat', sans-serif">DORIS</h1>
    </button>
    <div class="flex items-center gap-2">
      <button
        v-for="item in navItems"
        :key="item.id"
        @click="item.enabled && emit('navigate', item.id)"
        class="flex items-center gap-2 px-4 py-2 rounded-lg transition-all"
        :class="[
          currentScreen === item.id ? 'text-white' : item.enabled ? 'hover:bg-slate-800' : 'cursor-not-allowed'
        ]"
        :style="currentScreen === item.id
          ? { backgroundColor: '#41B9C3', color: '#FFFFFF' }
          : { color: item.enabled ? '#96EEF2' : 'rgba(150, 238, 242, 0.3)', opacity: item.enabled ? 1 : 0.5 }"
        :disabled="!item.enabled"
      >
        <component :is="item.icon" class="w-4 h-4" />
        <span v-if="item.id !== 'notifications'" class="text-sm">{{ item.label }}</span>
        <span
          v-if="item.badge && item.badge > 0"
          class="ml-1 text-xs px-1.5 py-0.5 rounded-full"
          style="background-color: #DD2C1D; color: white; min-width: 20px; text-align: center"
        >
          {{ item.badge }}
        </span>
      </button>
    </div>
  </nav>

  <!-- Mobile Navigation Header -->
  <nav
    class="md:hidden flex items-center justify-between px-4 py-3 border-b"
    style="background-color: rgba(14, 36, 70, 0.95); backdrop-filter: blur(8px); border-color: rgba(65, 185, 195, 0.2)"
  >
    <button
      @click="emit('navigate', 'home')"
      class="flex items-center hover:opacity-80 transition-opacity"
    >
      <h1 class="text-white text-2xl" style="font-weight: 700; font-family: 'Montserrat', sans-serif">DORIS</h1>
    </button>
    <button
      @click="mobileMenuOpen = !mobileMenuOpen"
      class="relative p-2 rounded-lg transition-all"
      style="color: #96EEF2"
    >
      <X v-if="mobileMenuOpen" class="w-6 h-6" />
      <Menu v-else class="w-6 h-6" />
      <span
        v-if="notificationCount > 0 && !mobileMenuOpen"
        class="absolute top-1 right-1 text-xs px-1.5 py-0.5 rounded-full"
        style="background-color: #DD2C1D; color: white; min-width: 18px; text-align: center; font-size: 10px"
      >
        {{ notificationCount }}
      </span>
    </button>
  </nav>

  <!-- Mobile Menu Dropdown -->
  <template v-if="mobileMenuOpen">
    <div
      class="md:hidden fixed inset-0 bg-black bg-opacity-50 z-40"
      @click="mobileMenuOpen = false"
    />
    <div
      class="md:hidden fixed top-[57px] left-0 right-0 z-50 border-b"
      style="background-color: rgba(14, 36, 70, 0.98); backdrop-filter: blur(8px); border-color: rgba(65, 185, 195, 0.2); max-height: calc(100vh - 57px); overflow-y: auto"
    >
      <div class="py-2">
        <button
          v-for="item in navItems"
          :key="item.id"
          @click="item.enabled && handleMobileNavigate(item.id)"
          class="w-full flex items-center gap-3 px-4 py-3 transition-all"
          :class="currentScreen === item.id ? 'text-white' : ''"
          :style="currentScreen === item.id
            ? { backgroundColor: '#41B9C3', color: '#FFFFFF' }
            : { color: item.enabled ? '#96EEF2' : 'rgba(150, 238, 242, 0.3)', opacity: item.enabled ? 1 : 0.5 }"
          :disabled="!item.enabled"
        >
          <component :is="item.icon" class="w-5 h-5" />
          <span class="text-base">{{ item.label }}</span>
          <span
            v-if="item.badge && item.badge > 0"
            class="ml-auto text-xs px-2 py-1 rounded-full"
            style="background-color: #DD2C1D; color: white; min-width: 24px; text-align: center"
          >
            {{ item.badge }}
          </span>
        </button>
      </div>
    </div>
  </template>
</template>
