#!/usr/bin/env bash

set -e

if [ $# -ne 2 ]; then
    echo "Usage: sh 114_update_messages_with_surveys <user> <data-root>"
    echo "Merges messages, surveys and demogs"
    exit
fi

USER=$1
DATA_DIR=$2

rm -rf "$DATA_DIR/114 Messages Merged with Surveys and Demogs with ID"

mkdir -p "$DATA_DIR/114 Messages Merged with Surveys and Demogs with ID"

cd ../update_messages_with_surveys

pipenv run python update_messages_with_surveys.py $USER "$DATA_DIR/111 Messages with Unique Keys" \
"$DATA_DIR/112 Surveys with Unique Keys" "$DATA_DIR/113 Demogs with Unique Keys/Demog_survey_updated_keys.json" \
"$DATA_DIR/114 Messages Merged with Surveys and Demogs with ID/messages_merged_with_surveys_and_demogs_with_id.json"





