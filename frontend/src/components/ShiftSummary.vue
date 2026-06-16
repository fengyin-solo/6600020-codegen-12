<template>
  <div class="bg-gray-900 rounded-xl p-4">
    <div class="flex items-center justify-between mb-3">
      <h3 class="text-sm text-gray-400 font-bold">交接班摘要</h3>
      <div class="flex gap-2">
        <button v-if="!store.shiftActive && !store.lastShiftSummary" @click="store.startShift()"
          class="bg-blue-700 hover:bg-blue-600 text-white text-xs px-3 py-1 rounded">
          开始班次
        </button>
        <template v-if="store.shiftActive">
          <button @click="copySummary(shiftSummaryText)"
            class="bg-gray-700 hover:bg-gray-600 text-white text-xs px-3 py-1 rounded">
            复制摘要
          </button>
          <button @click="handleEndShift"
            class="bg-red-700 hover:bg-red-600 text-white text-xs px-3 py-1 rounded">
            结束班次
          </button>
        </template>
        <template v-if="!store.shiftActive && store.lastShiftSummary">
          <button @click="copySummary(lastSummaryText)"
            class="bg-gray-700 hover:bg-gray-600 text-white text-xs px-3 py-1 rounded">
            复制摘要
          </button>
          <button @click="store.dismissLastSummary(); store.startShift()"
            class="bg-blue-700 hover:bg-blue-600 text-white text-xs px-3 py-1 rounded">
            开始新班次
          </button>
          <button @click="store.dismissLastSummary()"
            class="bg-gray-800 hover:bg-gray-700 text-gray-400 text-xs px-2 py-1 rounded">
            关闭
          </button>
        </template>
      </div>
    </div>

    <div v-if="!store.shiftActive && !store.lastShiftSummary" class="text-gray-600 text-xs text-center py-6">
      点击「开始班次」记录本班次数据
    </div>

    <div v-else-if="store.shiftActive" class="space-y-3">
      <div class="flex items-center gap-3 text-xs">
        <span class="text-gray-400">
          班次时长: <span class="text-white font-mono">{{ store.shiftSummary.durationMinutes.toFixed(1) }} min</span>
        </span>
        <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
        <span v-if="store.shiftStart" class="text-gray-500">
          {{ new Date(store.shiftStart).toLocaleTimeString() }} - 至今
        </span>
      </div>

      <AlarmStatsGrid :stats="store.shiftSummary.alarmStats" />
      <AlarmLevelBadges :stats="store.shiftSummary.alarmStats" />
      <OfflineDevices v-if="store.shiftSummary.offlineDevices.length" :devices="store.shiftSummary.offlineDevices" />
      <PeakDataGrid v-if="store.shiftSummary.peakData.length" :peaks="store.shiftSummary.peakData" />
    </div>

    <div v-else-if="store.lastShiftSummary" class="space-y-3">
      <div class="bg-green-900/30 border border-green-800 rounded-lg p-2 text-xs text-green-300 mb-2">
        班次已结束 — 摘要如下
      </div>
      <div class="flex items-center gap-3 text-xs">
        <span class="text-gray-400">
          班次时长: <span class="text-white font-mono">{{ store.lastShiftSummary.durationMinutes.toFixed(1) }} min</span>
        </span>
        <span v-if="store.lastShiftSummary.shiftStart" class="text-gray-500">
          {{ new Date(store.lastShiftSummary.shiftStart).toLocaleTimeString() }}
          <template v-if="store.lastShiftSummary.shiftEnd">
            → {{ new Date(store.lastShiftSummary.shiftEnd).toLocaleTimeString() }}
          </template>
        </span>
      </div>

      <AlarmStatsGrid :stats="store.lastShiftSummary.alarmStats" />
      <AlarmLevelBadges :stats="store.lastShiftSummary.alarmStats" />
      <OfflineDevices v-if="store.lastShiftSummary.offlineDevices.length" :devices="store.lastShiftSummary.offlineDevices" />
      <PeakDataGrid v-if="store.lastShiftSummary.peakData.length" :peaks="store.lastShiftSummary.peakData" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useModbusStore } from '../store/modbus'
import AlarmStatsGrid from './shift/AlarmStatsGrid.vue'
import AlarmLevelBadges from './shift/AlarmLevelBadges.vue'
import OfflineDevices from './shift/OfflineDevices.vue'
import PeakDataGrid from './shift/PeakDataGrid.vue'

const store = useModbusStore()

const shiftSummaryText = computed(() => buildText(store.shiftSummary))
const lastSummaryText = computed(() => store.lastShiftSummary ? buildText(store.lastShiftSummary) : '')

function handleEndShift() {
  const text = shiftSummaryText.value
  store.endShift()
  copyToClipboard(text)
}

function copySummary(text: string) {
  copyToClipboard(text)
}

async function copyToClipboard(text: string) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text)
    } else {
      fallbackCopy(text)
    }
  } catch {
    fallbackCopy(text)
  }
}

function fallbackCopy(text: string) {
  const ta = document.createElement('textarea')
  ta.value = text
  ta.style.position = 'fixed'
  ta.style.left = '-9999px'
  document.body.appendChild(ta)
  ta.select()
  try { document.execCommand('copy') } catch {}
  document.body.removeChild(ta)
}

function buildText(s: { shiftStart: number | null; shiftEnd: number | null; durationMinutes: number; alarmStats: { total: number; acknowledged: number; unacknowledged: number; critical: number; warning: number; info: number }; offlineDevices: { deviceName: string; wentOfflineAt: number | null; cameBackAt: number | null; stillOffline: boolean }[]; peakData: { deviceName: string; registerName: string; peakValue: number; unit: string }[] }): string {
  const lines: string[] = []
  lines.push('=== 交接班摘要 ===')
  if (s.shiftStart) lines.push(`班次开始: ${new Date(s.shiftStart).toLocaleString()}`)
  if (s.shiftEnd) lines.push(`班次结束: ${new Date(s.shiftEnd).toLocaleString()}`)
  lines.push(`班次时长: ${s.durationMinutes.toFixed(1)} min`)
  lines.push('')
  lines.push('--- 告警处理 ---')
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
