import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.routes import auth, task


app = FastAPI()

app.include_router(auth.router)
app.include_router(task.router)


@app.get('/')
def get_hello():
    return {"message": 'Hello world'}






