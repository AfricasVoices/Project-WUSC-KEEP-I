#!/usr/bin/env bash

set -e

if [ $# -ne 3 ]; then
    echo "Usage: sh 116_filter_coded_messages.sh <user> <data-root>"
    echo "Filters messages from coded data based on _moved_from key"
    exit
fi

USER=$1
DATA_DIR=$2

rm -rf "$DATA_DIR/116 Coded Messages"

mkdir -p "$DATA_DIR/116 Coded Messages"

cd ../apply_manual_codes

pipenv run filter_coded_messages.py $USER "$DATA_DIR/115 Coded Messages to Filter" \
"$DATA_DIR/116 Coded Messages"




