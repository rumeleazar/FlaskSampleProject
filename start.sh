#!/bin/bash


source venv/Scripts/activat.bat
pip install -r requirements.txt

python flaskdatabase.py
python application.py
