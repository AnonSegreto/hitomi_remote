import subprocess
from cbz.page import PageInfo
from cbz.comic import ComicInfo
from cbz.constants import PageType, YesNo, Manga, AgeRating, Format
import json
import os
import shutil
from pathlib import Path
import datetime
import re
from logcatter import Log

PARENT = Path(__name__).resolve().parent
OUT = PARENT / ".out"
DEST = (PARENT / "dest")
IS_DEBUG = os.path.exists("debug.json")
TIMEOUT = 500 if IS_DEBUG else 5

def download(url: str, collection: str = "") -> bool:
    temp = OUT / re.sub("[^0-9]", "", url)[0:16]
    # Check temp directory exists
    if os.path.exists(temp):
        Log.i(f"{temp} is exists. Task {url} has been cancled")
        return False
    command = [
        "gallery-dl",
        "-D",
        str(temp),
        "-f",
        "{gallery_id}_{num:04}.png",
        "--write-info-json",
        url
    ]
    process = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.wait()
    return generate(temp, collection)

def generate(temp, collection) -> bool:
    # Check metadata is ready
    begin = datetime.datetime.now()
    enter = False
    while(not enter):
        enter = os.path.exists(temp / "info.json")
        current = datetime.datetime.now()
        if ((current - begin).total_seconds() > TIMEOUT):  # Return if json file downloading is failed in 5 sec
            return False
    data = {}
    with open(temp / "info.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    id = data["gallery_id"]
    # Check download complete
    numbers = data["count"]
    enter = False
    begin = datetime.datetime.now()
    while(not enter):
        fs = os.listdir(temp)
        enter = f"{id}_{numbers:04}.png" in fs
        current = datetime.datetime.now()
        if ((current - begin).total_seconds() > TIMEOUT * numbers):  # Return if json file downloading is failed in 5 sec
            return False
    # Set metadata
    url = f"https://hitomi.la/galleries/{id}.html"
    images_path = temp / name
    pages = [PageInfo.load(path) for path in images_path.iterdir()]
    comic = ComicInfo.from_pages(
        pages=pages,
        title=data['title'],
        year=int(data["date"][0:4]),
        month=int(data["date"][5:7]),
        date=int(data["date"][8:10]),
        writer=",".join([*data["artist"], *data["group"]]),
        genre=data['type'],
        tags=",".join([*data["tags"], *data["parody"], *data["characters"]]),
        manga=Manga.YES,
        language_iso=data['lang'],
        characters=",".join(data["characters"]),
        web=url,
        age_rating=AgeRating.ADULTS18,
        publisher="Hitomi.la",
        number='1',
        format=Format.NSFW,
        black_white=YesNo.NO,
    )
    # Create CBZ
    filename = f"{id}.cbz"
    cbz_content = comic.pack()
    cbz_path = temp / Path(filename)
    cbz_path.write_bytes(cbz_content)
    Log.i(f"Download: {id} - {url}")
    # Clear cache
    files = sorted(os.listdir(temp))
    for name in files:
        if "cbz" in name:
            continue
        os.remove(str(temp / name))
    # Remove old file which its name is same
    output = DEST
    if collection != "":
        output = output / collection
        if not os.path.exists(output):
            os.makedirs(output, exist_ok=True)
    output = output / filename
    if os.path.exists(output):
        Log.w(f"{filename} is already exists. Remove old one...")
        os.remove(output)
    # Move to destination
    try:
        shutil.move(str(temp / filename), str(output))
        Log.i(f"{id} has been downloaded successfully")
    except Exception:
        Log.e(f"Error on handling: {id}")
        removeDirectory(temp)
        return False
    removeDirectory(temp)
    return True

def removeDirectory(dir):
    # Remote temp directory
    if os.path.exists(dir):
        os.rmdir(dir)

def book_exist(id):
    if id == "":
        return False
    results = []
    def loop(dir):
        for file in os.listdir(dir):
            if os.path.isdir(dir / file):
                return loop(dir / file)
            elif file == f"{id}.cbz":
                results.append(True)
        results.append(False)
    loop(DEST)
    return any(results)


def get_collections():
    cols = []
    for dir in os.listdir(DEST):
        if os.path.isdir(DEST / dir):
            cols.append(dir)
    return cols

def create_collection(name):
    if not os.path.exists(DEST / name):
        os.makedirs(DEST / name, exist_ok=True)
        return True
    return False