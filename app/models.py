from pydantic import BaseModel
from typing import Any
from enum import Enum


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


class ChannelType(Enum):
    STRING = 0
    INT = 1
    FLOAT = 2
    ENUM = 3
    CHAR = 4
    LONG = 5
    DOUBLE = 6


class Status(BaseModel):
    name: str
    code: int
    code_with_severity: int
    severity: int
    success: bool
    description: str


class PVModel(BaseModel):
    name: str
    data: Any
    data_type: ChannelType
    data_count: int
    status: Status
