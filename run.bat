@echo off
title REUSE IMS — Flask Application
color 0A
cls
echo Starting REUSE IMS Flask Application...
echo Installing requirements if necessary: pip install -r requirements.txt
python -m pip install -r requirements.txt
echo.
echo Running REUSE server at http://127.0.0.1:5000 ...
python main.py
pause

