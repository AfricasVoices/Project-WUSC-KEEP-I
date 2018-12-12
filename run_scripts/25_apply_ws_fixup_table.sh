#!/usr/bin/env bash

set -e

if [ $# -ne 1 ]; then
    echo "Usage: sh 24_generate_ws_fixup_table.sh <data-root>"
    echo "Apply fixup tables"
    exit
fi

DATA_DIR=$1

mkdir -p "$DATA_DIR/25 WS Fixup Log"

cd ../apply_fixup_tables

# echo "pipenv run python get.py" "$CRYPTO_TOKEN" "$DATASET" messages > "$DATA_DIR/20 Data for WS Migration/$DATASET.json"
pipenv run python apply_fixup_table.py "$DATA_DIR/24 Data WS Fixup/fixup_table.json" \
    "$DATA_DIR/05 Messages with ID" "$DATA_DIR/07 Surveys with ID" "$DATA_DIR/09 Demogs with ID" \
    ../code_schemes > "$DATA_DIR/25 WS Fixup Log/ws_fixup_messages.csv"

    # "$DATA_DIR/25 Fixedup Messages" "$DATA_DIR/26 Fixedup Surveys" "$DATA_DIR/27 Fixedup Demogs"



