#!/bin/bash

echo " Running Pipeline Now "

# Execute pipeline
python project/pipeline.py
  
# Check dataset is avilable
if [ -f "../data/train.sqlite" ] && [ -f "../data/test.sqlite" ]; then
  echo "Dataset exist."
else
  echo "Dataset not exist executing pipeline to fetchand create database."
fi

echo "=== Running Tests ==="

#Execute testcase
python project/test.py

read -p "Press any key to continue... " -n1 -s
exit 0