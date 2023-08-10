import subprocess

def download(url: str):
    process = subprocess.run(f"gallery-dl -d .out")
    process.wait()