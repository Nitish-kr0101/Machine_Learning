import streamlit as st
import pickle
import numpy as np
import pandas as pd
import requests
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Customer Clustering System",
    page_icon="👥",
    layout="wide"
)

# Load model artifacts
@st.cache_resource
def load_model_artifacts():
    with open('customer_clustering_model.pkl', 'rb') as f:
        kmeans_model = pickle.load(f)
    
    with open('customer_scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    
    with open('cluster_metadata.pkl', 'rb') as f:
        metadata = pickle.load(f)
    
    return kmeans_model, scaler, metadata

kmeans_model, scaler, metadata = load_model_artifacts()
cluster_names = metadata['cluster_names']
cluster_characteristics = metadata['cluster_characteristics']
cluster_offers = metadata['cluster_offers']

# Title and description
st.title("🎯 Customer Clustering & Personalized Offers System")
st.markdown("---")

# Sidebar for navigation
page = st.sidebar.radio("Navigation", ["🏠 Home", "🔮 Predict Customer Cluster", "📊 Cluster Analytics", "ℹ️ About"])

if page == "🏠 Home":
    st.header("Welcome to Customer Clustering System")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Clusters", "3", "Customer Segments")
    
    with col2:
        st.metric("Model Type", "K-Means", "Unsupervised")
    
    with col3:
        st.metric("Features Used", "9", "Customer Attributes")
    
    st.markdown("### 📌 System Features")
    st.markdown("""
    - **Customer Segmentation**: Classify customers into 3 distinct clusters
    - **Personalized Offers**: Get tailored marketing offers for each customer
    - **Real-time Prediction**: Instant cluster prediction for new customers
    - **Analytics Dashboard**: Visualize cluster distribution and characteristics
    """)
    
    st.markdown("### 🎯 Available Clusters")
    
    for cluster_id, name in cluster_names.items():
        with st.expander(f"Cluster {cluster_id + 1}: {name}"):
            st.markdown("**Characteristics:**")
            for char in cluster_characteristics[name]:
                st.markdown(f"- {char}")
            
            st.markdown("**Suggested Offers:**")
            for offer in cluster_offers[name]:
                st.markdown(f"✅ {offer}")

elif page == "🔮 Predict Customer Cluster":
    st.header("🔮 Predict Customer Cluster")
    st.markdown("Enter customer details to predict their cluster and get personalized offers.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Personal Information")
        age = st.number_input("Age", min_value=18, max_value=80, value=30, step=1)
        gender = st.selectbox("Gender", ["Male", "Female"])
        annual_income = st.number_input("Annual Income (₹)", min_value=100000, max_value=3000000, value=500000, step=50000)
        total_spent = st.number_input("Total Spent (₹)", min_value=0, max_value=2000000, value=100000, step=10000)
    
    with col2:
        st.subheader("Shopping Behavior")
        monthly_purchases = st.number_input("Monthly Purchases", min_value=1, max_value=30, value=5, step=1)
        avg_order_value = st.number_input("Average Order Value (₹)", min_value=500, max_value=50000, value=3000, step=500)
        app_time = st.number_input("App Usage (Minutes/Day)", min_value=0, max_value=200, value=60, step=5)
        discount_usage = st.selectbox("Discount Usage", ["Low", "Medium", "High"])
        preferred_time = st.selectbox("Preferred Shopping Time", ["Day", "Night"])
    
    if st.button("🔍 Predict Cluster", type="primary"):
        # Encode inputs
        gender_encoded = 0 if gender == "Male" else 1
        discount_map = {'Low': 0, 'Medium': 1, 'High': 2}
        discount_encoded = discount_map[discount_usage]
        time_encoded = 0 if preferred_time == "Day" else 1
        
        # Create feature array
        customer_features = np.array([[
            age, gender_encoded, annual_income, total_spent,
            monthly_purchases, avg_order_value, app_time,
            discount_encoded, time_encoded
        ]])
        
        # Scale and predict
        customer_scaled = scaler.transform(customer_features)
        predicted_cluster = int(kmeans_model.predict(customer_scaled)[0])
        cluster_name = cluster_names[predicted_cluster]
        
        st.markdown("---")
        st.success(f"### Predicted Cluster: **{cluster_name}**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Cluster Characteristics")
            for char in cluster_characteristics[cluster_name]:
                st.markdown(f"- {char}")
        
        with col2:
            st.markdown("#### 🎁 Personalized Offers")
            for offer in cluster_offers[cluster_name]:
                st.markdown(f"✅ {offer}")
        
        # Display customer profile
        st.markdown("---")
        st.markdown("#### 👤 Customer Profile Summary")
        profile_df = pd.DataFrame({
            'Attribute': ['Age', 'Gender', 'Annual Income', 'Total Spent', 'Monthly Purchases', 
                         'Avg Order Value', 'App Time', 'Discount Usage', 'Preferred Time'],
            'Value': [str(age), str(gender), f"₹{annual_income:,}", f"₹{total_spent:,}", str(monthly_purchases),
                     f"₹{avg_order_value:,}", f"{app_time} min", str(discount_usage), str(preferred_time)]
        })
        st.dataframe(profile_df, width='stretch', hide_index=True)

elif page == "📊 Cluster Analytics":
    st.header("📊 Cluster Analytics Dashboard")
    
    # Create sample visualization data
    cluster_data = {
        'Cluster': [cluster_names[0], cluster_names[1], cluster_names[2]],
        'Customer Count': [54, 23, 19],  # Example data from your clustering
        'Avg Income': [634444, 298696, 1430526],
        'Avg Spending': [301019, 73696, 1015789],
        'Avg App Time': [73.8, 25.1, 147.0]
    }
    
    df_viz = pd.DataFrame(cluster_data)
    
    # Cluster distribution
    st.subheader("Customer Distribution Across Clusters")
    fig1 = px.pie(df_viz, values='Customer Count', names='Cluster', 
                  title='Cluster Distribution',
                  color_discrete_sequence=['#2ecc71', '#3498db', '#e74c3c'])
    st.plotly_chart(fig1, width='stretch')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Average Income by Cluster")
        fig2 = px.bar(df_viz, x='Cluster', y='Avg Income',
                     title='Average Annual Income',
                     color='Cluster',
                     color_discrete_sequence=['#2ecc71', '#3498db', '#e74c3c'])
        st.plotly_chart(fig2, width='stretch')
    
    with col2:
        st.subheader("Average Spending by Cluster")
        fig3 = px.bar(df_viz, x='Cluster', y='Avg Spending',
                     title='Average Total Spending',
                     color='Cluster',
                     color_discrete_sequence=['#2ecc71', '#3498db', '#e74c3c'])
        st.plotly_chart(fig3, width='stretch')
    
    st.subheader("App Engagement by Cluster")
    fig4 = px.bar(df_viz, x='Cluster', y='Avg App Time',
                 title='Average App Usage (Minutes/Day)',
                 color='Cluster',
                 color_discrete_sequence=['#2ecc71', '#3498db', '#e74c3c'])
    st.plotly_chart(fig4, width='stretch')
    
    # Cluster comparison table
    st.subheader("Cluster Comparison Table")
    st.dataframe(df_viz, width='stretch', hide_index=True)

else:  # About page
    st.header("ℹ️ About This System")
    
    st.markdown("""
    ### 🎯 Customer Clustering System
    
    This system uses **K-Means clustering** algorithm to segment customers into distinct groups 
    based on their shopping behavior, demographics, and engagement patterns.
    
    #### 📚 Features Used for Clustering:
    1. Age
    2. Gender
    3. Annual Income
    4. Total Spent
    5. Monthly Purchases
    6. Average Order Value
    7. App Usage Time
    8. Discount Usage Pattern
    9. Preferred Shopping Time
    
    #### 🔧 Technical Stack:
    - **Machine Learning**: K-Means Clustering (scikit-learn)
    - **API**: FastAPI
    - **Frontend**: Streamlit
    - **Data Processing**: pandas, numpy
    - **Visualization**: Plotly, Matplotlib
    
    #### 💡 Use Cases:
    - Targeted Marketing Campaigns
    - Personalized Product Recommendations
    - Customer Retention Strategies
    - Revenue Optimization
    - Customer Lifetime Value Prediction
    
    #### 📊 Model Performance:
    - **Number of Clusters**: 3
    - **Algorithm**: K-Means with Elbow Method
    - **Preprocessing**: StandardScaler for feature normalization
    - **Outlier Removal**: IQR method applied
    
    ---
    
    **Developed for Customer Analytics & Marketing Optimization**
    """)

# Footer
st.markdown("---")
st.markdown("**Customer Clustering System** | Powered by K-Means & Streamlit")
