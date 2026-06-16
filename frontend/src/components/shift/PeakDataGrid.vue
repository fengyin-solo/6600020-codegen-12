<template>
  <div class="bg-gray-800 rounded-lg p-2">
    <div class="text-xs text-gray-400 mb-1 font-bold">峰值数据</div>
    <div class="grid grid-cols-2 gap-1">
      <div v-for="p in peaks" :key="`${p.deviceName}_${p.registerName}`"
        class="flex justify-between text-xs bg-gray-900 rounded px-2 py-1">
        <span class="text-gray-400 truncate mr-2">{{ p.deviceName }} · {{ p.registerName }}</span>
        <span class="text-orange-400 font-mono whitespace-nowrap">{{ p.peakValue.toFixed(p.peakValue > 100 ? 0 : 1) }} {{ p.unit }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PeakRecord } from '../../types'
defineProps<{ peaks: PeakRecord[] }>()
</script>
