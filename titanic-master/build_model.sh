#!/usr/bin/env bash

export FILE_NAME_TRAIN=${1:-}
export MODEL_TYPE=${2:-logistic}

echo "FILE_NAME_TRAIN is ${FILE_NAME_TRAIN}"
echo "MODEL_TYPE is ${MODEL_TYPE}"

cd ./src/main/python

chmod +x build_model.py
python build_model.py

echo "Job Complete"
