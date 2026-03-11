<script setup lang="ts">
import { ref, computed } from 'vue'
import { HelpCircle, PlayCircle, Book, AlertCircle, Send, Download, ExternalLink } from 'lucide-vue-next'
import type { Tutorial } from '../types'

const selectedCategory = ref<'all' | 'setup' | 'operation' | 'troubleshooting'>('all')
const bugReport = ref({ title: '', description: '', severity: 'medium' })

const tutorials = ref<Tutorial[]>([
  { id: 1, title: 'Getting Started with DORIS', description: 'Complete setup guide for first-time users', duration: '12:45', category: 'setup', downloaded: true },
  { id: 2, title: 'Network Configuration', description: 'How to connect DORIS to WiFi networks', duration: '8:30', category: 'setup', downloaded: true },
  { id: 3, title: 'Programming Your First Mission', description: 'Step-by-step mission planning tutorial', duration: '15:20', category: 'operation', downloaded: true },
  { id: 4, title: 'Sensor Calibration Guide', description: 'Calibrating CTD and other sensors', duration: '10:15', category: 'operation', downloaded: false },
  { id: 5, title: 'Troubleshooting Connection Issues', description: 'Common network problems and solutions', duration: '7:45', category: 'troubleshooting', downloaded: true },
  { id: 6, title: 'Data Export and Analysis', description: 'Working with captured data', duration: '14:00', category: 'operation', downloaded: false },
])

const faqs = [
  {
    question: 'How long does the battery last?',
    answer: 'Battery life depends on configuration, but typically provides 10-15 hours of continuous operation with standard settings.'
  },
  {
    question: 'What video formats are supported?',
    answer: 'DORIS natively supports H.265 and H.264 video formats. No transcoding is required for playback.'
  },
  {
    question: 'Can I use DORIS without internet connection?',
    answer: 'Yes! All mission programming, data access, and basic functionality work offline. Internet is only needed for software updates and cloud sync.'
  },
  {
    question: 'How do I update the firmware?',
    answer: 'Firmware updates are available through the software interface. Updates can be automatic or manually installed.'
  },
]

const filteredTutorials = computed(() => {
  if (selectedCategory.value === 'all') return tutorials.value
  return tutorials.value.filter(t => t.category === selectedCategory.value)
})

const handleSubmitBugReport = (e: Event) => {
  e.preventDefault()
  alert(`Bug report submitted:\nTitle: ${bugReport.value.title}\nSeverity: ${bugReport.value.severity}\n\nThank you for your feedback!`)
  bugReport.value = { title: '', description: '', severity: 'medium' }
}
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-6 md:py-8">
    <!-- Header -->
    <div class="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-cyan-500/20 mb-6">
      <h1 class="text-white text-2xl mb-2 flex items-center gap-2">
        <HelpCircle class="w-6 h-6 text-cyan-400" />
        Help & Tutorials
      </h1>
      <p class="text-cyan-300">Learn how to use DORIS effectively and troubleshoot common issues</p>
    </div>

    <!-- Quick Links -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <a
        href="#"
        class="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-cyan-500/20 hover:border-cyan-500/40 transition-all"
      >
        <Book class="w-8 h-8 text-cyan-400 mb-3" />
        <h3 class="text-white mb-2">User Manual</h3>
        <p class="text-cyan-300 text-sm">Complete documentation and reference guide</p>
      </a>
      <a
        href="#"
        class="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-cyan-500/20 hover:border-cyan-500/40 transition-all"
      >
        <ExternalLink class="w-8 h-8 text-cyan-400 mb-3" />
        <h3 class="text-white mb-2">Online Community</h3>
        <p class="text-cyan-300 text-sm">Connect with other DORIS users</p>
      </a>
      <a
        href="#"
        class="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-cyan-500/20 hover:border-cyan-500/40 transition-all"
      >
        <Download class="w-8 h-8 text-cyan-400 mb-3" />
        <h3 class="text-white mb-2">Software Updates</h3>
        <p class="text-cyan-300 text-sm">Check for latest firmware and features</p>
      </a>
    </div>

    <!-- Video Tutorials -->
    <div class="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-cyan-500/20 mb-6">
      <h2 class="text-white text-xl mb-4">Video Tutorials</h2>

      <!-- Category Filter -->
      <div class="flex flex-wrap gap-2 mb-6">
        <button
          @click="selectedCategory = 'all'"
          class="px-4 py-2 rounded-lg transition-all"
          :class="selectedCategory === 'all'
            ? 'bg-cyan-500 text-white'
            : 'bg-slate-700 text-cyan-300 hover:bg-slate-600'"
        >
          All Tutorials
        </button>
        <button
          @click="selectedCategory = 'setup'"
          class="px-4 py-2 rounded-lg transition-all"
          :class="selectedCategory === 'setup'
            ? 'bg-cyan-500 text-white'
            : 'bg-slate-700 text-cyan-300 hover:bg-slate-600'"
        >
          Setup
        </button>
        <button
          @click="selectedCategory = 'operation'"
          class="px-4 py-2 rounded-lg transition-all"
          :class="selectedCategory === 'operation'
            ? 'bg-cyan-500 text-white'
            : 'bg-slate-700 text-cyan-300 hover:bg-slate-600'"
        >
          Operation
        </button>
        <button
          @click="selectedCategory = 'troubleshooting'"
          class="px-4 py-2 rounded-lg transition-all"
          :class="selectedCategory === 'troubleshooting'
            ? 'bg-cyan-500 text-white'
            : 'bg-slate-700 text-cyan-300 hover:bg-slate-600'"
        >
          Troubleshooting
        </button>
      </div>

      <!-- Tutorial List -->
      <div class="space-y-3">
        <div
          v-for="tutorial in filteredTutorials"
          :key="tutorial.id"
          class="bg-slate-700/50 rounded-lg p-4 flex items-center justify-between hover:bg-slate-700 transition-all"
        >
          <div class="flex items-center gap-4 flex-1">
            <div
              class="w-16 h-16 rounded-lg flex items-center justify-center"
              style="background: linear-gradient(135deg, #41B9C3 0%, #187D8B 100%)"
            >
              <PlayCircle class="w-8 h-8 text-white" />
            </div>
            <div class="flex-1">
              <h3 class="text-white mb-1">{{ tutorial.title }}</h3>
              <p class="text-cyan-300 text-sm mb-1">{{ tutorial.description }}</p>
              <div class="flex items-center gap-3 text-sm">
                <span class="text-cyan-400">{{ tutorial.duration }}</span>
                <span
                  class="px-2 py-0.5 rounded text-xs"
                  :class="tutorial.downloaded
                    ? 'bg-green-500/20 text-green-400'
                    : 'bg-blue-500/20 text-blue-400'"
                >
                  {{ tutorial.downloaded ? 'Downloaded' : 'Online Only' }}
                </span>
                <span class="px-2 py-0.5 rounded text-xs bg-purple-500/20 text-purple-400 capitalize">
                  {{ tutorial.category }}
                </span>
              </div>
            </div>
          </div>
          <div class="flex gap-2">
            <button
              v-if="!tutorial.downloaded"
              class="px-4 py-2 bg-slate-600 text-white rounded-lg hover:bg-slate-500 transition-all flex items-center gap-2"
            >
              <Download class="w-4 h-4" />
              Download
            </button>
            <button class="px-4 py-2 bg-cyan-500 text-white rounded-lg hover:bg-cyan-600 transition-all">
              Watch
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- FAQ Section -->
    <div class="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-cyan-500/20 mb-6">
      <h2 class="text-white text-xl mb-4">Frequently Asked Questions</h2>
      <div class="space-y-4">
        <div
          v-for="(faq, index) in faqs"
          :key="index"
          class="bg-slate-700/30 rounded-lg p-4"
        >
          <h3 class="text-white mb-2">{{ faq.question }}</h3>
          <p class="text-cyan-300 text-sm">{{ faq.answer }}</p>
        </div>
      </div>
    </div>

    <!-- Bug Report Form -->
    <div class="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-cyan-500/20">
      <h2 class="text-white text-xl mb-4 flex items-center gap-2">
        <AlertCircle class="w-6 h-6 text-cyan-400" />
        Report a Bug or Issue
      </h2>
      <form @submit="handleSubmitBugReport" class="space-y-4">
        <div>
          <label class="block text-cyan-300 text-sm mb-2">Issue Title</label>
          <input
            type="text"
            v-model="bugReport.title"
            required
            class="w-full px-4 py-2 bg-slate-700 text-white rounded-lg border border-cyan-500/30 focus:border-cyan-500 focus:outline-none"
            placeholder="Brief description of the issue"
          />
        </div>
        <div>
          <label class="block text-cyan-300 text-sm mb-2">Severity</label>
          <select
            v-model="bugReport.severity"
            class="w-full px-4 py-2 bg-slate-700 text-white rounded-lg border border-cyan-500/30 focus:border-cyan-500 focus:outline-none"
          >
            <option value="low">Low - Minor inconvenience</option>
            <option value="medium">Medium - Affects functionality</option>
            <option value="high">High - Critical issue</option>
          </select>
        </div>
        <div>
          <label class="block text-cyan-300 text-sm mb-2">Detailed Description</label>
          <textarea
            v-model="bugReport.description"
            required
            rows="5"
            class="w-full px-4 py-2 bg-slate-700 text-white rounded-lg border border-cyan-500/30 focus:border-cyan-500 focus:outline-none resize-none"
            placeholder="Please provide as much detail as possible, including steps to reproduce the issue..."
          ></textarea>
        </div>
        <button
          type="submit"
          class="w-full px-4 py-3 bg-cyan-500 text-white rounded-lg hover:bg-cyan-600 transition-all flex items-center justify-center gap-2"
        >
          <Send class="w-5 h-5" />
          Submit Bug Report
        </button>
      </form>
    </div>
  </div>
</template>
