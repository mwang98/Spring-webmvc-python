#!/bin/bash

python -m pip install Sphinx

mkdir docs
cd docs/
sphinx-quickstart

sphinx-apidoc -o source/ ../springframework --ext-autodoc --maxdepth 10 --separate -f
# uncomment following lines in source/conf.py
# import os
# import sys
# sys.path.insert(0, os.path.abspath('../springframework'))

# Add a docs/requirements.txt

# build at local
make html
