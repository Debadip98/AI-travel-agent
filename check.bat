@echo off
REM Windows batch script for pre-deployment checks
REM Usage: check.bat

echo ========================================
echo AI Travel Agent - Pre-Deployment Checks
echo ========================================
echo.

echo [1/2] Running environment and API tests...
python test_agent.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Pre-deployment tests failed!
    pause
    exit /b 1
)

echo.
echo [2/2] Running unit tests...
pytest tests/ -v
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Unit tests failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo All checks passed! Ready to deploy.
echo ========================================
pause
