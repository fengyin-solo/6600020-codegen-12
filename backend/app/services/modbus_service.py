"""Modbus service with mock data (replace with pymodbus for production)."""
import random
from typing import List, Dict, Any, Optional
from datetime import datetime

MOCK_DEVICES = [
    {"id": "dev1", "name": "温湿度传感器-A区", "ip": "192.168.1.101", "port": 502, "slave_id": 1, "online": True},
    {"id": "dev2", "name": "压力变送器-B区", "ip": "192.168.1.102", "port": 502, "slave_id": 2, "online": True},
    {"id": "dev3", "name": "电机控制器-C区", "ip": "192.168.1.103", "port": 502, "slave_id": 3, "online": False},
]

_shift_state: Dict[str, Any] = {
    "active": False,
    "start_time": None,
    "alarm_log": [],
    "offline_log": [],
    "peak_data": {},
}

def get_device_status() -> List[Dict[str, Any]]:
    return MOCK_DEVICES

def read_registers(device_id: str, address: int, count: int) -> Dict[str, Any]:
    """Read registers via pymodbus (mock implementation)."""
    # In production: from pymodbus.client import ModbusTcpClient
    # client = ModbusTcpClient(host, port=port)
    # result = client.read_holding_registers(address, count, slave=slave_id)
    values = [round(random.uniform(0, 100), 2) for _ in range(count)]
    return {"device_id": device_id, "address": address, "values": values}

def start_shift() -> Dict[str, Any]:
    _shift_state["active"] = True
    _shift_state["start_time"] = datetime.now()
    _shift_state["alarm_log"] = []
    _shift_state["offline_log"] = []
    _shift_state["peak_data"] = {}
    return {"status": "started", "shift_start": _shift_state["start_time"].isoformat()}

def end_shift() -> Dict[str, Any]:
    if not _shift_state["active"]:
        return {"error": "no active shift"}
    _shift_state["active"] = False
    summary = _build_summary(datetime.now())
    _shift_state["start_time"] = None
    return summary

def record_alarm(alarm: Dict[str, Any]) -> None:
    if _shift_state["active"]:
        _shift_state["alarm_log"].append({**alarm, "timestamp": datetime.now().isoformat()})

def record_offline(device_id: str, device_name: str, online: bool) -> None:
    if not _shift_state["active"]:
        return
    if not online:
        _shift_state["offline_log"].append({
            "device_id": device_id,
            "device_name": device_name,
            "went_offline_at": datetime.now().isoformat(),
            "came_back_at": None,
            "still_offline": True,
        })
    else:
        for ev in reversed(_shift_state["offline_log"]):
            if ev["device_id"] == device_id and ev["still_offline"]:
                ev["came_back_at"] = datetime.now().isoformat()
                ev["still_offline"] = False
                break

def update_peak(device_id: str, device_name: str, register_name: str, value: float, unit: str) -> None:
    if not _shift_state["active"]:
        return
    key = f"{device_id}_{register_name}"
    current = _shift_state["peak_data"].get(key)
    if current is None or value > current["peak_value"]:
        _shift_state["peak_data"][key] = {
            "device_name": device_name,
            "register_name": register_name,
            "peak_value": value,
            "unit": unit,
            "peak_time": datetime.now().isoformat(),
        }

def get_shift_summary() -> Dict[str, Any]:
    if not _shift_state["active"]:
        return {"active": False}
    return _build_summary(datetime.now())

def _build_summary(now: datetime) -> Dict[str, Any]:
    start = _shift_state["start_time"]
    duration = (now - start).total_seconds() / 60 if start else 0
    alarms = _shift_state["alarm_log"]
    total = len(alarms)
    acknowledged = sum(1 for a in alarms if a.get("acknowledged"))
    critical = sum(1 for a in alarms if a.get("level") == "critical")
    warning = sum(1 for a in alarms if a.get("level") == "warning")
    info = sum(1 for a in alarms if a.get("level") == "info")
    return {
        "active": _shift_state["active"],
        "shift_start": start.isoformat() if start else None,
        "shift_end": now.isoformat(),
        "duration_minutes": round(duration, 1),
        "alarm_stats": {
            "total": total,
            "acknowledged": acknowledged,
            "unacknowledged": total - acknowledged,
            "critical": critical,
            "warning": warning,
            "info": info,
        },
        "offline_devices": list(_shift_state["offline_log"]),
        "peak_data": list(_shift_state["peak_data"].values()),
    }
