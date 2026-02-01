"""CRUD operations for database."""

from sqlalchemy.orm import Session
from datetime import datetime
from .models import LoanApplication
from .schemas import LoanApplicationCreate, LoanApplicationUpdate


def create_loan_application(db: Session, application: LoanApplicationCreate) -> LoanApplication:
    """
    Create a new loan application in the database.
    
    Args:
        db: Database session
        application: Application data
        
    Returns:
        Created LoanApplication instance
    """
    db_application = LoanApplication(
        applicant_income=application.applicant_income,
        coapplicant_income=application.coapplicant_income,
        loan_amount=application.loan_amount,
        loan_amount_term=application.loan_amount_term,
        credit_history=application.credit_history,
        married=application.married,
        self_employed=application.self_employed,
        education=application.education,
        property_area=application.property_area
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


def get_loan_application(db: Session, loan_id: int) -> LoanApplication:
    """
    Retrieve a loan application by ID.
    
    Args:
        db: Database session
        loan_id: Loan application ID
        
    Returns:
        LoanApplication instance or None
    """
    return db.query(LoanApplication).filter(LoanApplication.loan_id == loan_id).first()


def update_loan_prediction(db: Session, loan_id: int, prediction: int, confidence: float) -> LoanApplication:
    """
    Update loan application with prediction results.
    
    Args:
        db: Database session
        loan_id: Loan application ID
        prediction: Prediction result (0 or 1)
        confidence: Confidence score
        
    Returns:
        Updated LoanApplication instance
    """
    db_application = get_loan_application(db, loan_id)
    if db_application:
        db_application.prediction = prediction
        db_application.prediction_confidence = confidence
        db_application.prediction_timestamp = datetime.utcnow()
        db.commit()
        db.refresh(db_application)
    return db_application


def get_all_loan_applications(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all loan applications with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of LoanApplication instances
    """
    return db.query(LoanApplication).offset(skip).limit(limit).all()


def delete_loan_application(db: Session, loan_id: int) -> bool:
    """
    Delete a loan application by ID.
    
    Args:
        db: Database session
        loan_id: Loan application ID
        
    Returns:
        True if deleted, False if not found
    """
    db_application = get_loan_application(db, loan_id)
    if db_application:
        db.delete(db_application)
        db.commit()
        return True
    return False
