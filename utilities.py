import re

def get_gallery_id(url: str) -> str | None:
    last = re.search(r"[0-9]+\.html", url)
    if last is None or not ".html" in last.group(0):
        return None
    last = re.sub(r"\.html", "", last.group(0))
    return last
