from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, SubwayOutlet

DATABASE_URL = "sqlite:///subway_outlets.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    from models import SubwayOutlet
    Base.metadata.create_all(bind=engine)