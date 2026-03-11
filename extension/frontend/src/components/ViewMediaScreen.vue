<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  ArrowLeft, Calendar, Clock, Gauge, MapPin, User, Download,
  Trash2, ZoomIn, Image, Video, Play, FileText
} from 'lucide-vue-next'
import type { Screen, DiveData } from '../types'

interface MediaItem {
  id: number
  type: 'image' | 'video'
  url: string
  thumbnail: string
  timestamp: string
  depth: string
  duration?: string
}

const props = withDefaults(defineProps<{
  previousScreen?: Screen
  diveData?: DiveData | null
}>(), {
  previousScreen: 'media',
  diveData: null
})

const emit = defineEmits<{
  navigate: [screen: Screen]
}>()

const lightboxIndex = ref<number | null>(null)
const showDeleteModal = ref(false)

const currentDive = computed<DiveData>(() => props.diveData ?? {
  name: 'Deep Sea Survey 2024-01',
  date: 'Jan 5, 2026',
  duration: '3h 45m',
  maxDepth: '125m',
  location: '41.7128° N, 74.0060° W',
  operator: 'Dr. Sarah Chen',
  images: 487,
  videos: 3
})

const mediaItems = ref<MediaItem[]>([
  { id: 1, type: 'image', url: 'https://images.unsplash.com/photo-1682687220742-aba13b6e50ba?w=1200', thumbnail: 'https://images.unsplash.com/photo-1682687220742-aba13b6e50ba?w=400', timestamp: '14:30:22 UTC', depth: '45m' },
  { id: 2, type: 'image', url: 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1200', thumbnail: 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400', timestamp: '14:32:15 UTC', depth: '52m' },
  { id: 3, type: 'video', url: 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=1200', thumbnail: 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400', timestamp: '14:35:30 UTC', depth: '58m', duration: '2:34' },
  { id: 4, type: 'image', url: 'https://images.unsplash.com/photo-1583212292454-1fe6229603b7?w=1200', thumbnail: 'https://images.unsplash.com/photo-1583212292454-1fe6229603b7?w=400', timestamp: '14:38:45 UTC', depth: '63m' },
  { id: 5, type: 'image', url: 'https://images.unsplash.com/photo-1546026423-cc4642628d2b?w=1200', thumbnail: 'https://images.unsplash.com/photo-1546026423-cc4642628d2b?w=400', timestamp: '14:42:10 UTC', depth: '71m' },
  { id: 6, type: 'video', url: 'https://images.unsplash.com/photo-1551244072-5d12893278ab?w=1200', thumbnail: 'https://images.unsplash.com/photo-1551244072-5d12893278ab?w=400', timestamp: '14:45:00 UTC', depth: '78m', duration: '5:12' },
  { id: 7, type: 'image', url: 'https://images.unsplash.com/photo-1571752726703-5e7d1f6a986d?w=1200', thumbnail: 'https://images.unsplash.com/photo-1571752726703-5e7d1f6a986d?w=400', timestamp: '14:50:22 UTC', depth: '85m' },
  { id: 8, type: 'image', url: 'https://images.unsplash.com/photo-1596436889106-be35e843f974?w=1200', thumbnail: 'https://images.unsplash.com/photo-1596436889106-be35e843f974?w=400', timestamp: '14:55:30 UTC', depth: '92m' },
  { id: 9, type: 'image', url: 'https://images.unsplash.com/photo-1582967788606-a171c7a0a87d?w=1200', thumbnail: 'https://images.unsplash.com/photo-1582967788606-a171c7a0a87d?w=400', timestamp: '15:00:45 UTC', depth: '98m' },
  { id: 10, type: 'video', url: 'https://images.unsplash.com/photo-1437622368342-7a3d73a34c8f?w=1200', thumbnail: 'https://images.unsplash.com/photo-1437622368342-7a3d73a34c8f?w=400', timestamp: '15:05:00 UTC', depth: '105m', duration: '3:45' },
  { id: 11, type: 'image', url: 'https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=1200', thumbnail: 'https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=400', timestamp: '15:10:15 UTC', depth: '110m' },
  { id: 12, type: 'image', url: 'https://images.unsplash.com/photo-1535591273668-578e31182c4f?w=1200', thumbnail: 'https://images.unsplash.com/photo-1535591273668-578e31182c4f?w=400', timestamp: '15:15:30 UTC', depth: '115m' },
  { id: 13, type: 'image', url: 'https://images.unsplash.com/photo-1504472478235-9bc48ba4d60f?w=1200', thumbnail: 'https://images.unsplash.com/photo-1504472478235-9bc48ba4d60f?w=400', timestamp: '15:18:00 UTC', depth: '118m' },
  { id: 14, type: 'video', url: 'https://images.unsplash.com/photo-1560275619-4662e36fa65c?w=1200', thumbnail: 'https://images.unsplash.com/photo-1560275619-4662e36fa65c?w=400', timestamp: '15:22:10 UTC', depth: '120m', duration: '1:58' },
  { id: 15, type: 'image', url: 'https://images.unsplash.com/photo-1497290756760-23ac55edf36f?w=1200', thumbnail: 'https://images.unsplash.com/photo-1497290756760-23ac55edf36f?w=400', timestamp: '15:25:45 UTC', depth: '122m' },
  { id: 16, type: 'image', url: 'https://images.unsplash.com/photo-1580019542155-247062e19ce4?w=1200', thumbnail: 'https://images.unsplash.com/photo-1580019542155-247062e19ce4?w=400', timestamp: '15:30:00 UTC', depth: '124m' },
  { id: 17, type: 'image', url: 'https://images.unsplash.com/photo-1682687982501-1e58ab814714?w=1200', thumbnail: 'https://images.unsplash.com/photo-1682687982501-1e58ab814714?w=400', timestamp: '15:32:30 UTC', depth: '125m' },
  { id: 18, type: 'image', url: 'https://images.unsplash.com/photo-1505118380757-91f5f5632de0?w=1200', thumbnail: 'https://images.unsplash.com/photo-1505118380757-91f5f5632de0?w=400', timestamp: '15:35:00 UTC', depth: '125m' }
])

const lightboxItem = computed(() => {
  if (lightboxIndex.value === null) return null
  return mediaItems.value[lightboxIndex.value]
})

const openLightbox = (index: number) => {
  lightboxIndex.value = index
}

const closeLightbox = () => {
  lightboxIndex.value = null
}

const prevImage = () => {
  if (lightboxIndex.value !== null && lightboxIndex.value > 0) {
    lightboxIndex.value--
  }
}

const nextImage = () => {
  if (lightboxIndex.value !== null && lightboxIndex.value < mediaItems.value.length - 1) {
    lightboxIndex.value++
  }
}

const handleKeydown = (e: KeyboardEvent) => {
  if (lightboxIndex.value === null) return
  if (e.key === 'ArrowLeft') prevImage()
  if (e.key === 'ArrowRight') nextImage()
  if (e.key === 'Escape') closeLightbox()
}

const confirmDelete = () => {
  showDeleteModal.value = true
}

const executeDelete = () => {
  showDeleteModal.value = false
  emit('navigate', props.previousScreen)
}

const cancelDelete = () => {
  showDeleteModal.value = false
}

const goBack = () => {
  emit('navigate', props.previousScreen)
}

const imageCount = computed(() => mediaItems.value.filter(m => m.type === 'image').length)
const videoCount = computed(() => mediaItems.value.filter(m => m.type === 'video').length)
</script>

<template>
  <div
    class="max-w-7xl mx-auto px-4 py-6 md:py-8"
    @keydown="handleKeydown"
    tabindex="0"
  >
    <!-- Back Button -->
    <button
      @click="goBack"
      class="flex items-center gap-2 mb-6 transition-colors hover:opacity-80"
      style="color: #41B9C3"
    >
      <ArrowLeft class="w-5 h-5" />
      <span>Back</span>
    </button>

    <!-- Dive Information Card -->
    <div
      class="backdrop-blur-sm rounded-xl p-6 border mb-6"
      style="background-color: rgba(0, 77, 100, 0.4); border-color: rgba(65, 185, 195, 0.3)"
    >
      <div class="flex flex-col md:flex-row md:items-start justify-between gap-4 mb-4">
        <div class="flex items-center gap-3 flex-wrap">
          <h1 class="text-white text-2xl font-medium">{{ currentDive.name }}</h1>
          <span
            class="px-2.5 py-0.5 rounded-full text-xs font-medium"
            style="background-color: rgba(0, 212, 170, 0.2); color: #00D4AA; border: 1px solid rgba(0, 212, 170, 0.4)"
          >
            Completed
          </span>
        </div>
        <div class="flex flex-wrap gap-2">
          <button
            class="px-3 py-1.5 text-sm rounded-lg transition-all hover:opacity-90 flex items-center gap-1.5"
            style="background: linear-gradient(135deg, #FF9937 0%, #FF621D 100%); color: white"
          >
            <Download class="w-3.5 h-3.5" />
            Download All
          </button>
          <button
            class="px-3 py-1.5 text-sm rounded-lg transition-all hover:opacity-90 flex items-center gap-1.5"
            style="background: linear-gradient(135deg, #41B9C3 0%, #187D8B 100%); color: white"
          >
            <FileText class="w-3.5 h-3.5" />
            Open Log
          </button>
          <button
            @click="confirmDelete"
            class="px-3 py-1.5 text-sm rounded-lg transition-all hover:opacity-90 flex items-center gap-1.5"
            style="background-color: rgba(255, 71, 87, 0.15); color: #FF4757; border: 1px solid rgba(255, 71, 87, 0.3)"
          >
            <Trash2 class="w-3.5 h-3.5" />
            Delete Dive
          </button>
        </div>
      </div>

      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <div class="flex items-center gap-2">
          <Calendar class="w-4 h-4 flex-shrink-0" style="color: #41B9C3" />
          <div>
            <p class="text-xs" style="color: #96EEF2">Date</p>
            <p class="text-white text-sm">{{ currentDive.date }}</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <Clock class="w-4 h-4 flex-shrink-0" style="color: #41B9C3" />
          <div>
            <p class="text-xs" style="color: #96EEF2">Duration</p>
            <p class="text-white text-sm">{{ currentDive.duration }}</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <Gauge class="w-4 h-4 flex-shrink-0" style="color: #41B9C3" />
          <div>
            <p class="text-xs" style="color: #96EEF2">Max Depth</p>
            <p class="text-white text-sm">{{ currentDive.maxDepth }}</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <MapPin class="w-4 h-4 flex-shrink-0" style="color: #41B9C3" />
          <div>
            <p class="text-xs" style="color: #96EEF2">Location</p>
            <p class="text-white text-sm">{{ currentDive.location }}</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <User class="w-4 h-4 flex-shrink-0" style="color: #41B9C3" />
          <div>
            <p class="text-xs" style="color: #96EEF2">Operator</p>
            <p class="text-white text-sm">{{ currentDive.operator ?? 'N/A' }}</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <Image class="w-4 h-4 flex-shrink-0" style="color: #41B9C3" />
          <div>
            <p class="text-xs" style="color: #96EEF2">Media</p>
            <p class="text-white text-sm">{{ imageCount }} img / {{ videoCount }} vid</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Media Gallery -->
    <div
      class="backdrop-blur-sm rounded-xl p-6 border"
      style="background-color: rgba(0, 77, 100, 0.4); border-color: rgba(65, 185, 195, 0.3)"
    >
      <h2 class="text-white text-xl mb-4 flex items-center gap-2">
        <Image class="w-5 h-5" style="color: #96EEF2" />
        Media Gallery
      </h2>

      <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 xl:grid-cols-8 gap-2">
        <div
          v-for="(item, index) in mediaItems"
          :key="item.id"
          class="relative group cursor-pointer aspect-square rounded-lg overflow-hidden"
          style="background-color: rgba(14, 36, 70, 0.5)"
          @click="openLightbox(index)"
        >
          <img
            :src="item.thumbnail"
            :alt="`Media ${item.id}`"
            class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
            loading="lazy"
          />
          <!-- Hover Overlay -->
          <div class="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-all duration-300 flex items-center justify-center">
            <ZoomIn class="w-6 h-6 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
          </div>
          <!-- Video Badge -->
          <div
            v-if="item.type === 'video'"
            class="absolute bottom-1 left-1 flex items-center gap-1 px-1.5 py-0.5 rounded text-xs"
            style="background-color: rgba(0, 0, 0, 0.7); color: white"
          >
            <Play class="w-3 h-3" />
            {{ item.duration }}
          </div>
          <!-- Type Icon -->
          <div
            v-if="item.type === 'video'"
            class="absolute top-1 right-1 w-6 h-6 rounded-full flex items-center justify-center"
            style="background-color: rgba(168, 85, 247, 0.8)"
          >
            <Video class="w-3 h-3 text-white" />
          </div>
        </div>
      </div>
    </div>

    <!-- Lightbox Modal -->
    <Teleport to="body">
      <div
        v-if="lightboxItem"
        class="fixed inset-0 z-50 flex items-center justify-center"
        style="background-color: rgba(0, 0, 0, 0.9)"
        @click.self="closeLightbox"
        @keydown="handleKeydown"
      >
        <!-- Close Button -->
        <button
          @click="closeLightbox"
          class="absolute top-4 right-4 w-10 h-10 rounded-full flex items-center justify-center text-white transition-colors z-10"
          style="background-color: rgba(255, 255, 255, 0.1)"
        >
          &times;
        </button>

        <!-- Previous -->
        <button
          v-if="lightboxIndex !== null && lightboxIndex > 0"
          @click.stop="prevImage"
          class="absolute left-4 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full flex items-center justify-center text-white transition-colors z-10"
          style="background-color: rgba(255, 255, 255, 0.1)"
        >
          <ArrowLeft class="w-5 h-5" />
        </button>

        <!-- Next -->
        <button
          v-if="lightboxIndex !== null && lightboxIndex < mediaItems.length - 1"
          @click.stop="nextImage"
          class="absolute right-4 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full flex items-center justify-center text-white transition-colors rotate-180 z-10"
          style="background-color: rgba(255, 255, 255, 0.1)"
        >
          <ArrowLeft class="w-5 h-5" />
        </button>

        <!-- Image -->
        <div class="max-w-5xl max-h-[85vh] flex flex-col items-center">
          <img
            :src="lightboxItem.url"
            :alt="`Media ${lightboxItem.id}`"
            class="max-w-full max-h-[75vh] object-contain rounded-lg"
          />
          <!-- Info Bar -->
          <div
            class="mt-3 px-4 py-2 rounded-lg flex items-center gap-6 text-sm"
            style="background-color: rgba(14, 36, 70, 0.8); border: 1px solid rgba(65, 185, 195, 0.3)"
          >
            <div class="flex items-center gap-1.5">
              <Clock class="w-3.5 h-3.5" style="color: #41B9C3" />
              <span style="color: #96EEF2">{{ lightboxItem.timestamp }}</span>
            </div>
            <div class="flex items-center gap-1.5">
              <Gauge class="w-3.5 h-3.5" style="color: #41B9C3" />
              <span style="color: #96EEF2">Depth: {{ lightboxItem.depth }}</span>
            </div>
            <span style="color: rgba(150, 238, 242, 0.5)">
              {{ (lightboxIndex ?? 0) + 1 }} / {{ mediaItems.length }}
            </span>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Delete Confirmation Modal -->
    <Teleport to="body">
      <div
        v-if="showDeleteModal"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        style="background-color: rgba(0, 0, 0, 0.7)"
        @click.self="cancelDelete"
      >
        <div
          class="rounded-xl p-6 max-w-md w-full border"
          style="background-color: #0E2446; border-color: rgba(255, 71, 87, 0.4)"
        >
          <div class="flex items-center gap-3 mb-4">
            <div
              class="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0"
              style="background-color: rgba(255, 71, 87, 0.2)"
            >
              <Trash2 class="w-5 h-5" style="color: #FF4757" />
            </div>
            <h3 class="text-white text-lg font-medium">Delete Dive</h3>
          </div>
          <p class="mb-2" style="color: #96EEF2">
            Are you sure you want to delete
            <span class="text-white font-medium">{{ currentDive.name }}</span>?
          </p>
          <p class="text-sm mb-6" style="color: rgba(150, 238, 242, 0.6)">
            This will permanently remove all media files and associated data. This action cannot be undone.
          </p>
          <div class="flex gap-3 justify-end">
            <button
              @click="cancelDelete"
              class="px-4 py-2 rounded-lg transition-all"
              style="background-color: rgba(14, 36, 70, 0.5); color: #96EEF2; border: 1px solid rgba(65, 185, 195, 0.3)"
            >
              Cancel
            </button>
            <button
              @click="executeDelete"
              class="px-4 py-2 rounded-lg transition-all hover:opacity-90 flex items-center gap-2"
              style="background-color: #FF4757; color: white"
            >
              <Trash2 class="w-4 h-4" />
              Delete Dive
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
