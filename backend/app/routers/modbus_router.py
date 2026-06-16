from fastapi import APIRouter
from app.services.modbus_service import read_registers, get_device_status, start_shift, end_shift, get_shift_summary

router = APIRouter()

@router.get("/modbus/devices")
def list_devices():
    return get_device_status()

@router.get("/modbus/read/{device_id}/{address}/{count}")
def read_holding(device_id: str, address: int, count: int = 1):
    """Read holding registers from a Modbus device."""
    return read_registers(device_id, address, count)

@router.post("/modbus/write/{device_id}/{address}")
def write_register(device_id: str, address: int, value: int):
    return {"device_id": device_id, "address": address, "value": value, "status": "written"}

@router.post("/shift/start")
def api_start_shift():
    return start_shift()

@router.post("/shift/end")
def api_end_shift():
    return end_shift()

@router.get("/shift/summary")
def api_shift_summary():
    return get_shift_summary()
