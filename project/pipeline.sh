#!/bin/bash
echo "Running Pipeline Now"

python3 /project/pipeline.py

read -p "Press any key to continue... " -n1 -s
exit 0