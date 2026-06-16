<template>
  <div class="grid grid-cols-3 gap-2">
    <div class="bg-gray-800 rounded-lg p-2 text-center">
      <div class="text-lg font-bold text-orange-400">{{ stats.total }}</div>
      <div class="text-xs text-gray-500">告警总数</div>
    </div>
    <div class="bg-gray-800 rounded-lg p-2 text-center">
      <div class="text-lg font-bold text-green-400">{{ stats.acknowledged }}</div>
      <div class="text-xs text-gray-500">已确认</div>
    </div>
    <div class="bg-gray-800 rounded-lg p-2 text-center">
      <div class="text-lg font-bold text-yellow-400">{{ stats.unacknowledged }}</div>
      <div class="text-xs text-gray-500">未确认</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { AlarmStat } from '../../types'
defineProps<{ stats: AlarmStat }>()
</script>
