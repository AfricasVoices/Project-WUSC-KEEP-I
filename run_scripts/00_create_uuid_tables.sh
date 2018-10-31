#!/usr/bin/env bash

set -e

if [ $# -ne 1 ]; then
    echo "Usage: sh 01_fetch_messages.sh <data-root>"
    echo "Writes empty UUID tables for phone numbers and messages."
    exit
fi

DATA_DIR=$1

mkdir -p "$DATA_DIR/00 UUIDs"

echo "{}" >"$DATA_DIR/00 UUIDs/phone_uuids.json"
echo "{}" >"$DATA_DIR/00 UUIDs/message_uuids.json"
