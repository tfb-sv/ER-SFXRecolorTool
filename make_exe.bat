REM @echo off

set ENV_NAME=exe_sql
set CONDA_DIR=C:\Users\nural\anaconda3
set MAIN_DIR=C:\Users\nural\ER-SFXRecolorTool
set PYTHON_EXE=%CONDA_DIR%\envs\%ENV_NAME%\python.exe

CALL %CONDA_DIR%\Scripts\activate.bat %ENV_NAME%
cd %MAIN_DIR%

REM %PYTHON_EXE% recolor_sfx.py
pyinstaller -y -i recolor_sfx_icon.ico ER-SFXRecolorTool.py
REM pyinstaller -y ER-SFXRecolorTool.spec

pause
