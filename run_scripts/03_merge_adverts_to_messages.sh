#!/usr/bin/env bash

set -e

if [ $# -ne 2 ]; then
    echo "Usage: sh 03_merge_adverts_to_messages.sh <user> <data-root>"
    echo "Merges the answers from the advets and the shows."
    exit
fi

USER=$1
DATA_DIR=$2

cd ../merge_advert_response_and_messages

mkdir -p "$DATA_DIR/03 Messages Merged"

SHOWS_AND_ADVERTS=(
    "AISHA"   "Adverts"           "Aisha_merged"
    "MOHAMED" "Advert (Mohamed)"  "Mohamed_merged"
    "ZAMZAM"  "Advert(Zamzam)"    "Zamzam_merged"
    )


# There were no adverts for Amina, so copy through
cp "$DATA_DIR/01 Raw Messages/AMINA.json" "$DATA_DIR/03 Messages Merged/Amina_merged.json"

for i in $(seq 0 $((${#SHOWS_AND_ADVERTS[@]} / 3 - 1)))
do
    INPUT_1="${SHOWS_AND_ADVERTS[3 * i]}"
    INPUT_2="${SHOWS_AND_ADVERTS[3 * i + 1]}"
    OUTPUT="${SHOWS_AND_ADVERTS[3 * i + 2]}"

    echo $INPUT_1 $INPUT_2 $OUTPUT
    bash docker-run.sh "$USER" "$DATA_DIR/01 Raw Messages/$INPUT_1.json" "$INPUT_1" \
        "$DATA_DIR/02 Raw Surveys/$INPUT_2.json" "$DATA_DIR/03 Messages Merged/$OUTPUT.json"
done


# for SHOW in "${SHOWS[@]}"
# do
#     echo "sh docker-run.sh" "$USER" "$DATA_DIR/03 Messages Merged/$SHOW.json" \
#         "$DATA_DIR/04 Clean Messages/$SHOW.json"

#     sh docker-run.sh "$USER" "$DATA_DIR/03 Messages Merged/$SHOW.json" \
#         "$DATA_DIR/04 Clean Messages/$SHOW.json"
# done
