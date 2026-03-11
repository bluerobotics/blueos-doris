<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import {
  Gauge, Wifi, WifiOff, Settings, Upload, RefreshCw,
  Camera, Lightbulb, Thermometer, Waves, Activity, Wind, Satellite, Radio
} from 'lucide-vue-next'
import type { Screen, SensorModule } from '../types'

interface Props {
  targetSensor?: string | null
}

const props = withDefaults(defineProps<Props>(), {
  targetSensor: null
})

const emit = defineEmits<{
  navigate: [screen: Screen]
}>()

const modules = ref<SensorModule[]>([
  { id: 1, name: 'Camera', type: 'camera', connected: true, power: 20, moduleStatus: 'Ready: Active' },
  { id: 2, name: 'Conductivity', type: 'sensor', connected: true, power: 12, sampleRate: 1, calibrationFile: 'ctd_cal_2024.cal', moduleStatus: 'Ready: Active' },
  { id: 3, name: 'Temperature', type: 'sensor', connected: true, power: 12, sampleRate: 1, calibrationFile: 'ctd_cal_2024.cal', moduleStatus: 'Ready: Active' },
  { id: 4, name: 'Depth', type: 'sensor', connected: true, power: 12, sampleRate: 1, calibrationFile: 'ctd_cal_2024.cal', moduleStatus: 'Ready: Active' },
  { id: 5, name: 'Light', type: 'light', connected: true, power: 15, moduleStatus: 'Ready: Active' },
  { id: 6, name: 'Carbon Dioxide (CO₂)', type: 'sensor', connected: false, power: 0, sampleRate: 1, moduleStatus: 'Disconnected' },
  { id: 7, name: 'Oxygen (O₂)', type: 'sensor', connected: false, power: 0, sampleRate: 1, moduleStatus: 'Disconnected' },
  { id: 8, name: 'Iridium', type: 'communication', connected: true, power: 12, moduleStatus: 'Ready: Active' },
  { id: 9, name: 'LoRa', type: 'communication', connected: true, power: 9, moduleStatus: 'Ready: Active' },
])

const selectedModule = ref<SensorModule | null>(null)
const isDetecting = ref(false)
const moduleRefs = ref<Record<number, HTMLDivElement | null>>({})

const sensorMapping: Record<string, string> = {
  'Camera': 'Camera',
  'Light': 'Light',
  'Conductivity': 'Conductivity',
  'Temperature': 'Temperature',
  'Depth': 'Depth',
  'CO2': 'Carbon Dioxide (CO₂)',
  'O2': 'Oxygen (O₂)',
  'Iridium': 'Iridium',
  'LoRa': 'LoRa',
}

watch(() => props.targetSensor, (sensor) => {
  if (!sensor) return
  const mappedName = sensorMapping[sensor] || sensor
  const target = modules.value.find(m => m.name === mappedName)
  if (target) {
    selectedModule.value = target
    nextTick(() => {
      setTimeout(() => {
        moduleRefs.value[target.id]?.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }, 100)
    })
  }
}, { immediate: true })

const detectSensors = () => {
  isDetecting.value = true
  setTimeout(() => {
    isDetecting.value = false
    alert('Sensor detection complete. All modules refreshed.')
  }, 1500)
}

const toggleConnection = (id: number) => {
  modules.value = modules.value.map(m =>
    m.id === id ? { ...m, connected: !m.connected, power: !m.connected ? 85 : 0 } : m
  )
}

const setModuleRef = (id: number, el: HTMLDivElement | null) => {
  moduleRefs.value[id] = el
}

const getModuleIcon = (name: string) => {
  switch (name) {
    case 'Camera': return Camera
    case 'Conductivity': return Activity
    case 'Temperature': return Thermometer
    case 'Depth': return Waves
    case 'Light': return Lightbulb
    case 'Carbon Dioxide (CO₂)': return Wind
    case 'Oxygen (O₂)': return Wind
    case 'Iridium': return Satellite
    case 'LoRa': return Radio
    default: return Gauge
  }
}

const getStatusColor = (moduleStatus: string) => {
  if (moduleStatus.includes('Warning')) return '#FF9937'
  if (moduleStatus.includes('Disconnected')) return '#DD2C1D'
  return '#FCD869'
}
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-6 md:py-8">
    <div
      class="backdrop-blur-sm rounded-xl p-6 border"
      style="background-color: rgba(0, 77, 100, 0.4); border-color: rgba(65, 185, 195, 0.3)"
    >
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <h1 class="text-white text-2xl flex items-center gap-2">
          <Gauge class="w-6 h-6" style="color: #96EEF2" />
          Sensor Status
        </h1>
        <button
          @click="detectSensors"
          :disabled="isDetecting"
          class="px-4 py-2 text-white rounded-lg transition-all hover:opacity-90 flex items-center gap-2"
          :style="{
            background: 'linear-gradient(135deg, #41B9C3 0%, #187D8B 100%)',
            opacity: isDetecting ? 0.7 : 1
          }"
        >
          <RefreshCw :class="['w-4 h-4', isDetecting && 'animate-spin']" />
          Refresh Sensors
        </button>
      </div>

      <!-- Module List -->
      <div class="space-y-4">
        <div
          v-for="mod in modules"
          :key="mod.id"
          :ref="(el) => setModuleRef(mod.id, el as HTMLDivElement | null)"
        >
          <div
            class="p-4 transition-all cursor-pointer"
            :style="{
              backgroundColor: selectedModule?.id === mod.id ? 'rgba(65, 185, 195, 0.2)' : 'rgba(14, 36, 70, 0.5)',
              border: selectedModule?.id === mod.id ? '1px solid #41B9C3' : '1px solid rgba(65, 185, 195, 0.2)',
              borderRadius: selectedModule?.id === mod.id ? '0.5rem 0.5rem 0 0' : '0.5rem',
              borderBottom: selectedModule?.id === mod.id ? 'none' : '1px solid rgba(65, 185, 195, 0.2)'
            }"
            @click="selectedModule = selectedModule?.id === mod.id ? null : mod"
          >
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center gap-3">
                <component :is="getModuleIcon(mod.name)" class="w-6 h-6" style="color: #96EEF2" />
                <div>
                  <h3 class="text-white">{{ mod.name }}</h3>
                </div>
              </div>
              <button
                @click.stop="toggleConnection(mod.id)"
                class="p-2 rounded-lg transition-all"
                :style="{
                  backgroundColor: mod.connected ? 'rgba(252, 216, 105, 0.2)' : 'rgba(14, 36, 70, 0.5)',
                  color: mod.connected ? '#FCD869' : '#96EEF2'
                }"
              >
                <Wifi v-if="mod.connected" class="w-5 h-5" />
                <WifiOff v-else class="w-5 h-5" />
              </button>
            </div>

            <div class="space-y-2">
              <div class="flex items-center justify-between text-sm">
                <span :style="{ color: getStatusColor(mod.moduleStatus) }">
                  {{ mod.moduleStatus }}
                </span>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span style="color: #96EEF2">Connection</span>
                <span :style="{ color: mod.connected ? '#FCD869' : '#DD2C1D' }">
                  {{ mod.connected ? 'Connected' : 'Disconnected' }}
                </span>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span style="color: #96EEF2">Power/Battery Usage</span>
                <span class="text-white">{{ mod.power }}%</span>
              </div>
            </div>
          </div>

          <!-- Expanded Configuration -->
          <div
            v-if="selectedModule?.id === mod.id"
            class="p-6 animate-slide-in"
            style="background-color: rgba(65, 185, 195, 0.15); border: 1px solid #41B9C3; border-top: 1px solid rgba(65, 185, 195, 0.3); border-radius: 0 0 0.5rem 0.5rem"
          >
            <h2 class="text-white mb-4 flex items-center gap-2">
              <Settings class="w-5 h-5" style="color: #96EEF2" />
              {{ selectedModule.name }} Configuration
            </h2>

            <!-- Sensor type config -->
            <div v-if="selectedModule.type === 'sensor'" class="space-y-4">
              <div>
                <label class="block text-sm mb-2" style="color: #96EEF2">Calibration File</label>
                <div class="flex gap-2">
                  <select
                    class="flex-1 px-4 py-2 text-white rounded-lg focus:outline-none"
                    style="background-color: rgba(14, 36, 70, 0.5); border: 1px solid rgba(65, 185, 195, 0.3)"
                  >
                    <option>Default Calibration</option>
                    <option>{{ selectedModule.calibrationFile }}</option>
                    <option>ctd_cal_2023.cal</option>
                  </select>
                  <button
                    class="px-4 py-2 text-white rounded-lg transition-all hover:opacity-90 flex items-center gap-2"
                    style="background: linear-gradient(135deg, #41B9C3 0%, #187D8B 100%)"
                  >
                    <Upload class="w-4 h-4" />
                    Upload
                  </button>
                </div>
              </div>
            </div>

            <!-- Camera type config -->
            <div v-if="selectedModule.type === 'camera'" class="space-y-4">
              <p style="color: #96EEF2">Camera-specific settings are available in the Configuration section.</p>
              <button
                @click="emit('navigate', 'dives')"
                class="px-4 py-2 text-white rounded-lg transition-all hover:opacity-90"
                style="background: linear-gradient(135deg, #41B9C3 0%, #187D8B 100%)"
              >
                Go to Configuration
              </button>
            </div>

            <!-- Light type config -->
            <div v-if="selectedModule.type === 'light'" class="space-y-4">
              <h3 class="mb-3" style="color: #96EEF2">Light Configuration</h3>
              <p style="color: #96EEF2">Lighting-specific settings are available in the Configuration section.</p>
              <button
                @click="emit('navigate', 'dives')"
                class="px-4 py-2 text-white rounded-lg transition-all hover:opacity-90"
                style="background: linear-gradient(135deg, #41B9C3 0%, #187D8B 100%)"
              >
                Go to Configuration
              </button>
            </div>

            <!-- Communication type config -->
            <div v-if="selectedModule.type === 'communication'" class="space-y-4">
              <p style="color: #96EEF2">Communication-specific settings are available in the Configuration section.</p>
              <button
                @click="emit('navigate', 'dives')"
                class="px-4 py-2 text-white rounded-lg transition-all hover:opacity-90"
                style="background: linear-gradient(135deg, #41B9C3 0%, #187D8B 100%)"
              >
                Go to Configuration
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
