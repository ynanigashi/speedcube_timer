@echo off
cd /d %~dp0
call .venv\Scripts\activate
title SpeedCube Timer
python main_gui.py