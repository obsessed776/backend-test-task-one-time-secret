from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import select, update

from src.config import settings
from src.database.db import engine, SessionDep
from src.database.models import Base, Secret
from src.security import security_instance


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)


class SecretCreate(BaseModel):
    secret: str
    password: str | None = None


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


def secret_create_form(
    secret: Annotated[str, Form()],
    password: Annotated[str | None, Form()] = None,
):
    return SecretCreate(secret=secret, password=password)


@app.post("/conceal", response_class=HTMLResponse)
def create_secret(
    request: Request,
    session: SessionDep,
    secret_data: Annotated[SecretCreate, Depends(secret_create_form)],
):
    hashed_password = None
    if secret_data.password:
        hashed_password = security_instance.hash_password(secret_data.password)

    encrypted_secret = security_instance.encrypt(secret_data.secret)
    secret_id = security_instance.create_secret_key()

    session.add(
        Secret(
            id=secret_id,
            secret_data=encrypted_secret,
            hashed_password=hashed_password,
        )
    )
    session.commit()
    return templates.TemplateResponse(request, "conceal.html",
                                      context={"secret_id": secret_id,})



@app.get("/secret/{secret_id}/reveal", response_class=HTMLResponse)
def get_secret_data(
    request: Request,
    session: SessionDep,
    secret_id: str,
    password: Annotated[str | None, Form()] = None,
):
    query = select(Secret).filter_by(
        id=secret_id,
        is_viewed=False,
    ).with_for_update()
    result = session.execute(query)

    record = result.scalar_one_or_none()
    if record is None:
        raise

    update_viewed_status_stmt = update(Secret).filter_by(
        id=secret_id,
    ).values(is_viewed=True)
    session.execute(update_viewed_status_stmt)
    session.commit()

    decrypted_secret =  security_instance.decrypt(record.secret_data)
    return templates.TemplateResponse(request, "reveal.html",
                                      context={"secret": decrypted_secret})
