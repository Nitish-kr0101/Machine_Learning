"""Loan application API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from ..database import get_db
from ..schemas import (
    LoanApplicationCreate,
    LoanApplicationResponse,
    PredictionRequest,
    PredictionResponse
)
from .. import crud
from ..ml_model import get_predictor

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/loans",
    tags=["loans"],
    responses={404: {"description": "Not found"}}
)


@router.post("/applications", response_model=LoanApplicationResponse, status_code=status.HTTP_201_CREATED)
def save_application(
    application: LoanApplicationCreate,
    db: Session = Depends(get_db)
):
    """
    Save a new loan application to the database.
    
    Returns:
        Loan application with unique loan_id
    """
    try:
        db_application = crud.create_loan_application(db, application)
        logger.info(f"Created new loan application with ID: {db_application.loan_id}")
        return db_application
    except Exception as e:
        logger.error(f"Error creating loan application: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save application"
        )


@router.get("/applications/{loan_id}", response_model=LoanApplicationResponse)
def get_application(loan_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a loan application by ID.
    """
    db_application = crud.get_loan_application(db, loan_id)
    if not db_application:
        logger.warning(f"Loan application not found: {loan_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Loan application with ID {loan_id} not found"
        )
    return db_application


@router.post("/predict", response_model=PredictionResponse)
def predict_loan(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):
    """
    Predict loan eligibility for a saved application.
    
    Process:
    1. Fetch application data from database
    2. Run ML model prediction
    3. Store results in database
    4. Return prediction to frontend
    """
    try:
        # Step 1: Fetch application from database
        db_application = crud.get_loan_application(db, request.loan_id)
        if not db_application:
            logger.warning(f"Application not found for prediction: {request.loan_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Loan application with ID {request.loan_id} not found"
            )
        
        # Step 2: Load ML model and make prediction
        logger.info(f"Starting prediction for loan_id: {request.loan_id}")
        predictor = get_predictor()
        
        prediction, confidence = predictor.predict(
            applicant_income=db_application.applicant_income,
            coapplicant_income=db_application.coapplicant_income,
            loan_amount=db_application.loan_amount,
            loan_amount_term=db_application.loan_amount_term,
            credit_history=db_application.credit_history,
            married=db_application.married,
            self_employed=db_application.self_employed,
            education=db_application.education,
            property_area=db_application.property_area
        )
        
        # Step 3: Store prediction in database
        updated_application = crud.update_loan_prediction(
            db,
            request.loan_id,
            prediction,
            confidence
        )
        
        logger.info(
            f"Prediction complete for loan_id {request.loan_id}: "
            f"prediction={prediction}, confidence={confidence:.4f}"
        )
        
        # Step 4: Return result to frontend
        return PredictionResponse(
            loan_id=request.loan_id,
            prediction=prediction,
            prediction_confidence=confidence,
            message=f"Loan {'APPROVED' if prediction == 1 else 'REJECTED'} "
                   f"(Confidence: {confidence*100:.2f}%)"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.get("/applications", response_model=list[LoanApplicationResponse])
def list_applications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all loan applications with pagination.
    """
    applications = crud.get_all_loan_applications(db, skip=skip, limit=limit)
    return applications


@router.delete("/applications/{loan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(loan_id: int, db: Session = Depends(get_db)):
    """
    Delete a loan application by ID.
    """
    success = crud.delete_loan_application(db, loan_id)
    if not success:
        logger.warning(f"Failed to delete application: {loan_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Loan application with ID {loan_id} not found"
        )
    logger.info(f"Deleted loan application: {loan_id}")
    return None
