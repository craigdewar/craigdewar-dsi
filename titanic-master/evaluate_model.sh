#!/usr/bin/env bash

export FILE_NAME_TEST=${1:-}
export MODEL_NAME=${2:-}
export MODEL_TYPE=${3:-logistic}

echo "Test file name is ${FILE_NAME_TEST}"
echo "Model name is ${MODEL_NAME}"
echo "Model will be evaluated for ${MODEL_TYPE}"

cd ./src/main/python

chmod +x evaluate_model.py
python evaluate_model.py

echo "Job Complete"
