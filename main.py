from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import SubwayOutlet, SubwayOutletRead
from typing import List

app = FastAPI()

origins = [
    "http://localhost:5500", 
    "http://127.0.0.1:5500", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
        

@app.on_event("startup")
def on_startup():
    init_db()
    
@app.get("/outlets/", response_model=List[SubwayOutletRead])
def read_outlets(skip: int = 0, limit: int = Query(None), db: Session = Depends(get_db)):
    if limit is None:
        outlets = db.query(SubwayOutlet).offset(skip).all()
    else:
        outlets = db.query(SubwayOutlet).offset(skip).limit(limit).all()
    return outlets

@app.get("/outlets/{outlet_id}", response_model=SubwayOutletRead)
def read_outlet(outlet_id: int, db: Session = Depends(get_db)):
    outlet = db.query(SubwayOutlet).filter(SubwayOutlet.id == outlet_id).first()
    if outlet is None:
        raise HTTPException(status_code=404, detail="Outlet not found")
    return outlet

@app.get("/outlets/search/", response_model=SubwayOutletRead)
def search_outlet(name: str, db: Session = Depends(get_db)):
    outlet = db.query(SubwayOutlet).filter(SubwayOutlet.name == name).first()
    if outlet is None:
        raise HTTPException(status_code=404, detail="Outlet not found")
    return outlet

    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
