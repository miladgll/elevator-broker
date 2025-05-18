
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

from database import SessionLocal, engine, Base
from models import IoTData
from schemas import IoTDataCreate, IoTDataRead

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Elevator IoT Broker & Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/broker/data", response_model=IoTDataRead)
async def receive_data(data: IoTDataCreate, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host
    record = IoTData(source_ip=data.source_ip or client_ip, payload=data.payload)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@app.get("/api/data", response_model=list[IoTDataRead])
def read_all_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(IoTData).offset(skip).limit(limit).all()

@app.get("/api/data/latest", response_model=IoTDataRead)
def read_latest_data(db: Session = Depends(get_db)):
    record = db.query(IoTData).order_by(IoTData.timestamp.desc()).first()
    if not record:
        raise HTTPException(status_code=404, detail="No data found")
    return record

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
