import subprocess
from pycbzhelper import Helper
import json
import os
import shutil
from pathlib import Path
import datetime
import re
import logging

logger = logging.getLogger("uvicorn")

PARENT = Path(__name__).resolve().parent
OUT = PARENT / ".out"
DEST = PARENT / "dest"
IS_DEBUG = os.path.exists("debug.json")
TIMEOUT = 500 if IS_DEBUG else 5

def download(url: str):
    temp = OUT / re.sub("[^0-9]", "", url)[0:16]
    # Check temp directory exists
    if os.path.exists(temp):
        logger.info(f"{temp} is exists. Task {url} has been cancled")
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
    return generate(temp)

def generate(temp) -> bool:
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
    metadata = {}
    metadata["Title"] = data["title"]
    if len(data["date"]) > 10:
        metadata["Year"] = int(data["date"][0:4])
        metadata["Month"] = int(data["date"][5:7])
        metadata["Date"] = int(data["date"][8:10])
    metadata["Writer"] = ",".join([*data["artist"], *data["group"]])
    metadata["Genre"] = data["type"]
    metadata["Tags"] = ",".join([*data["tags"], *data["parody"], *data["characters"]])
    metadata["Manga"] = "YesAndRightToLeft"
    metadata["LanguageISO"] = data["lang"]
    metadata["Characters"] = ",".join(data["characters"])
    metadata["Web"] = f"https://hitomi.la/galleries/{id}.html"
    metadata["AgeRating"] = "Adults Only 18+"
    metadata["Publisher"] = "Hitomi.la"
    metadata["Pages"] = []
    for name in sorted(os.listdir(temp)):
        if "png" in name:
            metadata["Pages"].append({
                "File": temp / name,
            })
    logger.info(f"Download: {id} - {metadata['Web']}")
    # Create cbz
    filename = f"{id}.cbz"
    helper = Helper(metadata)
    helper.create_cbz(temp / filename)
    # Clear cache
    files = sorted(os.listdir(temp))
    for name in files:
        if "cbz" in name:
            continue
        os.remove(str(temp / name))
    # Remove old file which its name is same
    output = (DEST) / filename
    if os.path.exists(output):
        logger.info(f"{filename} is already exists. Remove old one...")
        os.remove(output)
    # Move to destination
    try:
        shutil.move(str(temp / filename), str(output))
        logger.info(f"{id} has been downloaded successfully")
    except Exception:
        logger.info(f"Error on handling: {id}")
        removeDirectory(temp)
        return False
    removeDirectory(temp)
    return True

def removeDirectory(dir):
    # Remote temp directory
    if os.path.exists(dir):
        os.rmdir(dir)
