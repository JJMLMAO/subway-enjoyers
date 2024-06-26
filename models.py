from sqlalchemy import  Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class SubwayOutlet(Base):
    __tablename__ = "subway_outlets"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    operating_hours = Column(String)
    waze_link = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    
    
class SubwayOutletBase(BaseModel):
    name: str
    address: str
    operating_hours: str
    waze_link: str
    latitude: str
    longitude: str

class SubwayOutletCreate(SubwayOutletBase):
    pass

class SubwayOutletRead(SubwayOutletBase):
    id: int
    
    class Config:
        orm_mode = True