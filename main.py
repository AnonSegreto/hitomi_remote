from fastapi import FastAPI, status, Response, Request
from pydantic import BaseModel
import logging
import re
import os

import books_control

logger = logging.getLogger("uvicorn")
logger.info("Initialize system")

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
    get_cors_headers(response)
    return {
        "url": url,
        "status": books_control.book_exist(id),
        "collections": books_control.get_collections(),
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
