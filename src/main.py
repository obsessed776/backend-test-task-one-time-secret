from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

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
    encrypted_secret = security_instance.encrypt(secret_data.secret)
    secret_id = security_instance.create_secret_key()
    session.add(
        Secret(
            id=secret_id,
            secret_data=encrypted_secret,
            hashed_password=secret_data.password,
        )
    )
    session.commit()
    return templates.TemplateResponse(request, "conceal.html",
                                      context={"secret_id": secret_id,})
