#!/bin/bash

#apt update
#apt install python3 python3-pip liblzma
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --user
python3 -m pip install -r requirements.txt
python3 coronavirus_graph.py

