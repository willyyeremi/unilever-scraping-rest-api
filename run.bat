@echo off

call .\container\run-docker.bat
python -m pip install virtualenv
python -m virtualenv ./api/.venv
.\api\.venv\Scripts\python.exe -m pip install -r ./api/requirements.txt
.\api\.venv\Scripts\python.exe ./api/main.py