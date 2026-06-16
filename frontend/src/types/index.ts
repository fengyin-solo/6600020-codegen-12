export interface ModbusRegister {
  address: number
  name: string
  type: 'coil' | 'discrete' | 'holding' | 'input'
  value: number | boolean
  unit: string
  updatedAt: number
}

export interface Device {
  id: string
  name: string
  ip: string
  port: number
  slaveId: number
  online: boolean
  registers: ModbusRegister[]
}

export interface Alarm {
  id: string
  deviceId: string
  register: string
  message: string
  level: 'info' | 'warning' | 'critical'
  timestamp: number
  acknowledged: boolean
}

export interface AlarmStat {
  total: number
  acknowledged: number
  unacknowledged: number
  critical: number
  warning: number
  info: number
}

export interface OfflineEvent {
  deviceId: string
  deviceName: string
  wentOfflineAt: number | null
  cameBackAt: number | null
  stillOffline: boolean
}

export interface PeakRecord {
  deviceName: string
  registerName: string
  peakValue: number
  unit: string
  peakTime: number
}

export interface ShiftSummary {
  shiftStart: number | null
  shiftEnd: number | null
  durationMinutes: number
  alarmStats: AlarmStat
  offlineDevices: OfflineEvent[]
  peakData: PeakRecord[]
}
