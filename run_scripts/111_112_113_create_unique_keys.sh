#!/usr/bin/env bash

set -e

if [ $# -ne 2 ]; then
    echo "Usage: sh 111_112_113_create_unique_keys.sh <user> <data-root>"
    echo "Adds group name to varibles in messages, surveys and demogs"
    exit
fi

USER=$1
DATA_DIR=$2

rm -rf "$DATA_DIR/111 Messages with Unique Keys"
rm -rf "$DATA_DIR/112 Surveys with Unique Keys"
rm -rf "$DATA_DIR/113 Demogs with Unique Keys"

mkdir -p "$DATA_DIR/111 Messages with Unique Keys"
mkdir -p "$DATA_DIR/112 Surveys with Unique Keys"
mkdir -p "$DATA_DIR/113 Demogs with Unique Keys"

cd ../create_unique_keys/

pipenv run python create_unique_keys.py $USER "$DATA_DIR/05 Messages with ID/" "$DATA_DIR/07 Surveys with ID/" \
    "$DATA_DIR/09 Demogs with ID/" "$DATA_DIR/111 Messages with Unique Keys" "$DATA_DIR/112 Surveys with Unique Keys" \
    "$DATA_DIR/113 Demogs with Unique Keys"




