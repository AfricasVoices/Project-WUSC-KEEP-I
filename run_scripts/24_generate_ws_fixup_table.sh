#!/usr/bin/env bash

set -e

if [ $# -ne 1 ]; then
    echo "Usage: sh 24_generate_ws_fixup_table.sh <data-root>"
    echo "Generate fixup tables"
    exit
fi

DATA_DIR=$1

mkdir -p "$DATA_DIR/24 Data WS Fixup"

cd ../generate_fixup_tables

# echo "pipenv run python get.py" "$CRYPTO_TOKEN" "$DATASET" messages > "$DATA_DIR/20 Data for WS Migration/$DATASET.json"
pipenv run python generate_fixup_table.py "$DATA_DIR/23 Data for WS Fixup" "$DATA_DIR/24 Data WS Fixup/fixup_table.json"  



