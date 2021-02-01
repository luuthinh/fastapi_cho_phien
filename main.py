from fastapi import Depends, FastAPI

from . import auth
from .internal import admin
from .routers import items, users

app = FastAPI()


app.include_router(users.router)
app.include_router(items.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": 'Hello Bigger Applications'}
