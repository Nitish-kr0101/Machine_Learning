"""Machine learning model loader and inference."""

import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class LoanPredictor:
    """
    Wrapper for the loan prediction model.
    Handles model loading and inference.
    """
    
    def __init__(self, model_path: str):
        """
        Initialize the predictor with a model file.
        
        Args:
            model_path: Path to the joblib model file
        """
        self.model_path = Path(model_path)
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the joblib model from disk."""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found at {self.model_path}")
        
        try:
            self.model = joblib.load(self.model_path)
            logger.info(f"Model loaded successfully from {self.model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise
    
    def prepare_features(
        self,
        applicant_income: float,
        coapplicant_income: float,
        loan_amount: float,
        loan_amount_term: float,
        credit_history: float,
        married: str,
        self_employed: str,
        education: str,
        property_area: str
    ) -> pd.DataFrame:
        """
        Prepare features for prediction in the same format as training data.
        
        Args:
            Individual applicant features
            
        Returns:
            DataFrame with features in correct format
        """
        data = {
            'ApplicantIncome': [applicant_income],
            'CoapplicantIncome': [coapplicant_income],
            'LoanAmount': [loan_amount],
            'Loan_Amount_Term': [loan_amount_term],
            'Credit_History': [credit_history],
            'Married': [married],
            'Self_Employed': [self_employed],
            'Education': [education],
            'Property_Area': [property_area]
        }
        return pd.DataFrame(data)
    
    def predict(
        self,
        applicant_income: float,
        coapplicant_income: float,
        loan_amount: float,
        loan_amount_term: float,
        credit_history: float,
        married: str,
        self_employed: str,
        education: str,
        property_area: str
    ) -> Tuple[int, float]:
        """
        Make a prediction for a loan application.
        
        Args:
            Individual applicant features
            
        Returns:
            Tuple of (prediction, confidence)
            prediction: 0 (Rejected) or 1 (Approved)
            confidence: Confidence score (0-1)
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        # Prepare features
        features_df = self.prepare_features(
            applicant_income=applicant_income,
            coapplicant_income=coapplicant_income,
            loan_amount=loan_amount,
            loan_amount_term=loan_amount_term,
            credit_history=credit_history,
            married=married,
            self_employed=self_employed,
            education=education,
            property_area=property_area
        )
        
        # Make prediction
        try:
            prediction = self.model.predict(features_df)[0]
            
            # Get prediction probabilities
            probabilities = self.model.predict_proba(features_df)[0]
            confidence = float(max(probabilities))
            
            logger.info(f"Prediction made: {prediction} with confidence: {confidence}")
            return int(prediction), confidence
        
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise


# Global model instance
_predictor = None


def get_predictor(model_path: str = None) -> LoanPredictor:
    """
    Get or create a global predictor instance.
    
    Args:
        model_path: Path to model file (required on first call)
        
    Returns:
        LoanPredictor instance
    """
    global _predictor
    if _predictor is None:
        if model_path is None:
            # Try to find model in standard locations
            possible_paths = [
                Path(__file__).parent.parent / "loan_model.pkl",
                Path(__file__).parent.parent.parent / "backend" / "loan_model.pkl",
                Path(__file__).parent.parent.parent.parent / "Machine Learning" / "loan_model.pkl",
                Path("loan_model.pkl"),
            ]
            model_path = None
            for path in possible_paths:
                if path.exists():
                    model_path = str(path)
                    break
            if model_path is None:
                raise FileNotFoundError("Could not find loan_model.pkl")
        
        _predictor = LoanPredictor(model_path)
    return _predictor
