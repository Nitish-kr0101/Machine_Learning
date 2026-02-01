"""
Streamlit Frontend for Loan Prediction Application

This application provides a user-friendly interface for submitting loan applications
and receiving AI-powered predictions via the FastAPI backend.
"""

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from typing import Optional
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Loan Eligibility Predictor",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000/api/loans"
TIMEOUT = 10


# ===================== Helper Functions =====================

def get_api_health() -> bool:
    """Check if API is running."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=TIMEOUT)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def save_application(data: dict) -> Optional[dict]:
    """Save loan application to backend."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/applications",
            json=data,
            timeout=TIMEOUT
        )
        if response.status_code == 201:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to API: {str(e)}")
        return None


def get_application(loan_id: int) -> Optional[dict]:
    """Retrieve loan application from backend."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/applications/{loan_id}",
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            st.error(f"Loan ID {loan_id} not found")
            return None
        else:
            st.error(f"Error: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to API: {str(e)}")
        return None


def predict_loan(loan_id: int) -> Optional[dict]:
    """Get prediction for a loan application."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json={"loan_id": loan_id},
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            st.error(f"Loan ID {loan_id} not found")
            return None
        else:
            st.error(f"Prediction error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to API: {str(e)}")
        return None


def list_applications(skip: int = 0, limit: int = 100) -> Optional[list]:
    """Get all loan applications."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/applications",
            params={"skip": skip, "limit": limit},
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except requests.exceptions.RequestException:
        return []


# ===================== Page Styling =====================

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: bold;
        color: #2c3e50;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        color: #155724;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        color: #0c5460;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        border-radius: 5px;
        padding: 1rem;
        color: #856404;
    }
    </style>
""", unsafe_allow_html=True)

# ===================== Main App =====================

# Check API health
api_healthy = get_api_health()

# Header
st.markdown('<p class="main-header">🏦 Loan Eligibility Predictor</p>', unsafe_allow_html=True)

if not api_healthy:
    st.warning("⚠️ **API Connection Issue**: The backend API is not responding. Please ensure the FastAPI server is running on `http://localhost:8000`")
    st.info("To start the backend, run: `python -m uvicorn backend.app.main:app --reload`")
    st.stop()

st.success("✅ API Connected and Ready")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Action",
    ["New Application", "View & Predict", "Application History"],
    index=0
)

# ===================== Page: New Application =====================

if page == "New Application":
    st.markdown('<p class="section-header">📝 Submit New Loan Application</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Income Information")
        applicant_income = st.number_input(
            "Applicant Income (₹)",
            min_value=0.0,
            value=50000.0,
            step=1000.0,
            help="Monthly income of the primary applicant"
        )
        
        coapplicant_income = st.number_input(
            "Co-applicant Income (₹)",
            min_value=0.0,
            value=0.0,
            step=1000.0,
            help="Monthly income of the co-applicant (if any)"
        )
    
    with col2:
        st.subheader("📊 Loan Details")
        loan_amount = st.number_input(
            "Loan Amount (₹)",
            min_value=1.0,
            value=200000.0,
            step=10000.0,
            help="Loan amount requested"
        )
        
        loan_term = st.number_input(
            "Loan Term (months)",
            min_value=1.0,
            value=360.0,
            step=12.0,
            help="Duration of the loan"
        )
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("👤 Personal Information")
        
        married = st.selectbox(
            "Marital Status",
            ["Yes", "No"],
            help="Are you married?"
        )
        
        education = st.selectbox(
            "Education Level",
            ["Graduate", "Not Graduate"],
            help="Educational qualification"
        )
    
    with col4:
        st.subheader("📋 Credit Information")
        
        self_employed = st.selectbox(
            "Self Employed",
            ["No", "Yes"],
            help="Are you self-employed?"
        )
        
        credit_history = st.selectbox(
            "Credit History",
            [1.0, 0.0],
            format_func=lambda x: "Good (1)" if x == 1.0 else "No/Bad (0)",
            help="Your credit history status"
        )
        
        property_area = st.selectbox(
            "Property Area",
            ["Urban", "Semiurban", "Rural"],
            help="Location of the property"
        )
    
    # Save Application
    st.markdown("---")
    col_save, col_clear = st.columns(2)
    
    with col_save:
        if st.button("💾 Save Application", key="save_btn", use_container_width=True):
            with st.spinner("Saving application..."):
                application_data = {
                    "applicant_income": applicant_income,
                    "coapplicant_income": coapplicant_income,
                    "loan_amount": loan_amount,
                    "loan_amount_term": loan_term,
                    "credit_history": credit_history,
                    "married": married,
                    "self_employed": self_employed,
                    "education": education,
                    "property_area": property_area
                }
                
                result = save_application(application_data)
                
                if result:
                    st.session_state.last_loan_id = result.get("loan_id")
                    st.markdown(f"""
                        <div class="success-box">
                        <h4>✅ Application Saved Successfully!</h4>
                        <p><strong>Loan ID:</strong> {result['loan_id']}</p>
                        <p><strong>Submitted:</strong> {result['created_at']}</p>
                        <p>You can now proceed to make a prediction using this Loan ID.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2)
    
    with col_clear:
        if st.button("🔄 Clear Form", key="clear_btn", use_container_width=True):
            st.rerun()


# ===================== Page: View & Predict =====================

elif page == "View & Predict":
    st.markdown('<p class="section-header">🔮 View Application & Get Prediction</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        loan_id = st.number_input(
            "Enter Loan ID",
            min_value=1,
            value=1,
            step=1,
            help="Enter the Loan ID you received after saving your application"
        )
    
    with col2:
        st.write("")  # Spacing
        if st.button("🔍 Search", use_container_width=True):
            st.session_state.search_triggered = True
    
    # Search and display application
    if "search_triggered" in st.session_state and st.session_state.search_triggered:
        with st.spinner("Fetching application details..."):
            application = get_application(loan_id)
        
        if application:
            # Display Application Details
            st.markdown("### 📋 Application Details")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Applicant Income", f"₹{application['applicant_income']:,.0f}")
                st.metric("Loan Amount", f"₹{application['loan_amount']:,.0f}")
                st.metric("Education", application['education'])
                st.metric("Self Employed", application['self_employed'])
            
            with col2:
                st.metric("Co-applicant Income", f"₹{application['coapplicant_income']:,.0f}")
                st.metric("Loan Term", f"{int(application['loan_amount_term'])} months")
                st.metric("Marital Status", application['married'])
                st.metric("Property Area", application['property_area'])
            
            # Show Current Prediction Status
            st.markdown("### 🎯 Prediction Status")
            
            if application.get('prediction') is not None:
                # Already predicted
                prediction_text = "✅ APPROVED" if application['prediction'] == 1 else "❌ REJECTED"
                confidence = application.get('prediction_confidence', 0) * 100
                
                st.markdown(f"""
                    <div class="success-box">
                    <h4>{prediction_text}</h4>
                    <p><strong>Confidence:</strong> {confidence:.2f}%</p>
                    <p><strong>Prediction Date:</strong> {application['prediction_timestamp']}</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="info-box">
                    <p>⏳ <strong>No prediction yet.</strong> Click the button below to run the ML model.</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Prediction Button
            st.markdown("---")
            col_pred, col_new = st.columns(2)
            
            with col_pred:
                if st.button("🚀 Get Prediction", key="predict_btn", use_container_width=True):
                    with st.spinner("Running ML model and generating prediction..."):
                        prediction_result = predict_loan(loan_id)
                    
                    if prediction_result:
                        prediction_text = "✅ APPROVED" if prediction_result['prediction'] == 1 else "❌ REJECTED"
                        
                        st.markdown(f"""
                            <div class="success-box">
                            <h4>{prediction_text}</h4>
                            <p><strong>Confidence:</strong> {prediction_result['prediction_confidence']*100:.2f}%</p>
                            <p><strong>Message:</strong> {prediction_result['message']}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.session_state.search_triggered = True
            
            with col_new:
                if st.button("➕ New Application", use_container_width=True):
                    st.session_state.search_triggered = False
                    st.switch_page("pages/new_application.py") if "pages" in st.session_state else None
                    st.rerun()


# ===================== Page: Application History =====================

elif page == "Application History":
    st.markdown('<p class="section-header">📊 All Loan Applications</p>', unsafe_allow_html=True)
    
    with st.spinner("Loading applications..."):
        applications = list_applications()
    
    if applications:
        # Create DataFrame for display
        df = pd.DataFrame([
            {
                "Loan ID": app['loan_id'],
                "Applicant Income": f"₹{app['applicant_income']:,.0f}",
                "Loan Amount": f"₹{app['loan_amount']:,.0f}",
                "Status": "✅ Approved" if app['prediction'] == 1 else ("❌ Rejected" if app['prediction'] == 0 else "⏳ Pending"),
                "Confidence": f"{app['prediction_confidence']*100:.1f}%" if app['prediction_confidence'] else "—",
                "Submitted": app['created_at'][:10],
                "Predicted": app['prediction_timestamp'][:10] if app['prediction_timestamp'] else "—"
            }
            for app in applications
        ])
        
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Loan ID": st.column_config.NumberColumn(width="small"),
                "Status": st.column_config.TextColumn(width="medium"),
                "Confidence": st.column_config.TextColumn(width="small"),
                "Submitted": st.column_config.TextColumn(width="small"),
                "Predicted": st.column_config.TextColumn(width="small"),
            }
        )
        
        # Statistics
        st.markdown("### 📈 Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        total = len(applications)
        approved = sum(1 for app in applications if app['prediction'] == 1)
        rejected = sum(1 for app in applications if app['prediction'] == 0)
        pending = sum(1 for app in applications if app['prediction'] is None)
        
        with col1:
            st.metric("Total Applications", total)
        with col2:
            st.metric("Approved", approved)
        with col3:
            st.metric("Rejected", rejected)
        with col4:
            st.metric("Pending", pending)
    
    else:
        st.info("📭 No applications found. Start by creating a new application!")


# ===================== Footer =====================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9rem;'>
    <p>🏦 Loan Eligibility Predictor | Powered by FastAPI, Streamlit & Machine Learning</p>
    <p>API Base URL: http://localhost:8000 | Frontend: Streamlit</p>
</div>
""", unsafe_allow_html=True)
