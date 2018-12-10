#!/usr/bin/env bash

set -e

if [ $# -ne 3 ]; then
    echo "Usage: sh 13_analysis_file.sh <user> <data-root> <code_scheme_root>"
    echo "Outputs individual-based analysis file"
    exit
fi

USER=$1
DATA_DIR=$2
SCHEME_DIR=$3

rm -rf "$DATA_DIR/17 Analysis Files"

mkdir -p "$DATA_DIR/17 Analysis Files"

cd ../analysis_file

pipenv run python analysis_file.py $USER "$SCHEME_DIR/" "$DATA_DIR/16 Messages Merged and Coded/messages_merged_coded.json" \
"$DATA_DIR/17 Analysis Files/messages.csv" "$DATA_DIR/17 Analysis Files/individuals.csv"
    