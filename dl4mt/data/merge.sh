#!/bin/bash
# This script merges all the bitext files in the current directory. 
# Source side files are concatenated into all_[src]-[trg].[src]
# Target side files are concatenated into all_[src]-[trg].[trg] 

if [ "$#" -ne 3 ]; then
    echo ""
    echo "Usage: $0 src trg path_to_data"
    echo ""
    exit 1
fi

SRC=$1
TRG=$2

DATA_DIR=$3

FSRC=${DATA_DIR}/all_${1}-${2}.${1}
FTRG=${DATA_DIR}/all_${1}-${2}.${2}

echo "" > $FSRC
for F in ${DATA_DIR}/$SRC/*
do
    cat $F >> $FSRC

done


echo "" > $FTRG
for F in ${DATA_DIR}/$TRG/*
do
    cat $F >> $FTRG
done
