#!/bin/bash
source "/home/ubuntu/MotionWeb/venv/bin/activate"
nohup uvicorn --host '0.0.0.0' main:app > /dev/null 2>&1 &

deactivate