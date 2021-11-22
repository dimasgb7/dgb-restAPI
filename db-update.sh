#!/usr/bin/env bash
source dgvenv/bin/activate
export FIREBASE_KEY_PATH=$(pwd)/keys/key.json
export CLOUD_STORE_KEY_PATH=$(pwd)/keys/dgb-adm.json
python ./scripts/move_to_db.py
