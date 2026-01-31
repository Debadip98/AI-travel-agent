@echo off
echo ========================================================
echo   AI Travel Agent - Deployment Helper
echo ========================================================
echo.
echo Checking for Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is NOT installed.
    echo Please download and install Git from: https://git-scm.com/downloads
    echo.
    echo After installing, close this window and run this script again.
    pause
    exit /b
)

echo Git is installed!
echo.
echo initializing repository...
"C:\Program Files\Git\cmd\git.exe" remote add origin %repo_url%
"C:\Program Files\Git\cmd\git.exe" push -u origin main

echo.
echo Done! If asked for credentials, please sign in.
pause
