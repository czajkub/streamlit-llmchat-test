from logging import INFO, basicConfig

from fastapi import FastAPI

from app.config import settings
from app.api import chat_router_v1

basicConfig(level=INFO, format="[%(asctime)s - %(name)s] (%(levelname)s) %(message)s")

api = FastAPI(title=settings.api_name)


@api.get("/")
async def root() -> dict[str, str]:
    return {"message": "Server is running!"}


api.include_router(chat_router_v1, prefix=settings.api_latest)
