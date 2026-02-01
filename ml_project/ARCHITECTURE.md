"""
Loan Eligibility Prediction System - Architecture Documentation

This document provides an in-depth overview of the system architecture,
design patterns, and technical implementation details.
"""

# ============================================================================
# 1. SYSTEM ARCHITECTURE
# ============================================================================

"""
LAYERED ARCHITECTURE
====================

The system follows a classic layered architecture with clear separation of concerns:

┌────────────────────────────────────────────────────────────────────────┐
│                       PRESENTATION LAYER                              │
│                    (Streamlit Frontend - Port 8501)                   │
│  - User Interface Components                                          │
│  - Form Input & Validation                                           │
│  - Result Display                                                    │
│  - Session State Management                                         │
└────────────────────┬────────────────────────────────────────────────┘
                     │ HTTP (REST API)
                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         API LAYER                                      │
│                   (FastAPI - Port 8000)                               │
│  - REST Endpoints                                                    │
│  - Request/Response Validation (Pydantic)                           │
│  - Error Handling & Logging                                         │
│  - CORS & Security Middleware                                       │
│  - Route Handlers (routing)                                         │
└────────────────────┬────────────────────────────────────────────────┘
                     │ CRUD Operations
                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                                │
│  - CRUD Operations (database interactions)                           │
│  - ML Model Wrapper                                                 │
│  - Data Preparation                                                │
│  - Prediction Logic                                                │
└────────────────────┬────────────────────────────────────────────────┘
                     │ SQL Queries
                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   DATA ACCESS LAYER                                    │
│              (SQLAlchemy ORM - SQLite)                               │
│  - Database Connection Management                                   │
│  - Query Building & Execution                                      │
│  - Transaction Management                                          │
│  - Schema Definition (ORM Models)                                  │
└────────────────────┬────────────────────────────────────────────────┘
                     │ SQL
                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│                    DATABASE LAYER                                      │
│           (SQLite Database - loans.db)                              │
│  - Persistent Data Storage                                         │
│  - ACID Transactions                                               │
│  - Indexed Queries                                                 │
└────────────────────────────────────────────────────────────────────────┘

                    ┌──────────────────┐
                    │  ML MODEL LAYER  │
                    │  (joblib pkl)    │
                    │  - Inference     │
                    │  - Predictions   │
                    │  - Confidence    │
                    └──────────────────┘
                          ▲
                          │ Called by Business Logic
"""

# ============================================================================
# 2. MODULE BREAKDOWN
# ============================================================================

"""
BACKEND STRUCTURE
=================

backend/
├── app/
│   ├── __init__.py
│   │   Purpose: Package marker
│   │
│   ├── main.py
│   │   - FastAPI application factory
│   │   - Database initialization (create tables)
│   │   - CORS middleware configuration
│   │   - Route registration
│   │   - Health check endpoints
│   │
│   ├── database.py
│   │   - SQLAlchemy engine setup
│   │   - Session factory configuration
│   │   - Connection pooling
│   │   - Dependency injection (get_db)
│   │   - Database URL configuration
│   │
│   ├── models.py
│   │   - LoanApplication ORM model
│   │   - Table schema definition
│   │   - Column types and constraints
│   │   - Relationships (future)
│   │   - Metadata
│   │
│   ├── schemas.py
│   │   - Pydantic validation schemas
│   │   - LoanApplicationCreate (input validation)
│   │   - LoanApplicationResponse (output format)
│   │   - PredictionRequest (prediction input)
│   │   - PredictionResponse (prediction output)
│   │   - Field validators
│   │
│   ├── crud.py
│   │   - create_loan_application()
│   │   - get_loan_application()
│   │   - update_loan_prediction()
│   │   - get_all_loan_applications()
│   │   - delete_loan_application()
│   │   - Database abstraction layer
│   │
│   ├── ml_model.py
│   │   - LoanPredictor class
│   │   - Model loading (joblib)
│   │   - Feature preparation
│   │   - Inference execution
│   │   - Confidence score extraction
│   │   - Error handling
│   │
│   └── routes/
│       ├── __init__.py
│       │   Package marker
│       │
│       └── loan.py
│           - POST /api/loans/applications (save)
│           - GET /api/loans/applications/{loan_id} (retrieve)
│           - POST /api/loans/predict (predict)
│           - GET /api/loans/applications (list)
│           - DELETE /api/loans/applications/{loan_id} (delete)
│           - Error handling per endpoint
│
└── loan_model.pkl
    Pre-trained ML model (Logistic Regression)
"""

# ============================================================================
# 3. DATA FLOW
# ============================================================================

"""
COMPLETE REQUEST-RESPONSE FLOW
==============================

USER SUBMITS APPLICATION:
─────────────────────────
1. Frontend (Streamlit)
   └─> User fills form with applicant data
   └─> Clicks "Save Application"
   └─> Form validation (client-side)
   └─> Sends POST request with JSON data

2. Network Layer (HTTP/REST)
   └─> POST http://localhost:8000/api/loans/applications
   └─> Content-Type: application/json
   └─> Request body contains applicant data

3. Backend - FastAPI Route Handler
   └─> main.py loads router from routes/loan.py
   └─> @app.post("/applications") handler invoked
   └─> Receives LoanApplicationCreate schema

4. Pydantic Validation (schemas.py)
   └─> Validates all fields
   └─> Runs custom validators
   └─> Raises 422 if invalid
   └─> Returns validated object

5. Business Logic (routes/loan.py)
   └─> Calls crud.create_loan_application()
   └─> Passes database session

6. CRUD Layer (crud.py)
   └─> Creates LoanApplication ORM instance
   └─> Populates all fields from validated data
   └─> db.add(instance)
   └─> db.commit()

7. SQLAlchemy ORM (models.py)
   └─> LoanApplication model translates to SQL
   └─> Generates INSERT statement
   └─> Executes via database engine

8. SQLite Database (loans.db)
   └─> Creates new row in loan_applications table
   └─> Assigns auto-increment loan_id
   └─> Returns auto_increment value

9. CRUD Response (crud.py)
   └─> db.refresh() fetches latest data
   └─> Returns LoanApplication object

10. Response Serialization (schemas.py)
    └─> LoanApplicationResponse converts ORM to dict
    └─> JSON serialization
    └─> HTTP 201 Created status

11. Network Response (HTTP/REST)
    └─> Returns JSON with loan_id and all fields
    └─> Status: 201 Created

12. Frontend Receives Response (Streamlit)
    └─> Parses JSON
    └─> Extracts loan_id
    └─> Displays confirmation message
    └─> Stores loan_id in session state


USER REQUESTS PREDICTION:
─────────────────────────
1. Frontend (Streamlit)
   └─> User enters loan_id = 42
   └─> Clicks "Get Prediction"
   └─> Sends POST request

2. Network Layer (HTTP/REST)
   └─> POST http://localhost:8000/api/loans/predict
   └─> Request body: {"loan_id": 42}

3. Backend - FastAPI Route Handler (routes/loan.py)
   └─> @app.post("/predict") handler invoked
   └─> Receives PredictionRequest schema
   └─> loan_id = 42

4. Fetch from Database (crud.py)
   └─> get_loan_application(db, loan_id=42)
   └─> Generates SELECT query
   └─> Returns ORM instance with all fields

5. Load ML Model (ml_model.py)
   └─> get_predictor() returns LoanPredictor instance
   └─> Model already in memory (singleton)
   └─> No reload needed (efficient)

6. Prepare Features (ml_model.py)
   └─> prepare_features() creates pandas DataFrame
   └─> Column names match training data
   └─> Feature order: exact match
   └─> Data types: correct types
   └─> Values: from database record

7. Run Inference (ml_model.py)
   └─> model.predict(features_df) → [0 or 1]
   └─> model.predict_proba(features_df) → [prob_0, prob_1]
   └─> confidence = max(probabilities)

8. Store Prediction (crud.py)
   └─> update_loan_prediction(db, loan_id, prediction, confidence)
   └─> Updates database record
   └─> Sets: prediction, confidence, timestamp
   └─> Commits transaction

9. Response Creation (routes/loan.py)
   └─> PredictionResponse object
   └─> loan_id, prediction, confidence, message
   └─> HTTP 200 OK

10. Network Response (HTTP/REST)
    └─> Returns JSON with prediction details
    └─> Status: 200 OK

11. Frontend Displays Result (Streamlit)
    └─> Parses JSON response
    └─> Shows prediction: APPROVED/REJECTED
    └─> Shows confidence percentage
    └─> Shows formatted message
"""

# ============================================================================
# 4. DESIGN PATTERNS
# ============================================================================

"""
DESIGN PATTERNS USED
====================

1. SINGLETON PATTERN (ML Model)
   Location: backend/app/ml_model.py
   
   Problem: Loading ML model repeatedly is expensive
   Solution: Load once, reuse globally
   
   Implementation:
   - Global _predictor variable
   - get_predictor() checks if instance exists
   - Returns existing instance or creates new one
   
   Benefits:
   - Model loaded only once
   - Faster predictions
   - Consistent behavior

2. FACTORY PATTERN (Database Sessions)
   Location: backend/app/database.py
   
   Problem: Need new DB session for each request
   Solution: SessionLocal factory creates sessions
   
   Implementation:
   - SessionLocal = sessionmaker(bind=engine)
   - get_db() dependency yields sessions
   - Flask-like dependency injection
   
   Benefits:
   - Automatic session cleanup
   - Thread-safe operations
   - Isolation between requests

3. REPOSITORY PATTERN (CRUD Layer)
   Location: backend/app/crud.py
   
   Problem: Business logic shouldn't know SQL
   Solution: Encapsulate DB queries in CRUD functions
   
   Implementation:
   - Separate functions for each operation
   - db.query() only in crud.py
   - Routes use CRUD, not ORM directly
   
   Benefits:
   - Easier testing
   - Reusability
   - Database independence

4. SCHEMA VALIDATION PATTERN (Pydantic)
   Location: backend/app/schemas.py
   
   Problem: Need to validate requests and format responses
   Solution: Pydantic schemas for validation
   
   Implementation:
   - Separate schemas for input/output
   - Field validators with custom logic
   - Type hints for IDE support
   
   Benefits:
   - Automatic validation
   - Type safety
   - Self-documenting

5. DEPENDENCY INJECTION (FastAPI)
   Location: backend/app/routes/loan.py
   
   Problem: Routes need DB access and ML model
   Solution: Inject dependencies as parameters
   
   Implementation:
   - db: Session = Depends(get_db)
   - Predictor fetched in handler
   
   Benefits:
   - Testable code
   - Loose coupling
   - Automatic management

6. MVC-LIKE PATTERN (Streamlit)
   Location: frontend/app.py
   
   Problem: UI code mixed with logic
   Solution: Separate helper functions from UI code
   
   Implementation:
   - Helper functions: get_api_health(), save_application()
   - Page rendering: st.write(), st.form()
   - Session state: st.session_state
   
   Benefits:
   - Cleaner code
   - Reusable functions
   - Easier testing
"""

# ============================================================================
# 5. ERROR HANDLING STRATEGY
# ============================================================================

"""
ERROR HANDLING FLOW
===================

Frontend Errors:
┌─────────────────────────┐
│ API Connection Failed   │
├─────────────────────────┤
│ Check:                  │
│ - API running?          │
│ - Port 8000 open?       │
│ - Firewall allows?      │
│ Handle: Show error msg  │
└─────────────────────────┘

Backend Errors:
┌─────────────────────────┐
│ FastAPI Exception       │
├─────────────────────────┤
│ Validation Error (422)  │
│ → Invalid input data    │
│ → Return error details  │
│                         │
│ Not Found (404)         │
│ → Loan ID doesn't exist │
│ → Return 404 response   │
│                         │
│ Server Error (500)      │
│ → Unexpected exception  │
│ → Log error, return 500 │
└─────────────────────────┘

ML Model Errors:
┌─────────────────────────┐
│ Prediction Failure      │
├─────────────────────────┤
│ Model not found         │
│ → FileNotFoundError     │
│ → Check model path      │
│                         │
│ Inference error         │
│ → Data format issue     │
│ → Invalid features      │
│ → Log exception         │
└─────────────────────────┘

Database Errors:
┌─────────────────────────┐
│ Database Exception      │
├─────────────────────────┤
│ Lock error              │
│ → Restart application   │
│                         │
│ Integrity error         │
│ → Duplicate key         │
│ → Check constraints     │
│                         │
│ Connection error        │
│ → Database file missing │
│ → Permissions issue     │
└─────────────────────────┘

Logging Strategy:
- INFO: API requests, predictions, database operations
- WARNING: Missing data, connection issues
- ERROR: Exceptions, failures
- DEBUG: Variable values, query statements (dev only)
"""

# ============================================================================
# 6. SECURITY CONSIDERATIONS
# ============================================================================

"""
SECURITY MEASURES
=================

1. Input Validation
   - Pydantic validates all fields
   - Type checking
   - Range validation (income > 0)
   - Enum validation (Yes/No, Urban/Rural)
   
2. CORS Configuration
   - Configured in main.py
   - Allow all origins (change for production)
   - Credentials allowed
   - All methods and headers

3. Database Security
   - SQLite (local development)
   - SQLAlchemy prevents SQL injection
   - ORM parameterized queries
   - Connection pooling

4. API Security (Production)
   - Add API key authentication
   - Use JWT tokens
   - HTTPS enforced
   - Rate limiting
   - Request throttling

5. Data Privacy
   - Encrypt sensitive data
   - Audit logs for predictions
   - Access controls
   - Data retention policies
"""

# ============================================================================
# 7. PERFORMANCE CONSIDERATIONS
# ============================================================================

"""
OPTIMIZATION STRATEGIES
=======================

1. Model Caching
   - Singleton pattern for ML model
   - Model loaded once at startup
   - Reused for all predictions
   - ~100ms inference time

2. Database Optimization
   - SQLAlchemy connection pooling
   - Indexed queries (loan_id is PK)
   - Lazy loading disabled (simple schema)
   - Session per request pattern

3. Frontend Optimization
   - Streamlit caching (@st.cache)
   - Async-like operations with spinners
   - Minimal re-renders
   - Efficient data fetching

4. API Optimization
   - Async endpoint support (future)
   - Request timeout handling
   - Response compression (gzip)
   - Pagination for list endpoints

Scalability Options:
- Add Gunicorn for production
- Use PostgreSQL for database
- Add caching layer (Redis)
- Implement API versioning
- Container deployment (Docker)
"""

# ============================================================================
# 8. TESTING STRATEGY
# ============================================================================

"""
TESTING APPROACH
================

Unit Tests:
- Test individual functions
- Mock database and model
- Verify validation logic
- Example: test_schemas.py

Integration Tests:
- Test API endpoints with real DB
- Test full request flow
- Verify database updates
- Example: test_api.py

Manual Testing:
- Use curl commands
- Use Postman/Insomnia
- Test via UI
- Check logs

Test Coverage:
- CRUD operations
- Input validation
- Error handling
- ML model loading
- API routes

Test Data:
- Sample applications
- Edge cases (zero income)
- Invalid data
- Boundary values
"""

# ============================================================================
# 9. DEPLOYMENT GUIDE
# ============================================================================

"""
PRODUCTION DEPLOYMENT
=====================

Database Migration:
1. Move from SQLite to PostgreSQL
2. Update DATABASE_URL in config
3. No code changes needed (SQLAlchemy handles it)
4. Backup SQLite data before migration

API Deployment:
1. Use Gunicorn for production WSGI
2. Deploy to cloud (AWS, GCP, Azure)
3. Configure environment variables
4. Set up CI/CD pipeline
5. Monitor with logging service

Frontend Deployment:
1. Deploy to Streamlit Cloud
2. Or: AWS S3 + CloudFront
3. Configure API endpoint
4. Enable HTTPS

Docker Containerization:
Dockerfile for backend:
  FROM python:3.11
  COPY requirements.txt .
  RUN pip install -r requirements.txt
  COPY backend ./backend
  CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0"]

Environment Configuration:
.env.production:
  DATABASE_URL=postgresql://user:pass@localhost:5432/loans
  API_BASE_URL=https://api.yourdomain.com
  ALLOW_ORIGINS=https://yourdomain.com
  LOG_LEVEL=INFO
"""

# ============================================================================
# 10. FUTURE ENHANCEMENTS
# ============================================================================

"""
POTENTIAL IMPROVEMENTS
======================

Features:
- User authentication
- Multiple ML models (model selection)
- Async predictions (background jobs)
- Webhook notifications
- PDF reports
- Bulk upload (CSV)
- Model retraining pipeline
- A/B testing framework

Performance:
- Async endpoints
- Redis caching
- CDN for static files
- Query optimization
- Load testing

Architecture:
- Microservices split
- Message queue (Celery/RabbitMQ)
- Event sourcing
- CQRS pattern
- GraphQL API

Monitoring:
- Application metrics
- Performance monitoring
- Error tracking (Sentry)
- Log aggregation (ELK)
- Alerting system

Testing:
- Automated testing pipeline
- Load testing
- Security testing
- Penetration testing
- Accessibility testing
"""

print(__doc__)
