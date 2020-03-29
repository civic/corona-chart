#!/bin/bash

apt update
apt install python3 python3-pip liblzma
python3 -m pip install -U pip
python3 -m pip install -r requirements.txt
python3 coronavirus_graph.py

