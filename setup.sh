#!/bin/bash
pip install -r requirements.txt
sudo apt-get update && sudo apt-get upgrade && sudo apt-get install -y build-essential python-dev

git clone https://github.com/minepy/minepy.git
cd minepy
python setup.py build && python setup.py install

