from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings

engine = create_engine(url=settings.DATABASE_URL, echo=True)
session_factory = sessionmaker(bind=engine, expire_on_commit=False)
