from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from src.config import settings

app = FastAPI()
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)
