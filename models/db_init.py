from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.model import Base

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, future=True)

with engine.begin() as conn:
    Base.metadata.create_all(conn)
