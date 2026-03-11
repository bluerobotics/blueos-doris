<script setup lang="ts">
import odlLogo from '../assets/odl-logo.png'
import blueRoboticsLogo from '../assets/blue-robotics-logo.png'
</script>

<template>
  <footer
    class="border-t mt-auto"
    style="background-color: rgba(14, 36, 70, 0.9); backdrop-filter: blur(8px); border-color: rgba(65, 185, 195, 0.2)"
  >
    <div class="max-w-7xl mx-auto px-6 py-6">
      <div class="flex flex-col md:flex-row items-center justify-center gap-6 md:gap-16">
        <a
          href="https://www.oceandiscoveryleague.org"
          target="_blank"
          rel="noopener noreferrer"
          class="flex items-center justify-center transition-opacity hover:opacity-80 flex-shrink-0"
        >
          <img
            :src="odlLogo"
            alt="Ocean Discovery League"
            class="h-12 md:h-14 w-auto object-contain"
            style="max-width: 180px"
          />
        </a>

        <a
          href="https://bluerobotics.com/"
          target="_blank"
          rel="noopener noreferrer"
          class="flex items-center justify-center transition-opacity hover:opacity-80 flex-shrink-0"
        >
          <img
            :src="blueRoboticsLogo"
            alt="Blue Robotics"
            class="h-8 md:h-10 w-auto object-contain"
            style="max-width: 160px"
          />
        </a>
      </div>

      <div class="text-center mt-6">
        <a
          href="https://bluerobotics.com/what-is-blueos/"
          target="_blank"
          rel="noopener noreferrer"
          class="text-sm transition-colors hover:underline"
          style="color: #96EEF2"
        >
          Powered by BlueOS
        </a>
      </div>
    </div>
  </footer>
</template>
