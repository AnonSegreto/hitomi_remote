from fastapi import FastAPI, status, Response, Request
from pydantic import BaseModel
import logging
import re
import os

from logcatter import Log

import books_control

Log.init()
custom_logger = Log.get_logger()
# Replace uvicorn loggers' handlers with logcatter's handlers
for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
    logging.getLogger(logger_name).handlers = custom_logger.handlers
logger = custom_logger

app = FastAPI()


class Data(BaseModel):
    url: str
    col: str = ""


def get_cors_headers(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "https://hitomi.la"
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"


@app.get("/", status_code=status.HTTP_200_OK)
def check(url, response: Response):
    id = re.sub(r'http(s)://hitomi.la/[a-z]+/.+\-|\.html{0,1}', "", url)
    result = books_control.book_exist(id)
    collections = books_control.get_collections()
    get_cors_headers(response)
    Log.d(f"Quearying {id}: Result={result}, from {len(collections)} collections")
    return {
        "url": url,
        "status": result,
        "collections": collections,
    }


@app.put("/", status_code=status.HTTP_200_OK)
def create_collection(name: str, response: Response):
    get_cors_headers(response)
    if books_control.create_collection(name):
        return {"status": True, "name": name}
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": False, "message": "Collection already exists or invalid name"}    


@app.post("/", status_code=status.HTTP_200_OK)
def download(data: Data, request: Request, response: Response):
    response.status_code = status.HTTP_200_OK
    get_cors_headers(response)
    url = data.url
    col = data.col
    result = books_control.download(url, collection=col)
    if not result:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"url": url}


@app.options("/", status_code=status.HTTP_200_OK)
def options(response: Response):
    get_cors_headers(response)
    return 200
