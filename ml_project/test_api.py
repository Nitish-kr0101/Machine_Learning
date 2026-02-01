"""
API Testing Examples

This file contains example test cases for the Loan Prediction API.
Run with: pytest test_api.py
"""

import pytest
import requests
import json
from typing import Dict

BASE_URL = "http://localhost:8000/api/loans"
TIMEOUT = 10


class TestLoanAPI:
    """Test suite for Loan Prediction API."""
    
    @pytest.fixture
    def sample_application(self) -> Dict:
        """Sample loan application data."""
        return {
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
    
    def test_api_health(self):
        """Test API health endpoint."""
        response = requests.get("http://localhost:8000/health", timeout=TIMEOUT)
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_save_application(self, sample_application):
        """Test saving a loan application."""
        response = requests.post(
            f"{BASE_URL}/applications",
            json=sample_application,
            timeout=TIMEOUT
        )
        assert response.status_code == 201
        data = response.json()
        assert "loan_id" in data
        assert data["applicant_income"] == sample_application["applicant_income"]
        assert data["prediction"] is None
        
        return data["loan_id"]
    
    def test_get_application(self, sample_application):
        """Test retrieving a loan application."""
        # First save
        save_response = requests.post(
            f"{BASE_URL}/applications",
            json=sample_application,
            timeout=TIMEOUT
        )
        loan_id = save_response.json()["loan_id"]
        
        # Then retrieve
        response = requests.get(
            f"{BASE_URL}/applications/{loan_id}",
            timeout=TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        assert data["loan_id"] == loan_id
    
    def test_get_nonexistent_application(self):
        """Test getting non-existent application."""
        response = requests.get(
            f"{BASE_URL}/applications/99999",
            timeout=TIMEOUT
        )
        assert response.status_code == 404
    
    def test_make_prediction(self, sample_application):
        """Test making a prediction."""
        # Save application first
        save_response = requests.post(
            f"{BASE_URL}/applications",
            json=sample_application,
            timeout=TIMEOUT
        )
        loan_id = save_response.json()["loan_id"]
        
        # Make prediction
        response = requests.post(
            f"{BASE_URL}/predict",
            json={"loan_id": loan_id},
            timeout=TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert "prediction_confidence" in data
        assert data["loan_id"] == loan_id
        assert data["prediction"] in [0, 1]
        assert 0 <= data["prediction_confidence"] <= 1
    
    def test_invalid_input(self):
        """Test with invalid input."""
        invalid_data = {
            "applicant_income": -5000,  # Negative income
            "coapplicant_income": 25000,
            "loan_amount": 300000,
            "loan_amount_term": 360,
            "credit_history": 1.0,
            "married": "Yes",
            "self_employed": "No",
            "education": "Graduate",
            "property_area": "Urban"
        }
        
        response = requests.post(
            f"{BASE_URL}/applications",
            json=invalid_data,
            timeout=TIMEOUT
        )
        assert response.status_code >= 400
    
    def test_invalid_credit_history(self):
        """Test with invalid credit history."""
        invalid_data = {
            "applicant_income": 50000,
            "coapplicant_income": 25000,
            "loan_amount": 300000,
            "loan_amount_term": 360,
            "credit_history": 2.5,  # Invalid value
            "married": "Yes",
            "self_employed": "No",
            "education": "Graduate",
            "property_area": "Urban"
        }
        
        response = requests.post(
            f"{BASE_URL}/applications",
            json=invalid_data,
            timeout=TIMEOUT
        )
        assert response.status_code >= 400


# Manual test function for quick testing
def manual_test():
    """Run manual tests without pytest."""
    print("\n" + "="*60)
    print("Loan Prediction API - Manual Test")
    print("="*60)
    
    # Test 1: Health Check
    print("\n1. Testing API Health...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=TIMEOUT)
        if response.status_code == 200:
            print("   ✓ API is healthy")
        else:
            print(f"   ✗ API health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ✗ Cannot connect to API: {str(e)}")
        print("   Make sure backend is running: python -m uvicorn backend.app.main:app --reload")
        return
    
    # Test 2: Save Application
    print("\n2. Testing Save Application...")
    sample_data = {
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
    
    try:
        response = requests.post(f"{BASE_URL}/applications", json=sample_data, timeout=TIMEOUT)
        if response.status_code == 201:
            result = response.json()
            loan_id = result["loan_id"]
            print(f"   ✓ Application saved with Loan ID: {loan_id}")
        else:
            print(f"   ✗ Save failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return
    
    # Test 3: Get Application
    print(f"\n3. Testing Get Application (ID: {loan_id})...")
    try:
        response = requests.get(f"{BASE_URL}/applications/{loan_id}", timeout=TIMEOUT)
        if response.status_code == 200:
            result = response.json()
            print(f"   ✓ Application retrieved")
            print(f"   Income: ₹{result['applicant_income']:,.0f}")
            print(f"   Loan Amount: ₹{result['loan_amount']:,.0f}")
        else:
            print(f"   ✗ Get failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return
    
    # Test 4: Make Prediction
    print(f"\n4. Testing Prediction (ID: {loan_id})...")
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json={"loan_id": loan_id},
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            result = response.json()
            prediction_text = "APPROVED ✓" if result["prediction"] == 1 else "REJECTED ✗"
            print(f"   ✓ Prediction: {prediction_text}")
            print(f"   Confidence: {result['prediction_confidence']*100:.2f}%")
            print(f"   Message: {result['message']}")
        else:
            print(f"   ✗ Prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return
    
    # Test 5: List Applications
    print(f"\n5. Testing List Applications...")
    try:
        response = requests.get(f"{BASE_URL}/applications", timeout=TIMEOUT)
        if response.status_code == 200:
            results = response.json()
            print(f"   ✓ Found {len(results)} application(s)")
        else:
            print(f"   ✗ List failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    print("\n" + "="*60)
    print("All manual tests completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    manual_test()
