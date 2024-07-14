import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from app.routes.auth import router


app = FastAPI()

app.include_router(router)


@app.get('/')
def get_hello():
    return {"message": 'Hello world'}






