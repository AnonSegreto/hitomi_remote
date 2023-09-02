from fastapi import FastAPI, status, Response, Request
from pydantic import BaseModel
import logging

import downloader
import file_handler
import utilities as util

logger = logging.getLogger("uvicorn")
logger.info("Initialize system")

app = FastAPI()


class Data(BaseModel):
    url: str


@app.get("/{url}")
def read_root(url: str, response: Response):
    result = file_handler.check_file_exist(downloader.DEST, util.get_gallery_id(url))
    response.headers.append("Access-Control-Allow-Origin", "https://hitomi.la")
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
    return result if not result is None else response.status_code

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