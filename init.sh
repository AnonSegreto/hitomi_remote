#!/bin/bash
rm -r ./dest
rm -r ./.out
ln -s /data ./dest
pip install -r requirements.txt
source ./venv/bin/activate
chmod +x ./production.sh
