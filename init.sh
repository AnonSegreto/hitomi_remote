#!/bin/bash
ln -s /data ./dest
pip install -r requirements.txt
python -m venv venv
source ./venv/bin/activate
chmod +x ./production.sh
