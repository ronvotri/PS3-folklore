@echo off
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0"
chcp 65001 >nul
TITLE Folklore - Vietnamese CMC000 Alpha 0.1
ECHO ======================================================
ECHO FOLKLORE - VIET HOA CMC000 ALPHA 0.1 (1 CAU THU)
ECHO ======================================================
ECHO Chi ho tro ban BCUS98147. DONG RPCS3 TRUOC KHI VA.
ECHO Nen dung BAN SAO thu muc game de thu nghiem.
ECHO Patch luu BACKUP 1 file CMC goc ngay trong thu muc game.
ECHO.
set "GAME_DIR=E:\Game\Folklore"
set /p "GAME_DIR=Thu muc GAME copy (Enter neu o E:\Game\Folklore): "
set "GAME_DIR=%GAME_DIR:"=%"
ECHO.
ECHO [1] Chi KIEM TRA (KHONG sua game)
ECHO [2] CAI patch Alpha01 vao thu muc da chon
ECHO [3] KHOI PHUC file CMC000 goc tu backup
set /p "OPT=Chon 1, 2 hoac 3: "
if "%OPT%"=="1" set "ACTION=check"
if "%OPT%"=="2" set "ACTION=apply"
if "%OPT%"=="3" set "ACTION=restore"
if not defined ACTION goto BAD
where py >nul 2>nul
if not errorlevel 1 goto PYPATH
where python >nul 2>nul
if errorlevel 1 (
  ECHO Loi: May can Python 3.10+.
  goto BAD
)
python "tools\cmc_alpha01.py" --game-root "%GAME_DIR%" --action %ACTION%
goto RESULT
:PYPATH
py -3 "tools\cmc_alpha01.py" --game-root "%GAME_DIR%" --action %ACTION%
:RESULT
if errorlevel 1 goto BAD
ECHO.
ECHO THANH CONG. Neu chon cai patch, mo RPCS3 va den canh CMC000.
ECHO Neu co loi, DONG RPCS3 roi chon 3 de phuc hoi.
goto END
:BAD
ECHO.
ECHO KHONG THANH CONG. Doc loi phia tren. Khong co patch duoc xac nhan.
:END
pause
