#!/usr/bin/env bash

set -e

if [ $# -ne 3 ]; then
    echo "Usage: sh 23_download_coded_data.sh <data-root> <coda-root> <coda-crypto-token>"
    echo "Downloads labelled messages for reallocating WS data"
    exit
fi

DATA_DIR=$1
CODA_DIR=$2
CRYPTO_TOKEN=$3

mkdir -p "$DATA_DIR/23 Data for WS Fixup"

cd $CODA_DIR/data_tools

DATASET_NAMES=(
    "WUSC_KEEP_II_Aisha"
    "WUSC_KEEP_II_Aisha_Empirical_Expectations"
    "WUSC_KEEP_II_Aisha_Normative_Expectations"
    "WUSC_KEEP_II_Aisha_Parenthood"
    "WUSC_KEEP_II_Aisha_Reference_Groups"
    "WUSC_KEEP_II_Aisha_Reference_Groups_Others"
    "WUSC_KEEP_II_Aisha_Sanctions"
    "WUSC_KEEP_II_Amina"
    "WUSC_KEEP_II_Amina_Empirical_Expectations"
    "WUSC_KEEP_II_Amina_Normative_Expectations"
    "WUSC_KEEP_II_Amina_Parenthood"
    "WUSC_KEEP_II_Amina_Reference_Groups"
    "WUSC_KEEP_II_Amina_Reference_Groups_Others"
    "WUSC_KEEP_II_Amina_Sanctions"
    "WUSC_KEEP_II_Demogs_Age"
    "WUSC_KEEP_II_Demogs_Gender"
    "WUSC_KEEP_II_Demogs_Locations"
    "WUSC_KEEP_II_Mohamed"
    "WUSC_KEEP_II_Mohamed_Empirical_Expectations"
    "WUSC_KEEP_II_Mohamed_Normative_Expectations"
    "WUSC_KEEP_II_Mohamed_Parenthood"
    "WUSC_KEEP_II_Mohamed_Reference_Groups"
    "WUSC_KEEP_II_Mohamed_Reference_Groups_Others"
    "WUSC_KEEP_II_Mohamed_Sanctions"
    "WUSC_KEEP_II_Zamzam"
    "WUSC_KEEP_II_Zamzam_Empirical_Expectations"
    "WUSC_KEEP_II_Zamzam_Normative_Expectations"
    "WUSC_KEEP_II_Zamzam_Parenthood"
    "WUSC_KEEP_II_Zamzam_Reference_Groups"
    "WUSC_KEEP_II_Zamzam_Reference_Groups_Others"
    "WUSC_KEEP_II_Zamzam_Sanctions"    
)


for DATASET in "${DATASET_NAMES[@]}"
do
    # echo "pipenv run python get.py" "$CRYPTO_TOKEN" "$DATASET" messages > "$DATA_DIR/20 Data for WS Migration/$DATASET.json"
    pipenv run python get.py "$CRYPTO_TOKEN" "$DATASET" messages > "$DATA_DIR/23 Data for WS Fixup/${DATASET}.json"
done



