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
git init
git add .
git commit -m "Initial commit of AI Travel Agent"
git branch -M main

echo.
echo ========================================================
echo   IMPORTANT: You need your GitHub Repository URL.
echo   Create a repo at https://github.com/new if you haven't.
echo ========================================================
echo.
set /p repo_url="Paste your GitHub Repository URL here: "

git remote add origin %repo_url%
git push -u origin main

echo.
echo Done! If asked for credentials, please sign in.
pause
