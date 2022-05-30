#!/bin/bash

python3 -m venv venv
ln -s venv/bin/activate activate
source activate
pip install -r requirements.txt
