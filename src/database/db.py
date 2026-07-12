from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import settings

engine = create_engine(url=settings.DATABASE_URL, echo=True)
session_factory = sessionmaker(bind=engine, expire_on_commit=False)


def get_session() -> Iterator[Session]:
    with session_factory() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
