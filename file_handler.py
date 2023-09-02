from pathlib import Path
import os
import queue

def check_file_exist(path: Path | str, filename: str) -> bool:
    # Check path is valid
    if not os.path.exists(path):
        return False
    # Get all files in path
    items = queue.Queue()
    for item in os.listdir(path):
        items.put(Path(Path(path) / item))
    while(not items.empty()):
        item = items.get()
        if filename in str(item):
            return True
        if os.path.isdir(item):
            for i in os.listdir(item):
                items.put(Path(Path(path) / i))
