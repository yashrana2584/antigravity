@echo off
title Face Biometric Unlock Screen
echo ========================================================
echo        Face Biometric Unlock Screen with Voice Greeting
echo ========================================================
echo.
echo Launching Face Unlock application...
cd /d "%~dp0"
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo App closed with an error code %ERRORLEVEL%.
    pause
)
