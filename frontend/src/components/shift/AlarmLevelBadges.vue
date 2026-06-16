<template>
  <div class="flex gap-2 text-xs">
    <span class="bg-red-900/50 text-red-300 px-2 py-0.5 rounded">
      严重 {{ stats.critical }}
    </span>
    <span class="bg-yellow-900/50 text-yellow-300 px-2 py-0.5 rounded">
      警告 {{ stats.warning }}
    </span>
    <span class="bg-blue-900/50 text-blue-300 px-2 py-0.5 rounded">
      信息 {{ stats.info }}
    </span>
  </div>
</template>

<script setup lang="ts">
import type { AlarmStat } from '../../types'
defineProps<{ stats: AlarmStat }>()
</script>
