<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  Database, Calendar, Clock, MapPin, Camera, Image, FileText, Play,
  Download, Settings, Trash2, AlertTriangle, Archive, Search, X, Gauge
} from 'lucide-vue-next'
import type { Screen, DiveData, Mission } from '../types'

const emit = defineEmits<{
  navigate: [screen: Screen, diveData?: DiveData]
}>()

const selectedMission = ref<number | null>(null)
const nameFilter = ref('')
const dateSort = ref<'recent' | 'oldest'>('recent')

const previousMissions: Mission[] = [
  {
    id: 1,
    name: 'DeepSeaSurvey_20260105143022',
    configuration: 'DORIS 6 Hour Dive Configuration',
    date: 'Jan 5, 2026',
    duration: '3h 45m',
    location: '41.7128° N, 74.0060° W',
    maxDepth: 125,
    images: 487,
    videos: 3,
    status: 'completed',
    calibrationFiles: {
      camera: 'CAM_CAL_20260105_v2.3.cal',
      depthSensor: 'DEPTH_CAL_20251220_v1.8.cal',
      temperature: 'TEMP_CAL_20260102_v3.1.cal',
      conductivity: 'COND_CAL_20251215_v2.0.cal',
      imu: 'IMU_CAL_20260101_v4.2.cal'
    }
  },
  {
    id: 2,
    name: 'CoralReefDoc_20260102091530',
    configuration: 'DORIS 4 Hour Dive Configuration',
    date: 'Jan 2, 2026',
    duration: '2h 18m',
    location: '25.7617° N, 80.1918° W',
    maxDepth: 45,
    images: 324,
    videos: 5,
    status: 'completed',
    calibrationFiles: {
      camera: 'CAM_CAL_20260101_v2.3.cal',
      depthSensor: 'DEPTH_CAL_20251220_v1.8.cal',
      temperature: 'TEMP_CAL_20260102_v3.1.cal',
      conductivity: 'COND_CAL_20251215_v2.0.cal',
      imu: 'IMU_CAL_20260101_v4.2.cal'
    }
  },
  {
    id: 3,
    name: 'KelpForestStudy_20251228103045',
    configuration: 'DORIS 6 Hour Dive Configuration',
    date: 'Dec 28, 2025',
    duration: '4h 12m',
    location: '36.6002° N, 121.8947° W',
    maxDepth: 78,
    images: 612,
    videos: 7,
    status: 'completed',
    calibrationFiles: {
      camera: 'CAM_CAL_20251220_v2.2.cal',
      depthSensor: 'DEPTH_CAL_20251220_v1.8.cal',
      temperature: 'TEMP_CAL_20251215_v3.0.cal',
      conductivity: 'COND_CAL_20251215_v2.0.cal',
      imu: 'IMU_CAL_20251222_v4.1.cal'
    }
  },
  {
    id: 4,
    name: 'ShipwreckInv_20251220074512',
    configuration: 'DORIS 12 Hour Dive Configuration',
    date: 'Dec 20, 2025',
    duration: '5h 30m',
    location: '42.3601° N, 71.0589° W',
    maxDepth: 156,
    images: 893,
    videos: 12,
    status: 'completed',
    calibrationFiles: {
      camera: 'CAM_CAL_20251220_v2.2.cal',
      depthSensor: 'DEPTH_CAL_20251220_v1.8.cal',
      temperature: 'TEMP_CAL_20251215_v3.0.cal',
      conductivity: 'COND_CAL_20251210_v1.9.cal',
      imu: 'IMU_CAL_20251218_v4.0.cal'
    }
  },
  {
    id: 5,
    name: 'BioLuminescence_20251215195520',
    configuration: 'DORIS 12 Hour Dive Configuration',
    date: 'Dec 15, 2025',
    duration: '6h 05m',
    location: '32.7157° N, 117.1611° W',
    maxDepth: 98,
    images: 1247,
    videos: 8,
    status: 'completed',
    calibrationFiles: {
      camera: 'CAM_CAL_20251210_v2.1.cal',
      depthSensor: 'DEPTH_CAL_20251205_v1.7.cal',
      temperature: 'TEMP_CAL_20251215_v3.0.cal',
      conductivity: 'COND_CAL_20251210_v1.9.cal',
      imu: 'IMU_CAL_20251212_v4.0.cal'
    }
  }
]

const filteredMissions = computed(() => {
  return previousMissions
    .filter(mission => mission.name.toLowerCase().includes(nameFilter.value.toLowerCase()))
    .sort((a, b) => {
      const dateA = new Date(a.date).getTime()
      const dateB = new Date(b.date).getTime()
      return dateSort.value === 'recent' ? dateB - dateA : dateA - dateB
    })
})

const handleViewMedia = (mission: Mission) => {
  const diveData: DiveData = {
    name: mission.name,
    date: mission.date,
    duration: mission.duration,
    maxDepth: `${mission.maxDepth}m`,
    location: mission.location,
    images: mission.images,
    videos: mission.videos
  }
  emit('navigate', 'viewmedia', diveData)
}
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-6 md:py-8">
    <div
      class="backdrop-blur-sm rounded-xl p-6 border"
      style="background-color: rgba(0, 77, 100, 0.4); border-color: rgba(65, 185, 195, 0.3)"
    >
      <h1 class="text-white text-2xl mb-6 flex items-center gap-2">
        <Database class="w-6 h-6" style="color: #96EEF2" />
        Previous Dives
      </h1>

      <!-- Filter Section -->
      <div class="mb-6 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm mb-2" style="color: #96EEF2">Filter by Name</label>
          <div class="relative">
            <Search
              class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4"
              style="color: #41B9C3"
            />
            <input
              v-model="nameFilter"
              type="text"
              placeholder="Search dive name..."
              class="w-full pl-10 pr-10 py-2 rounded-lg text-white placeholder-gray-400 focus:outline-none"
              style="background-color: rgba(14, 36, 70, 0.7); border: 1px solid rgba(65, 185, 195, 0.3)"
            />
            <button
              v-if="nameFilter"
              @click="nameFilter = ''"
              class="absolute right-3 top-1/2 transform -translate-y-1/2 hover:opacity-70 transition-opacity"
            >
              <X class="w-4 h-4" style="color: #96EEF2" />
            </button>
          </div>
        </div>

        <div>
          <label class="block text-sm mb-2" style="color: #96EEF2">Sort by Date</label>
          <div class="relative">
            <Calendar
              class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4"
              style="color: #41B9C3"
            />
            <select
              v-model="dateSort"
              class="w-full pl-10 pr-4 py-2 rounded-lg text-white focus:outline-none appearance-none cursor-pointer"
              style="background-color: rgba(14, 36, 70, 0.7); border: 1px solid rgba(65, 185, 195, 0.3)"
            >
              <option value="recent">Recent</option>
              <option value="oldest">Oldest</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Results Count -->
      <div
        v-if="nameFilter"
        class="mb-4 text-sm"
        style="color: #96EEF2"
      >
        Showing {{ filteredMissions.length }} of {{ previousMissions.length }} dives
      </div>

      <!-- No Results -->
      <div
        v-if="filteredMissions.length === 0"
        class="rounded-lg p-8 text-center"
        style="background-color: rgba(14, 36, 70, 0.5); border: 1px solid rgba(65, 185, 195, 0.2)"
      >
        <Search class="w-12 h-12 mx-auto mb-3" style="color: #41B9C3; opacity: 0.5" />
        <p class="text-white text-lg mb-2">No dives found</p>
        <p class="text-sm" style="color: #96EEF2">Try adjusting your filters</p>
      </div>

      <!-- Dives List -->
      <div class="space-y-3">
        <div
          v-for="mission in filteredMissions"
          :key="mission.id"
          class="rounded-lg p-5 transition-all hover:bg-slate-700/50"
          style="background-color: rgba(14, 36, 70, 0.5); border: 1px solid rgba(65, 185, 195, 0.2)"
        >
          <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
            <div class="flex-1 min-w-0">
              <!-- Name + Status -->
              <div class="flex flex-wrap items-center gap-2 sm:gap-3 mb-3">
                <h3 class="text-white text-base sm:text-lg break-all">{{ mission.name }}</h3>
                <span
                  class="px-2 py-1 rounded text-xs flex-shrink-0"
                  style="background-color: rgba(252, 216, 105, 0.2); color: #FCD869"
                >
                  {{ mission.status }}
                </span>
              </div>

              <!-- Info Grid -->
              <div class="grid grid-cols-1 md:grid-cols-4 gap-3 mb-3">
                <div class="flex items-center gap-2">
                  <Calendar class="w-4 h-4" style="color: #96EEF2" />
                  <span class="text-sm" style="color: #96EEF2">{{ mission.date }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <Clock class="w-4 h-4" style="color: #96EEF2" />
                  <span class="text-sm" style="color: #96EEF2">{{ mission.duration }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <MapPin class="w-4 h-4" style="color: #96EEF2" />
                  <span class="text-sm" style="color: #96EEF2">{{ mission.location }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-sm" style="color: #96EEF2">Max Depth: {{ mission.maxDepth }}m</span>
                </div>
              </div>

              <!-- Configuration -->
              <div class="mb-3">
                <div class="flex items-center gap-2">
                  <Settings class="w-4 h-4" style="color: #96EEF2" />
                  <span class="text-sm" style="color: #96EEF2">Configuration: {{ mission.configuration }}</span>
                </div>
              </div>

              <!-- Media Counts -->
              <div class="flex items-center gap-4">
                <div class="flex items-center gap-2">
                  <Camera class="w-4 h-4" style="color: #41B9C3" />
                  <span class="text-sm" style="color: #96EEF2">{{ mission.images }} images</span>
                </div>
                <div class="flex items-center gap-2">
                  <Image class="w-4 h-4" style="color: #41B9C3" />
                  <span class="text-sm" style="color: #96EEF2">{{ mission.videos }} videos</span>
                </div>
              </div>

              <!-- Calibration Files -->
              <div
                class="mt-4 rounded-lg p-3"
                style="background-color: rgba(65, 185, 195, 0.1); border: 1px solid rgba(65, 185, 195, 0.2)"
              >
                <div class="flex items-center gap-2 mb-2">
                  <Gauge class="w-4 h-4" style="color: #41B9C3" />
                  <span class="text-sm font-semibold" style="color: #96EEF2">
                    Sensor Calibration Files
                  </span>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs" style="color: #96EEF2">
                  <div class="flex items-start gap-1.5">
                    <span class="opacity-70">Camera:</span>
                    <span class="font-mono text-xs break-all">{{ mission.calibrationFiles.camera }}</span>
                  </div>
                  <div class="flex items-start gap-1.5">
                    <span class="opacity-70">Depth:</span>
                    <span class="font-mono text-xs break-all">{{ mission.calibrationFiles.depthSensor }}</span>
                  </div>
                  <div class="flex items-start gap-1.5">
                    <span class="opacity-70">Temp:</span>
                    <span class="font-mono text-xs break-all">{{ mission.calibrationFiles.temperature }}</span>
                  </div>
                  <div class="flex items-start gap-1.5">
                    <span class="opacity-70">Conductivity:</span>
                    <span class="font-mono text-xs break-all">{{ mission.calibrationFiles.conductivity }}</span>
                  </div>
                  <div class="flex items-start gap-1.5">
                    <span class="opacity-70">IMU:</span>
                    <span class="font-mono text-xs break-all">{{ mission.calibrationFiles.imu }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Action Buttons (vertical stack on right) -->
            <div class="flex flex-col gap-2 flex-shrink-0">
              <button
                class="px-4 py-2 rounded-lg transition-all hover:opacity-90 flex items-center gap-2 text-sm whitespace-nowrap"
                style="background-color: #41B9C3; color: white"
              >
                <FileText class="w-4 h-4" />
                View Log File
              </button>
              <button
                class="px-4 py-2 rounded-lg transition-all hover:opacity-90 flex items-center gap-2 text-sm whitespace-nowrap"
                style="background-color: #96EEF2; color: #0E2446"
              >
                <Database class="w-4 h-4" />
                View Data Files
              </button>
              <button
                class="px-4 py-2 rounded-lg transition-all hover:opacity-90 flex items-center gap-2 text-sm whitespace-nowrap"
                style="background-color: #FF9937; color: white"
                @click="handleViewMedia(mission)"
              >
                <Play class="w-4 h-4" />
                View Media
              </button>
              <button
                class="px-4 py-2 rounded-lg transition-all hover:opacity-90 flex items-center gap-2 text-sm whitespace-nowrap"
                style="background-color: rgba(65, 185, 195, 0.3); border: 1px solid #41B9C3; color: #96EEF2"
              >
                <Download class="w-4 h-4" />
                Download Media
              </button>
              <button
                class="px-4 py-2 rounded-lg transition-all hover:opacity-90 flex items-center gap-2 text-sm whitespace-nowrap"
                style="background-color: rgba(65, 185, 195, 0.2); border: 1px solid #41B9C3; color: #41B9C3"
              >
                <Archive class="w-4 h-4" />
                Download All Files
              </button>
              <button
                class="px-4 py-2 rounded-lg transition-all hover:opacity-90 flex items-center gap-2 text-sm whitespace-nowrap"
                style="background-color: rgba(221, 44, 29, 0.2); border: 1px solid #DD2C1D; color: #DD2C1D"
                @click="selectedMission = mission.id"
              >
                <Trash2 class="w-4 h-4" />
                Delete Dive
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <Teleport to="body">
      <div
        v-if="selectedMission !== null"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        style="background-color: rgba(0, 0, 0, 0.7)"
        @click.self="selectedMission = null"
      >
        <div
          class="rounded-xl p-6 max-w-md w-full border shadow-2xl"
          style="background-color: #0E2446; border-color: #DD2C1D"
          @click.stop
        >
          <div class="flex items-start gap-4 mb-4">
            <div class="p-3 rounded-lg" style="background-color: rgba(221, 44, 29, 0.2)">
              <AlertTriangle class="w-6 h-6" style="color: #DD2C1D" />
            </div>
            <div class="flex-1">
              <h3 class="text-white text-xl mb-2">Delete Dive?</h3>
              <p style="color: #96EEF2" class="text-sm mb-2">
                Are you sure you want to delete this dive? This action cannot be undone.
              </p>
              <div class="rounded p-3 mt-3" style="background-color: rgba(65, 185, 195, 0.1)">
                <p class="text-white font-semibold mb-1">
                  {{ previousMissions.find(m => m.id === selectedMission)?.name }}
                </p>
                <p style="color: #96EEF2" class="text-xs">
                  {{ previousMissions.find(m => m.id === selectedMission)?.images }} images,
                  {{ previousMissions.find(m => m.id === selectedMission)?.videos }} videos
                </p>
              </div>
            </div>
          </div>

          <div class="flex gap-3 mt-6">
            <button
              @click="selectedMission = null"
              class="flex-1 px-4 py-2 rounded-lg transition-all hover:opacity-80"
              style="background-color: rgba(65, 185, 195, 0.3); border: 1px solid #41B9C3; color: #96EEF2"
            >
              Cancel
            </button>
            <button
              @click="selectedMission = null"
              class="flex-1 px-4 py-2 rounded-lg transition-all hover:opacity-90 flex items-center justify-center gap-2"
              style="background-color: #DD2C1D; color: white"
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
