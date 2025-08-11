@echo off
echo 🏦 Life Annuity Advisor - Local Setup
echo =====================================

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 3 is required but not installed.
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

:: Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is required but not installed.
    echo Please install Node.js 16+ from https://nodejs.org
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do echo ✅ %%i found
for /f "tokens=*" %%i in ('node --version') do echo ✅ Node.js %%i found
echo.

:: Setup backend
echo 🔧 Setting up backend...
cd backend

:: Create virtual environment
python -m venv venv
echo ✅ Virtual environment created

:: Activate virtual environment
call venv\Scripts\activate
echo ✅ Virtual environment activated

:: Install Python dependencies
pip install -r requirements.txt
echo ✅ Python dependencies installed

cd ..

:: Setup frontend
echo 🔧 Setting up frontend...
cd frontend

:: Install Node.js dependencies
npm install
echo ✅ Node.js dependencies installed

cd ..

echo.
echo 🎉 Setup complete!
echo.
echo To run the application:
echo.
echo 1. Start Backend (Terminal 1):
echo    cd backend
echo    venv\Scripts\activate
echo    uvicorn api:app --reload
echo.
echo 2. Start Frontend (Terminal 2):
echo    cd frontend
echo    npm start
echo.
echo Then open http://localhost:3000 in your browser!
pause