#!/usr/bin/env bash


export AWS_ACCESS_KEY_ID=${1-}
export AWS_SECRET_ACCESS_KEY=${2-}
export AWS_BUCKET=${3-}
export FILE_PATH=$PWD/src/main/assets/predictions

cd ./src/main/python
chmod +x load_s3.py
python load_s3.py
