@echo off
echo ================================
echo        Starting IoT Project
echo ================================

REM ---------------------------------
REM Check if Mosquitto is installed
REM ---------------------------------
if not exist "C:\Program Files\mosquitto\mosquitto.exe" (
    echo ERROR: Mosquitto MQTT broker is not installed!
    echo Download it from https://mosquitto.org/download/
    pause
    exit /b
)

REM ---------------------------------
REM Check if Mosquitto is already running
REM ---------------------------------
tasklist | findstr /I "mosquitto.exe" > nul
if %ERRORLEVEL%==0 (
    echo Mosquitto is already running. Skipping start.
    goto MOSQUITTO_DONE
)

REM ---------------------------------
REM Check if port 1883 is already in use
REM ---------------------------------
netstat -ano | findstr ":1883" > nul
if %ERRORLEVEL%==0 (
    echo Port 1883 is already in use. Assuming MQTT broker is running.
    goto MOSQUITTO_DONE
)

REM ---------------------------------
REM Start Mosquitto MQTT Broker
REM ---------------------------------
echo Starting Mosquitto broker...
start "" "C:\Program Files\mosquitto\mosquitto.exe" -v
timeout /t 2 > nul

:MOSQUITTO_DONE
echo Mosquitto check complete.

REM ---------------------------------
REM Create virtual environment if missing
REM ---------------------------------
if not exist ".venv" (
    echo Virtual environment not found. Creating .venv...
    python -m venv .venv
) else (
    echo Virtual environment found.
)

REM ---------------------------------
REM Activate virtual environment
REM ---------------------------------
echo Activating virtual environment...
call .venv\Scripts\activate

REM ---------------------------------
REM Install backend dependencies
REM ---------------------------------
echo Installing requirements...
pip install -r requirements.txt

REM ---------------------------------
REM Install frontend dependencies
REM ---------------------------------
if not exist "frontend\node_modules" (
    echo Frontend dependencies not found. Installing...
    cd frontend
    npm install
    cd ..
) else (
    echo Frontend dependencies already installed.
)

REM ---------------------------------
REM Start backend server
REM ---------------------------------
echo Starting backend (Flask)...
start cmd /k python backend\main.py

REM ---------------------------------
REM Start bus simulator
REM ---------------------------------
echo Starting bus simulator...
start cmd /k python bus_simulator\main.py

REM ---------------------------------
REM Start frontend (React)
REM ---------------------------------
echo Starting frontend (React)...
start cmd /k "cd frontend && npm run dev"

REM ---------------------------------
REM Open browser
REM ---------------------------------
timeout /t 3 > nul
start "" "http://localhost:5173"

echo ================================
echo Project started successfully!
echo ================================
pause
