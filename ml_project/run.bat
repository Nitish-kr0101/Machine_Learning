@echo off
REM Loan Prediction System Startup Script for Windows

echo.
echo ================================
echo   Loan Eligibility Predictor
echo   Starting Application...
echo ================================
echo.

REM Check if venv exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if needed
echo Installing/updating dependencies...
pip install -q -r requirements.txt

REM Create database directory if it doesn't exist
if not exist database mkdir database

REM Start backend in a new window
echo.
echo Starting FastAPI Backend on http://localhost:8000...
echo Opening new terminal window for backend...
start "Loan API Backend" cmd /k "cd backend && python -m uvicorn app.main:app --reload --port 8000"

REM Wait for backend to start
echo Waiting for backend to initialize (5 seconds)...
timeout /t 5 /nobreak

REM Start frontend in a new window
echo.
echo Starting Streamlit Frontend on http://localhost:8501...
echo Opening new terminal window for frontend...
start "Loan Predictor Frontend" cmd /k "cd frontend && streamlit run app.py --server.port 8501"

REM Wait and show status
timeout /t 3 /nobreak

echo.
echo ================================
echo   Application Started!
echo ================================
echo.
echo Frontend:  http://localhost:8501
echo API Docs:  http://localhost:8000/docs
echo API ReDoc: http://localhost:8000/redoc
echo Database:  ./database/loans.db
echo.
echo Press Ctrl+C in any window to stop the service.
echo.
pause
