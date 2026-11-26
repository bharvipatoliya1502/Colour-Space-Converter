@echo off
title Install Colour Space Converter
cd /d "%~dp0"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo.
echo Installation finished. You can now run run.bat.
pause
