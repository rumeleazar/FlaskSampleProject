#!/bin/bash


source venv/Scripts/activate
pip install -r requirements.txt

python flaskdatabase.py
python application.py
