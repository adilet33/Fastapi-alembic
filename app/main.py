import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def get_hello():
    return {"message": 'Hello world'}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)




