#!/usr/bin/env bash
source dgvenv/bin/activate
export FLASK_APP=main.py
export FIREBASE_KEY_PATH=$(pwd)/keys/key.json
export CLOUD_STORE_KEY_PATH=$(pwd)/keys/dgb-adm.json
flask run
