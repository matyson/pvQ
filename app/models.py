from pydantic import BaseModel

class PVInfo(BaseModel):
    name: str
    value: float
    char_value: str
    count: int
    nelm: int
    type: str
    units: str
    precision: int
    host: str
    access: str
    status: int
    severity: int
    timestamp: str
    posixseconds: float
    nanoseconds: int
    upper_ctrl_limit: float
    lower_ctrl_limit: float
    upper_disp_limit: float
    lower_disp_limit: float
    upper_alarm_limit: float
    upper_warning_limit: float
    lower_warning_limit: float
    lower_alarm_limit: float

class PVGet(BaseModel):
    name: str
    value: float