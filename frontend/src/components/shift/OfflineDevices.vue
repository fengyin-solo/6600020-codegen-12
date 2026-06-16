<template>
  <div class="bg-gray-800 rounded-lg p-2">
    <div class="text-xs text-gray-400 mb-1 font-bold">离线设备</div>
    <div v-for="ev in devices" :key="ev.deviceId" class="flex items-center justify-between text-xs py-1">
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full" :class="ev.stillOffline ? 'bg-red-500' : 'bg-green-500'"></span>
        <span class="text-gray-300">{{ ev.deviceName }}</span>
      </div>
      <div class="text-gray-500">
        <template v-if="ev.wentOfflineAt">
          {{ new Date(ev.wentOfflineAt).toLocaleTimeString() }}
        </template>
        <template v-if="ev.cameBackAt">
          → {{ new Date(ev.cameBackAt).toLocaleTimeString() }}
        </template>
        <template v-if="ev.stillOffline">
          <span class="text-red-400"> (仍离线)</span>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { OfflineEvent } from '../../types'
defineProps<{ devices: OfflineEvent[] }>()
</script>
