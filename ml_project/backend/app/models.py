"""SQLAlchemy ORM models for the database."""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from .database import Base


class LoanApplication(Base):
    """Model for loan applications."""
    
    __tablename__ = "loan_applications"

    loan_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Applicant Information
    applicant_income = Column(Float, nullable=False)
    coapplicant_income = Column(Float, nullable=False)
    loan_amount = Column(Float, nullable=False)
    loan_amount_term = Column(Float, nullable=False)
    credit_history = Column(Float, nullable=False)
    
    # Categorical Features
    married = Column(String, nullable=False)
    self_employed = Column(String, nullable=False)
    education = Column(String, nullable=False)
    property_area = Column(String, nullable=False)
    
    # Prediction Results
    prediction = Column(Integer, nullable=True)  # 0 = Rejected, 1 = Approved
    prediction_confidence = Column(Float, nullable=True)
    prediction_timestamp = Column(DateTime, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<LoanApplication(loan_id={self.loan_id}, applicant_income={self.applicant_income})>"
