
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from database import Base

class IoTData(Base):
    __tablename__ = "iot_data"

    id = Column(Integer, primary_key=True, index=True)
    source_ip = Column(String, index=True)
    payload = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
