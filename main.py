from fastapi import FastAPI, status, Response, Request
from pydantic import BaseModel
import logging

import downloader

logger = logging.getLogger("uvicorn")
logger.info("Initialize system")

app = FastAPI()


class Data(BaseModel):
    url: str


@app.get("/")
def read_root():
    return 404

@app.post("/", status_code=status.HTTP_200_OK)
def download(data: Data, request: Request, response: Response):
    response.status_code = status.HTTP_200_OK
    response.headers.append("Access-Control-Allow-Origin", "https://hitomi.la")
    url = data.url
    result = downloader.download(url)
    if not result:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"url": url}

@app.options("/", status_code=status.HTTP_200_OK)
def options(response: Response):
    response.headers.append("Access-Control-Allow-Origin", "https://hitomi.la")
    response.headers.append("Access-Control-Allow-Private-Network", "true")
    response.headers.append("Access-Control-Allow-Headers", "Content-Type")
    return 200