from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ModbusRegister(BaseModel):
    address: int
    name: str
    type: str
    value: float
    unit: str

class Device(BaseModel):
    id: str
    name: str
    ip: str
    port: int
    slave_id: int
    online: bool
    registers: List[ModbusRegister] = []

class AlarmStat(BaseModel):
    total: int
    acknowledged: int
    unacknowledged: int
    critical: int
    warning: int
    info: int

class OfflineEvent(BaseModel):
    device_id: str
    device_name: str
    went_offline_at: Optional[datetime] = None
    came_back_at: Optional[datetime] = None
    still_offline: bool = False

class PeakRecord(BaseModel):
    device_name: str
    register_name: str
    peak_value: float
    unit: str
    peak_time: datetime

class ShiftSummary(BaseModel):
    shift_start: datetime
    shift_end: Optional[datetime] = None
    duration_minutes: float = 0
    alarm_stats: AlarmStat = AlarmStat()
    offline_devices: List[OfflineEvent] = []
    peak_data: List[PeakRecord] = []
