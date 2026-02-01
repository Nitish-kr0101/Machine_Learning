"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class LoanApplicationCreate(BaseModel):
    """Schema for creating a new loan application."""
    
    applicant_income: float = Field(..., gt=0, description="Income of the applicant")
    coapplicant_income: float = Field(..., ge=0, description="Income of co-applicant")
    loan_amount: float = Field(..., gt=0, description="Loan amount requested")
    loan_amount_term: float = Field(..., gt=0, description="Loan term in months")
    credit_history: float = Field(..., description="Credit history (0 or 1)")
    married: str = Field(..., description="Marital status (Yes/No)")
    self_employed: str = Field(..., description="Self employed status (Yes/No)")
    education: str = Field(..., description="Education level (Graduate/Not Graduate)")
    property_area: str = Field(..., description="Property area (Urban/Semiurban/Rural)")
    
    @validator('credit_history')
    def validate_credit_history(cls, v):
        if v not in [0, 1, 0.0, 1.0]:
            raise ValueError("Credit_History must be 0 or 1")
        return v
    
    @validator('married', 'self_employed', 'education', 'property_area')
    def validate_categorical_fields(cls, v):
        if not isinstance(v, str) or not v.strip():
            raise ValueError("Categorical fields must be non-empty strings")
        return v.strip()


class LoanApplicationUpdate(BaseModel):
    """Schema for updating loan application with prediction."""
    
    prediction: int = Field(..., description="Prediction result (0 or 1)")
    prediction_confidence: float = Field(..., ge=0, le=1, description="Confidence score")


class LoanApplicationResponse(BaseModel):
    """Schema for loan application response."""
    
    loan_id: int
    applicant_income: float
    coapplicant_income: float
    loan_amount: float
    loan_amount_term: float
    credit_history: float
    married: str
    self_employed: str
    education: str
    property_area: str
    prediction: Optional[int] = None
    prediction_confidence: Optional[float] = None
    prediction_timestamp: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PredictionRequest(BaseModel):
    """Schema for prediction request."""
    
    loan_id: int = Field(..., gt=0, description="Loan application ID")


class PredictionResponse(BaseModel):
    """Schema for prediction response."""
    
    loan_id: int
    prediction: int
    prediction_confidence: float
    message: str
    
    class Config:
        from_attributes = True
