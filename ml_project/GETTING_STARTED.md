# Getting Started Guide

## Quick Start

### Step 1: Install Python Dependencies

```bash
# Navigate to project directory
cd ml_project

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Prepare Pre-trained Model

The system expects a pre-trained ML model file: `loan_model.pkl`

**Option A: Use Existing Model**
```bash
# Copy your pre-trained model to:
cp /path/to/loan_model.pkl backend/loan_model.pkl
```

**Option B: Generate New Model**
If you have training data, use the included notebook to train:
```bash
jupyter notebook loan.ipynb
# Then save the model and place in backend/loan_model.pkl
```

### Step 3: Run the Application

**Windows:**
```bash
run.bat
```

**macOS/Linux:**
```bash
bash run.sh
```

Or manually in separate terminals:

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
streamlit run app.py
```

### Step 4: Access the Application

- **Frontend**: Open http://localhost:8501 in your browser
- **API Documentation**: Visit http://localhost:8000/docs
- **Interactive API**: Visit http://localhost:8000/redoc

---

## File Structure Explained

```
ml_project/
│
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── database.py              # SQLAlchemy configuration
│   │   ├── models.py                # ORM models (LoanApplication)
│   │   ├── schemas.py               # Pydantic validation schemas
│   │   ├── crud.py                  # Database operations
│   │   ├── ml_model.py              # ML model wrapper
│   │   └── routes/
│   │       └── loan.py              # API endpoints
│   └── loan_model.pkl               # Pre-trained ML model
│
├── frontend/                         # Streamlit Frontend
│   └── app.py                       # Main UI application
│
├── database/                         # SQLite Database
│   └── loans.db                     # Database file (auto-created)
│
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── README.md                        # Full documentation
├── GETTING_STARTED.md              # This file
├── run.bat                         # Windows startup script
└── run.sh                          # Linux/macOS startup script
```

---

## Architecture Overview

### Layers

```
┌─────────────────────────────┐
│  STREAMLIT FRONTEND (UI)    │  Port 8501
│  - User Interface           │
│  - Input Forms              │
│  - Results Display          │
└────────────┬────────────────┘
             │ HTTP Requests/Responses
             │ (REST API)
┌────────────▼────────────────┐
│  FASTAPI BACKEND (API)      │  Port 8000
│  - REST Endpoints           │
│  - Request Validation       │
│  - Error Handling           │
└────────────┬────────────────┘
             │ CRUD Operations
             │
┌────────────▼────────────────┐
│  SQLALCHEMY + SQLITE (DB)   │
│  - Data Storage             │
│  - Application Records      │
│  - Predictions              │
└─────────────────────────────┘

             ▲
             │
             │ Inference
             │
┌────────────▼────────────────┐
│  ML MODEL (joblib)          │
│  - Loan Prediction Logic    │
│  - Confidence Scores        │
└─────────────────────────────┘
```

---

## Workflow: End-to-End Example

### Scenario: John Applies for a Loan

1. **Frontend (User Input)**
   ```
   John opens http://localhost:8501
   → Fills in loan application form
   → Clicks "Save Application"
   ```

2. **Request Sent to Backend**
   ```
   POST /api/loans/applications
   {
     "applicant_income": 50000,
     "coapplicant_income": 25000,
     "loan_amount": 300000,
     "loan_amount_term": 360,
     "credit_history": 1.0,
     "married": "Yes",
     "self_employed": "No",
     "education": "Graduate",
     "property_area": "Urban"
   }
   ```

3. **Backend Processes Request**
   ```
   ✓ Validates data using Pydantic schema
   ✓ Creates LoanApplication in SQLite
   ✓ Returns loan_id = 42
   ```

4. **Frontend Receives Response**
   ```
   ✓ Displays: "Application Saved! Loan ID: 42"
   ```

5. **User Requests Prediction**
   ```
   John enters Loan ID: 42
   → Clicks "Get Prediction"
   ```

6. **Backend Makes Prediction**
   ```
   POST /api/loans/predict
   {
     "loan_id": 42
   }
   
   ✓ Fetches application #42 from SQLite
   ✓ Loads loan_model.pkl
   ✓ Runs inference with applicant data
   ✓ Gets prediction: APPROVED (92% confidence)
   ✓ Stores result in database
   ✓ Returns to frontend
   ```

7. **Frontend Displays Result**
   ```
   ✓ Shows: "✅ APPROVED - Confidence: 92%"
   ```

---

## API Quick Reference

### 1. Save Application
```bash
curl -X POST http://localhost:8000/api/loans/applications \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_income": 50000,
    "coapplicant_income": 25000,
    "loan_amount": 300000,
    "loan_amount_term": 360,
    "credit_history": 1.0,
    "married": "Yes",
    "self_employed": "No",
    "education": "Graduate",
    "property_area": "Urban"
  }'
```

**Response:**
```json
{
  "loan_id": 42,
  "applicant_income": 50000,
  ...
  "created_at": "2024-01-28T10:30:00"
}
```

### 2. Get Application
```bash
curl http://localhost:8000/api/loans/applications/42
```

### 3. Make Prediction
```bash
curl -X POST http://localhost:8000/api/loans/predict \
  -H "Content-Type: application/json" \
  -d '{"loan_id": 42}'
```

**Response:**
```json
{
  "loan_id": 42,
  "prediction": 1,
  "prediction_confidence": 0.92,
  "message": "Loan APPROVED (Confidence: 92.00%)"
}
```

### 4. List All Applications
```bash
curl http://localhost:8000/api/loans/applications?skip=0&limit=10
```

---

## Common Issues & Solutions

### Issue: "API Connection Failed"

**Problem:** Frontend can't connect to backend

**Solution:**
1. Ensure backend is running: `python -m uvicorn backend.app.main:app --reload`
2. Check port 8000 is not in use: `netstat -ano | findstr :8000`
3. Verify firewall settings

### Issue: "Model Not Found"

**Problem:** Backend can't find loan_model.pkl

**Solution:**
1. Place `loan_model.pkl` in `backend/` directory
2. Verify filename is exact (case-sensitive on Linux)
3. Check file permissions

### Issue: "Database Locked"

**Problem:** SQLite locked error

**Solution:**
1. Restart the application
2. Check no other process is accessing `database/loans.db`
3. Delete `database/loans.db` to start fresh (will lose data)

### Issue: Port Already in Use

**Problem:** Can't start on port 8000/8501

**Solution:**
1. Find process: `lsof -i :8000` (macOS/Linux) or `netstat -ano | findstr :8000` (Windows)
2. Kill process: `kill -9 <PID>` (macOS/Linux)
3. Use different port: `--port 8002`

---

## Development Tips

### View API Documentation
- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)

### Check Database
```bash
# Open SQLite directly
sqlite3 database/loans.db

# View schema
.schema loan_applications

# View data
SELECT * FROM loan_applications;
```

### View Logs
Check the backend terminal for detailed logs of all operations.

### Modify Input Validation
Edit `backend/app/schemas.py` to add/change validation rules.

### Add Database Fields
1. Edit `backend/app/models.py`
2. Update `backend/app/schemas.py`
3. Update `backend/app/crud.py`
4. Delete `database/loans.db` to regenerate schema
5. Restart backend

---

## Next Steps

1. ✅ Run the application
2. ✅ Test with sample data
3. ✅ Review API documentation
4. ✅ Explore database records
5. ✅ Modify frontend/backend as needed
6. ✅ Deploy to production (see README.md)

---

## Support Resources

- **API Docs**: http://localhost:8000/docs
- **README**: See README.md for detailed documentation
- **Code Comments**: All modules have detailed docstrings
- **Pydantic Docs**: https://docs.pydantic.dev/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Streamlit Docs**: https://docs.streamlit.io/

---

**Happy Predicting! 🎉**
