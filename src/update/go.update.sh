#!/bin/sh

BASE_NAME=result/history.csv

sufix=`tail -1 ${BASE_NAME} | cut -d , -f 1`
BACK_NAME=result/history-${sufix}.csv

mkdir -p logs
mv ${BASE_NAME} ${BACK_NAME}
python update_history.py ${BACK_NAME} ${BASE_NAME}
python parse.py ${BASE_NAME} > logs/${sufix}.log 2>&1
