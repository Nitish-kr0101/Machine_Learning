# 🏦 Loan Eligibility Prediction System

## Overview

A complete end-to-end Machine Learning application for predicting loan eligibility. This system demonstrates production-ready architecture with proper separation of concerns between frontend, backend, API, database, and ML model layers.

## Project Architecture

```
ml_project/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── database.py          # SQLAlchemy database configuration
│   │   ├── models.py            # SQLAlchemy ORM models
│   │   ├── schemas.py           # Pydantic validation schemas
│   │   ├── crud.py              # Database operations
│   │   ├── ml_model.py          # ML model loader and inference
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── loan.py          # API endpoints
│   └── loan_model.pkl           # Pre-trained ML model
├── frontend/
│   └── app.py                   # Streamlit UI
├── database/
│   └── loans.db                 # SQLite database (created automatically)
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── run.sh / run.bat            # Startup scripts
```

## Key Features

✅ **FastAPI Backend**
- RESTful API with proper request/response validation
- CORS enabled for frontend communication
- Comprehensive error handling and logging

✅ **Streamlit Frontend**
- Responsive, user-friendly interface
- Real-time API communication
- Application history and tracking

✅ **SQLite Database**
- Persistent storage with SQLAlchemy ORM
- Automatic schema creation
- Audit trails with timestamps

✅ **ML Model Integration**
- Pre-trained Logistic Regression model
- Production-ready inference
- Confidence scores for predictions

✅ **Clean Architecture**
- Separation of concerns
- SOLID principles
- Production-ready code structure

## Installation

### 1. Prerequisites

- Python 3.9+
- pip
- Virtual environment (recommended)

### 2. Setup

```bash
# Navigate to project directory
cd ml_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Place Pre-trained Model

Ensure `loan_model.pkl` is in the backend directory:
```
ml_project/backend/loan_model.pkl
```

## Running the Application

### Option 1: Using Startup Scripts

**Windows:**
```bash
run.bat
```

**macOS/Linux:**
```bash
bash run.sh
```

### Option 2: Manual Startup

**Terminal 1 - Start Backend API:**
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
streamlit run app.py
```

### Access the Application

- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Save Application

**POST** `/api/loans/applications`

Save a new loan application to the database.

**Request Body:**
```json
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

**Response (201):**
```json
{
  "loan_id": 1,
  "applicant_income": 50000,
  "coapplicant_income": 25000,
  "loan_amount": 300000,
  "loan_amount_term": 360,
  "credit_history": 1.0,
  "married": "Yes",
  "self_employed": "No",
  "education": "Graduate",
  "property_area": "Urban",
  "prediction": null,
  "prediction_confidence": null,
  "prediction_timestamp": null,
  "created_at": "2024-01-28T10:30:00",
  "updated_at": "2024-01-28T10:30:00"
}
```

---

### 2. Get Application

**GET** `/api/loans/applications/{loan_id}`

Retrieve a specific loan application.

**Response (200):**
```json
{
  "loan_id": 1,
  "applicant_income": 50000,
  ...
}
```

---

### 3. Make Prediction

**POST** `/api/loans/predict`

Generate ML prediction for a loan application.

**Request Body:**
```json
{
  "loan_id": 1
}
```

**Response (200):**
```json
{
  "loan_id": 1,
  "prediction": 1,
  "prediction_confidence": 0.92,
  "message": "Loan APPROVED (Confidence: 92.00%)"
}
```

---

### 4. List All Applications

**GET** `/api/loans/applications`

Retrieve all applications with pagination.

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Max records to return (default: 100)

**Response (200):**
```json
[
  {
    "loan_id": 1,
    "applicant_income": 50000,
    ...
  },
  {
    "loan_id": 2,
    "applicant_income": 75000,
    ...
  }
]
```

---

### 5. Delete Application

**DELETE** `/api/loans/applications/{loan_id}`

Remove a loan application.

**Response (204):** No content

---

## Workflow

### User Workflow

1. **Submit Application**
   - User fills in applicant details in Streamlit
   - Clicks "Save Application"
   - Frontend sends data to `/api/loans/applications`
   - Backend stores in SQLite and returns `loan_id`

2. **View Application**
   - User enters `loan_id` in "View & Predict" tab
   - Frontend retrieves application details via `/api/loans/applications/{loan_id}`
   - Application details displayed

3. **Get Prediction**
   - User clicks "Get Prediction"
   - Frontend calls `/api/loans/predict` with `loan_id`
   - Backend:
     - Fetches application data from SQLite
     - Loads ML model
     - Runs inference
     - Stores prediction in database
     - Returns result to frontend
   - Prediction displayed with confidence score

4. **View History**
   - User views all applications in "Application History" tab
   - Displays statistics and predictions

### Backend Workflow

```
Frontend Request
    ↓
FastAPI Route Handler
    ↓
CRUD Operations (SQLAlchemy)
    ↓
SQLite Database
    ↓
ML Model (if prediction)
    ↓
Update Database
    ↓
Response to Frontend
```

## Database Schema

### `loan_applications` Table

| Column | Type | Description |
|--------|------|-------------|
| loan_id | INTEGER (PK) | Unique loan identifier |
| applicant_income | FLOAT | Applicant's monthly income |
| coapplicant_income | FLOAT | Co-applicant's monthly income |
| loan_amount | FLOAT | Loan amount requested |
| loan_amount_term | FLOAT | Loan duration in months |
| credit_history | FLOAT | Credit history (0 or 1) |
| married | STRING | Marital status (Yes/No) |
| self_employed | STRING | Self-employment status (Yes/No) |
| education | STRING | Education level (Graduate/Not Graduate) |
| property_area | STRING | Property location (Urban/Semiurban/Rural) |
| prediction | INTEGER | ML prediction (0=Rejected, 1=Approved) |
| prediction_confidence | FLOAT | Confidence score (0-1) |
| prediction_timestamp | DATETIME | When prediction was made |
| created_at | DATETIME | Application creation time |
| updated_at | DATETIME | Last update time |

## Configuration

### Environment Variables

Create a `.env` file in the project root (optional):

```env
API_BASE_URL=http://localhost:8000
STREAMLIT_PORT=8501
BACKEND_PORT=8000
DATABASE_URL=sqlite:///./database/loans.db
LOG_LEVEL=INFO
```

### Logging

Logs are configured at the INFO level. Modify in `backend/app/main.py`:

```python
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for verbose output
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Production Deployment

### Key Considerations

1. **Environment Variables**
   - Use `.env` files for secrets
   - Never commit secrets to version control

2. **Database**
   - For production, migrate from SQLite to PostgreSQL/MySQL
   - Update `DATABASE_URL` in `database.py`

3. **CORS**
   - Configure specific origins instead of `"*"`
   ```python
   allow_origins=["https://yourdomain.com"]
   ```

4. **Model Loading**
   - Implement model versioning
   - Cache model in memory (already done)

5. **Security**
   - Add authentication/authorization
   - Validate all inputs
   - Use HTTPS

6. **Deployment Platforms**
   - Backend: Heroku, AWS EC2, Google Cloud Run
   - Frontend: Streamlit Cloud, AWS Amplify, Vercel

## Troubleshooting

### API Connection Failed

```
Error: Failed to connect to API
```

**Solution:** Ensure backend is running
```bash
cd backend
python -m uvicorn app.main:app --reload
```

---

### Model Not Found

```
FileNotFoundError: Could not find loan_model.pkl
```

**Solution:** Place `loan_model.pkl` in `backend/` directory

---

### Port Already in Use

```
Address already in use
```

**Solution:** Kill process or use different port
```bash
# Change port in startup script
uvicorn app.main:app --port 8001
```

---

### Database Locked

```
sqlite3.OperationalError: database is locked
```

**Solution:** Restart the application

---

## Development

### Code Structure Principles

- **Separation of Concerns**: Each module has a single responsibility
- **DRY (Don't Repeat Yourself)**: Reusable functions and classes
- **SOLID Principles**: Applied throughout the codebase
- **Type Hints**: Full type annotations for better IDE support

### Adding New Features

1. **New Database Field**
   - Add to `models.py`
   - Add to `schemas.py`
   - Update `crud.py` functions
   - Update API routes

2. **New API Endpoint**
   - Create route in `routes/loan.py`
   - Add validation schema in `schemas.py`
   - Add CRUD operation in `crud.py`

3. **New Frontend Page**
   - Add to `frontend/app.py` or new file
   - Use `st.page_link()` for navigation

## Testing

### Example API Call with curl

```bash
# Save application
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

# Get application
curl http://localhost:8000/api/loans/applications/1

# Make prediction
curl -X POST http://localhost:8000/api/loans/predict \
  -H "Content-Type: application/json" \
  -d '{"loan_id": 1}'
```

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions, review the troubleshooting section or check the API documentation at:
- `http://localhost:8000/docs` (Swagger UI)
- `http://localhost:8000/redoc` (ReDoc)

---

**Created:** January 2024  
**ML Framework:** Scikit-learn  
**Backend:** FastAPI  
**Frontend:** Streamlit  
**Database:** SQLite + SQLAlchemy  
