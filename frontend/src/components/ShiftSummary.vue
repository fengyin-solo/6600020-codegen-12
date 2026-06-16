<template>
  <div class="bg-gray-900 rounded-xl p-3">
    <div class="flex items-center justify-between mb-3">
      <h3 class="text-sm text-gray-400 font-bold">交接班摘要</h3>
      <div class="flex gap-2">
        <button v-if="!store.shiftActive" @click="store.startShift()"
          class="bg-blue-700 hover:bg-blue-600 text-white text-xs px-3 py-1 rounded">
          开始班次
        </button>
        <template v-else>
          <button @click="copySummary"
            class="bg-gray-700 hover:bg-gray-600 text-white text-xs px-3 py-1 rounded">
            复制摘要
          </button>
          <button @click="handleEndShift"
            class="bg-red-700 hover:bg-red-600 text-white text-xs px-3 py-1 rounded">
            结束班次
          </button>
        </template>
      </div>
    </div>

    <div v-if="!store.shiftActive && !store.shiftStart" class="text-gray-600 text-xs text-center py-6">
      点击「开始班次」记录本班次数据
    </div>

    <div v-else class="space-y-3">
      <div class="flex items-center gap-3 text-xs">
        <span class="text-gray-400">
          班次时长: <span class="text-white font-mono">{{ store.shiftSummary.durationMinutes.toFixed(1) }} min</span>
        </span>
        <span v-if="store.shiftActive" class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
        <span v-if="store.shiftStart" class="text-gray-500">
          {{ new Date(store.shiftStart).toLocaleTimeString() }} -
          <template v-if="store.shiftActive">至今</template>
        </span>
      </div>

      <div class="grid grid-cols-3 gap-2">
        <div class="bg-gray-800 rounded-lg p-2 text-center">
          <div class="text-lg font-bold text-orange-400">{{ store.shiftSummary.alarmStats.total }}</div>
          <div class="text-xs text-gray-500">告警总数</div>
        </div>
        <div class="bg-gray-800 rounded-lg p-2 text-center">
          <div class="text-lg font-bold text-green-400">{{ store.shiftSummary.alarmStats.acknowledged }}</div>
          <div class="text-xs text-gray-500">已确认</div>
        </div>
        <div class="bg-gray-800 rounded-lg p-2 text-center">
          <div class="text-lg font-bold text-yellow-400">{{ store.shiftSummary.alarmStats.unacknowledged }}</div>
          <div class="text-xs text-gray-500">未确认</div>
        </div>
      </div>

      <div class="flex gap-2 text-xs">
        <span class="bg-red-900/50 text-red-300 px-2 py-0.5 rounded">
          严重 {{ store.shiftSummary.alarmStats.critical }}
        </span>
        <span class="bg-yellow-900/50 text-yellow-300 px-2 py-0.5 rounded">
          警告 {{ store.shiftSummary.alarmStats.warning }}
        </span>
        <span class="bg-blue-900/50 text-blue-300 px-2 py-0.5 rounded">
          信息 {{ store.shiftSummary.alarmStats.info }}
        </span>
      </div>

      <div v-if="store.shiftSummary.offlineDevices.length" class="bg-gray-800 rounded-lg p-2">
        <div class="text-xs text-gray-400 mb-1 font-bold">离线设备</div>
        <div v-for="ev in store.shiftSummary.offlineDevices" :key="ev.deviceId" class="flex items-center justify-between text-xs py-1">
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

      <div v-if="store.shiftSummary.peakData.length" class="bg-gray-800 rounded-lg p-2">
        <div class="text-xs text-gray-400 mb-1 font-bold">峰值数据</div>
        <div class="grid grid-cols-2 gap-1">
          <div v-for="p in store.shiftSummary.peakData" :key="`${p.deviceName}_${p.registerName}`"
            class="flex justify-between text-xs bg-gray-900 rounded px-2 py-1">
            <span class="text-gray-400 truncate mr-2">{{ p.deviceName }} · {{ p.registerName }}</span>
            <span class="text-orange-400 font-mono whitespace-nowrap">{{ p.peakValue.toFixed(p.peakValue > 100 ? 0 : 1) }} {{ p.unit }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useModbusStore } from '../store/modbus'

const store = useModbusStore()

function handleEndShift() {
  const text = buildSummaryText()
  store.endShift()
  navigator.clipboard?.writeText(text)
}

function copySummary() {
  const text = buildSummaryText()
  navigator.clipboard?.writeText(text)
}

function buildSummaryText(): string {
  const s = store.shiftSummary
  const lines: string[] = []
  lines.push('=== 交接班摘要 ===')
  if (store.shiftStart) {
    lines.push(`班次开始: ${new Date(store.shiftStart).toLocaleString()}`)
  }
  lines.push(`班次时长: ${s.durationMinutes.toFixed(1)} min`)
  lines.push('')
  lines.push(`--- 告警处理 ---`)
  lines.push(`告警总数: ${s.alarmStats.total}`)
  lines.push(`已确认: ${s.alarmStats.acknowledged}  未确认: ${s.alarmStats.unacknowledged}`)
  lines.push(`严重: ${s.alarmStats.critical}  警告: ${s.alarmStats.warning}  信息: ${s.alarmStats.info}`)
  lines.push('')
  if (s.offlineDevices.length) {
    lines.push('--- 离线设备 ---')
    for (const ev of s.offlineDevices) {
      let line = `${ev.deviceName}: `
      if (ev.wentOfflineAt) line += new Date(ev.wentOfflineAt).toLocaleTimeString()
      if (ev.cameBackAt) line += ` → ${new Date(ev.cameBackAt).toLocaleTimeString()}`
      if (ev.stillOffline) line += ' (仍离线)'
      lines.push(line)
    }
    lines.push('')
  }
  if (s.peakData.length) {
    lines.push('--- 峰值数据 ---')
    for (const p of s.peakData) {
      lines.push(`${p.deviceName} · ${p.registerName}: ${p.peakValue.toFixed(p.peakValue > 100 ? 0 : 1)} ${p.unit}`)
    }
  }
  return lines.join('\n')
}
</script>
