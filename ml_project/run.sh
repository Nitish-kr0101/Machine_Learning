#!/bin/bash

# Loan Prediction System Startup Script for macOS/Linux

echo ""
echo "================================"
echo "   Loan Eligibility Predictor"
echo "   Starting Application..."
echo "================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "Installing/updating dependencies..."
pip install -q -r requirements.txt

# Create database directory if it doesn't exist
mkdir -p database

# Start backend
echo ""
echo "Starting FastAPI Backend on http://localhost:8000..."
cd backend
python -m uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for backend to initialize (5 seconds)..."
sleep 5

# Go back to project root
cd ..

# Start frontend
echo ""
echo "Starting Streamlit Frontend on http://localhost:8501..."
cd frontend
streamlit run app.py --server.port 8501 &
FRONTEND_PID=$!

# Wait a moment for UI to appear
sleep 3

# Show status
echo ""
echo "================================"
echo "   Application Started!"
echo "================================"
echo ""
echo "Frontend:  http://localhost:8501"
echo "API Docs:  http://localhost:8000/docs"
echo "API ReDoc: http://localhost:8000/redoc"
echo "Database:  ./database/loans.db"
echo ""
echo "Press Ctrl+C to stop the services."
echo ""

# Keep script running and handle cleanup
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT

wait $BACKEND_PID $FRONTEND_PID
