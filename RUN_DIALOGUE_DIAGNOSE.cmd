@echo off
setlocal EnableExtensions
cd /d "%~dp0"
set "GAME_ROOT=E:\Game\Folklore"
if not "%~1"=="" set "GAME_ROOT=%~1"
echo.
echo Folklore: read-only dialogue diagnosis
echo Game location: "%GAME_ROOT%"
echo No original game files will be modified or uploaded.
echo.
if not exist "%GAME_ROOT%\" (
  echo ERROR: Game folder was not found.
  echo Drag the game folder onto this .cmd, or edit GAME_ROOT inside this file.
  goto failed
)
where py >nul 2>nul
if not errorlevel 1 goto use_py
where python >nul 2>nul
if not errorlevel 1 goto use_python
echo ERROR: Python 3.10 or later is required.
goto failed

:use_py
py -3 "tools\dialogue_diagnose.py" --game-root "%GAME_ROOT%" --max-samples 48
goto checked

:use_python
python "tools\dialogue_diagnose.py" --game-root "%GAME_ROOT%" --max-samples 48

:checked
if errorlevel 1 goto failed
echo.
echo DONE: local-data\dialogue-structure-summary.json
echo PRIVATE: local-data\dialogue-probe.json
echo Only share the structure summary after reviewing it.
echo Never upload the private raw probe or game archives.
echo.
pause
exit /b 0

:failed
echo.
echo No game files were changed. See the error message above.
echo.
pause
exit /b 1
