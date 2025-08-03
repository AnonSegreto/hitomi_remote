#!/bin/bash
ln -s /data ./dest
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
chmod +x ./production.sh
