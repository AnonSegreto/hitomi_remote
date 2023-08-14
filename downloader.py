import subprocess
from pycbzhelper import Helper
import json
import os
import shutil
from pathlib import Path
import datetime

PARENT = Path(__name__).resolve().parent
OUT = PARENT / ".out"
IS_DEBUG = os.path.exists("debug.json")
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
    return generate()

def generate() -> bool:
    begin = datetime.datetime.now()
    enter = False
    while(not enter):
        enter = os.path.exists(OUT / "info.json")
        current = datetime.datetime.now()
        if ((current - begin).total_seconds() > TIMEOUT):  # Return if json file downloading is failed in 5 sec
            return False
    data = {}
    with open(OUT / "info.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    id = data["gallery_id"]
    # Check download complete
    numbers = data["count"]
    enter = False
    begin = datetime.datetime.now()
    while(not enter):
        fs = os.listdir(OUT)
        enter = f"{id}_{numbers:04}.png" in fs
        current = datetime.datetime.now()
        if ((current - begin).total_seconds() > TIMEOUT * numbers):  # Return if json file downloading is failed in 5 sec
            return False
    metadata = {}
    metadata["Title"] = data["title"]
    if len(data["date"]) > 10:
        metadata["Year"] = int(data["date"][0:4])
        metadata["Month"] = int(data["date"][5:7])
        metadata["Date"] = int(data["date"][8:10])
    metadata["Writer"] = ",".join([*data["artist"], *data["group"]])
    series = data["parody"][0] if len(data["parody"]) > 0 else data["type"]
    metadata["Series"] = series
    metadata["SeriesGroup"] = ",".join(data["parody"])
    metadata["Genre"] = data["type"]
    metadata["Tags"] = ",".join([*data["tags"], *data["parody"], *data["characters"]])
    metadata["Manga"] = "YesAndRightToLeft"
    metadata["LanguageISO"] = data["lang"]
    metadata["Characters"] = ",".join(data["characters"])
    metadata["Web"] = f"https://hitomi.la/galleries/{id}.html"
    metadata["AgeRating"] = "Adults Only 18+"
    metadata["Publisher"] = "Hitomi.la"
    metadata["Pages"] = []
    for name in os.listdir(OUT):
        if "png" in name:
            metadata["Pages"].append({
                "File": OUT / name,
            })
    output = OUT / f"{id}.cbz"
    print(f"Download: {id} ({metadata['Series']}) - {', '.join(metadata['Tags'][0:3])}")
    helper = Helper(metadata)
    helper.create_cbz(output)
    for name in os.listdir(".out"):
        if "cbz" in name:
            continue
        os.remove(str(OUT / name))
    if not os.path.exists(PARENT / "dest" / series):
        os.mkdir(PARENT / "dest" /  series)
        print(f"{series} directory does not exists. Create one...")
    try:
        shutil.move(str(output), str(PARENT / "dest" / series))
        print(f"{id} has been downloaded successfully")
    except FileExistsError or FileNotFoundError or shutil.Error:
        print(f"Error on handling: {id}")
        os.remove(str(output))
        return False
    return True
