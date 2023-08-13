import subprocess
from pycbzhelper import Helper
import json
from os import listdir, remove, path
from shutil import move
from pathlib import Path
import datetime

PARENT = Path(__name__).resolve().parent
OUT = PARENT / ".out"
IS_DEBUG = path.exists("debug.json")
TIMEOUT = 500 if IS_DEBUG else 5

def download(url: str):
    command = [
        "gallery-dl",
        "-D",
        str(OUT),
        "-f",
        "{gallery_id}_{num:04}.png",
        "--write-info-json",
        url
    ]
    process = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.wait()
    generate()

def generate():
    begin = datetime.datetime.now()
    enter = False
    while(not enter):
        enter = path.exists(OUT / "info.json")
        current = datetime.datetime.now()
        if ((current - begin).total_seconds() > TIMEOUT):  # Return if json file downloading is failed in 5 sec
            return
    data = {}
    with open(OUT / "info.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    id = data["gallery_id"]
    # Check download complete
    numbers = data["count"]
    enter = False
    begin = datetime.datetime.now()
    while(not enter):
        fs = listdir(OUT)
        enter = f"{id}_{numbers:04}.png" in fs
        current = datetime.datetime.now()
        if ((current - begin).total_seconds() > TIMEOUT):  # Return if json file downloading is failed in 5 sec
            return
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
    metadata["Pages"] = []
    metadata["Publisher"] = "Hitomi.la"
    for name in listdir(OUT):
        if "png" in name:
            metadata["Pages"].append({
                "File": OUT / name,
            })
    output = OUT / f"{id}.cbz"
    helper = Helper(metadata)
    helper.create_cbz(output)
    for name in listdir(".out"):
        if "cbz" in name:
            continue
        remove(str(OUT / name))
    move(str(output), str(PARENT / "dest"))
