#!/usr/bin/env bash

set -e

if [ $# -ne 3 ]; then
    echo "Usage: sh 116_apply_manual_codes.sh <user> <data-root> <scheme-dir>"
    echo "Adds manually coded labels to messages"
    exit
fi

USER=$1
DATA_DIR=$2
SCHEME_DIR=$3

rm -rf "$DATA_DIR/116 Messages Merged and Coded"

mkdir -p "$DATA_DIR/116 Messages Merged and Coded"

cd ../apply_manual_codes

pipenv run python apply_manual_codes.py $USER "$DATA_DIR/114 Messages Merged with Surveys and Demogs with ID/messages_merged_with_surveys_and_demogs_with_id.json" \
"$DATA_DIR/115 Coded Messages" "$DATA_DIR/116 Messages Merged and Coded/messages_merged_coded.json" "$SCHEME_DIR/"




