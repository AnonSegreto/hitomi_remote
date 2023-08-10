from fastapi import FastAPI, status, Response, Request
from pydantic import BaseModel

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
    return {"url": url}

@app.options("/", status_code=status.HTTP_200_OK)
def options(response: Response):
    response.headers.append("Access-Control-Allow-Origin", "https://hitomi.la")
    response.headers.append("Access-Control-Allow-Private-Network", "true")
    response.headers.append("Access-Control-Allow-Headers", "Content-Type")
    return 200