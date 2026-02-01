import streamlit as st
import requests
import pandas as pd

# Set page config
st.set_page_config(page_title="Loan Eligibility Prediction", layout="wide")

# Title and description
st.title("🏦 Loan Eligibility Prediction System")
st.write("Fill in the applicant details to check if they are eligible for a loan")

# Sidebar for API configuration
st.sidebar.header("API Configuration")
api_url = st.sidebar.text_input("API URL", value="http://localhost:8000/predict", help="FastAPI endpoint URL")

# Create columns for better layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Income Details")
    applicant_income = st.number_input(
        "Applicant Income (in rupees)",
        min_value=0,
        value=50000,
        step=1000
    )
    
    coapplicant_income = st.number_input(
        "Co-applicant Income (in rupees)",
        min_value=0,
        value=25000,
        step=1000
    )
    
    loan_amount = st.number_input(
        "Loan Amount (in thousands)",
        min_value=0,
        value=300,
        step=10
    )

with col2:
    st.subheader("Loan Details")
    loan_amount_term = st.number_input(
        "Loan Amount Term (in months)",
        min_value=12,
        value=360,
        step=12
    )
    
    credit_history = st.selectbox(
        "Credit History",
        options=[1.0, 0.0],
        format_func=lambda x: "Good (1)" if x == 1.0 else "Bad (0)"
    )

# Personal details
col3, col4 = st.columns(2)

with col3:
    st.subheader("Personal Details")
    married = st.selectbox(
        "Married Status",
        options=["Yes", "No"]
    )
    
    self_employed = st.selectbox(
        "Self Employed",
        options=["No", "Yes"]
    )

with col4:
    st.subheader("Education & Area")
    education = st.selectbox(
        "Education",
        options=["Graduate", "Not Graduate"]
    )
    
    property_area = st.selectbox(
        "Property Area",
        options=["Urban", "Semiurban", "Rural"]
    )

# Create a button to make prediction
if st.button("🔍 Predict Loan Eligibility", use_container_width=True):
    # Prepare data
    user_data = {
        "ApplicantIncome": applicant_income,
        "CoapplicantIncome": coapplicant_income,
        "LoanAmount": loan_amount,
        "Loan_Amount_Term": loan_amount_term,
        "Credit_History": credit_history,
        "Married": married,
        "Self_Employed": self_employed,
        "Education": education,
        "Property_Area": property_area
    }
    
    try:
        # Make API request
        response = requests.post(api_url, json=user_data)
        
        if response.status_code == 200:
            result = response.json()
            prediction = result.get("predicted_output")
            
            # Display result
            st.divider()
            
            if prediction == 1:
                st.success("✅ **LOAN APPROVED**", icon="✅")
                st.balloons()
            else:
                st.error("❌ **LOAN REJECTED**", icon="❌")
                st.snow()
            
            # Display applicant details summary
            st.subheader("Applicant Summary")
            summary_data = {
                "Applicant Income": f"₹{applicant_income:,.0f}",
                "Co-applicant Income": f"₹{coapplicant_income:,.0f}",
                "Total Income": f"₹{applicant_income + coapplicant_income:,.0f}",
                "Loan Amount": f"₹{loan_amount * 1000:,.0f}",
                "Loan Term": f"{int(loan_amount_term)} months",
                "Credit History": "Good" if credit_history == 1.0 else "Bad",
                "Married": married,
                "Self Employed": self_employed,
                "Education": education,
                "Property Area": property_area
            }
            
            # Display as table
            summary_df = pd.DataFrame(list(summary_data.items()), columns=["Field", "Value"])
            st.table(summary_df)
            
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        st.error(
            "⚠️ **Connection Error**: Unable to connect to the API. "
            "Please make sure the FastAPI server is running on the specified URL."
        )
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    <small>Loan Eligibility Prediction System | Powered by FastAPI & Streamlit</small>
    </div>
    """,
    unsafe_allow_html=True
)
