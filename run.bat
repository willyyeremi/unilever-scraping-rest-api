@echo off

python -m pip install virtualenv
python -m virtualenv ./.venv
.\.venv\Scripts\python.exe -m pip install -r ./requirements.txt
.\.venv\Scripts\python.exe ./main_v1.py
start cmd /k .\.venv\Scripts\python.exe ./main_v2.py