#!/bin/bash
python -m venv .
source bin/activate
pip install xlrd Cython pandas openpyxl tk pygubu-designer wheel playsound
pip install --upgrade setuptools wheel
pip install playsound
