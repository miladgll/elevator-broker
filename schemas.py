
from pydantic import BaseModel
from typing import Dict, Any

class IoTDataCreate(BaseModel):
    source_ip: str
    payload: Dict[str, Any]

class IoTDataRead(BaseModel):
    id: int
    source_ip: str
    payload: Dict[str, Any]
    timestamp: str

    class Config:
        orm_mode = True
