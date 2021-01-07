#!/bin/bash

python -m pip install Sphinx

mkdir docs
cd docs/
sphinx-quickstart

# uncomment following lines in source/conf.py
# import os
# import sys
# sys.path.insert(0, os.path.abspath('../springframework'))

# Add a docs/requirements.txt
# add sphinx

# create module
sphinx-apidoc -o source/reference ../springframework -f

# re-structure
python run.py -v source/reference/springframework*.rst

# build at local
make html
