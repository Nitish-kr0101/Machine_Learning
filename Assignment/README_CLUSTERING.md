# Customer Clustering System

## 📌 Project Overview
A complete customer segmentation system using K-Means clustering to classify customers into distinct groups and provide personalized marketing offers.

## 🎯 Features
- **K-Means Clustering**: Segments customers into 3 clusters
- **Outlier Removal**: IQR method for data cleaning
- **REST API**: FastAPI for predictions
- **Interactive UI**: Streamlit dashboard
- **Model Persistence**: Pickle files for model storage
- **Personalized Offers**: Cluster-based recommendations

## 📊 Clusters Identified
1. **High-Value Loyal Customers** - Premium segment with high spending
2. **Value-Seeking Regular Customers** - Mid-tier regular shoppers
3. **Price-Sensitive Occasional Customers** - Budget-conscious buyers

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_clustering.txt
```

### 2. Train the Model
Run the Jupyter notebook `customer_clustering.ipynb` to:
- Load and preprocess data
- Remove outliers
- Train K-Means model
- Save model artifacts (`.pkl` files)

### 3. Run FastAPI Server
```bash
python fastapi_app.py
```
API will be available at: `http://localhost:8000`

**API Endpoints:**
- `GET /` - API information
- `GET /health` - Health check
- `GET /clusters` - Get all cluster information
- `POST /predict` - Predict customer cluster

**Example API Request:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Age": 35,
    "Gender": "F",
    "AnnualIncome": 800000,
    "TotalSpent": 300000,
    "MonthlyPurchases": 10,
    "AvgOrderValue": 5000,
    "AppTimeMinutes": 90,
    "DiscountUsage": "Medium",
    "PreferredShoppingTime": "Night"
  }'
```

### 4. Run Streamlit App
```bash
streamlit run streamlit_clustering_app.py
```
App will open at: `http://localhost:8501`

## 📁 Project Structure
```
ml_ques/
├── customer_clustering.ipynb          # Main training notebook
├── CustomerData.csv                   # Dataset
├── customer_clustering_model.pkl      # Trained KMeans model
├── customer_scaler.pkl                # StandardScaler object
├── cluster_metadata.pkl               # Cluster names & offers
├── fastapi_app.py                     # FastAPI REST API
├── streamlit_clustering_app.py        # Streamlit dashboard
├── requirements_clustering.txt        # Dependencies
└── README_CLUSTERING.md               # This file
```

## 🔧 Technical Details

### Features Used (9)
1. Age
2. Gender (M/F → 0/1)
3. Annual Income
4. Total Spent
5. Monthly Purchases
6. Average Order Value
7. App Time (Minutes/Day)
8. Discount Usage (Low/Medium/High → 0/1/2)
9. Preferred Shopping Time (Day/Night → 0/1)

### Model Pipeline
1. **Data Loading** → Load CustomerData.csv
2. **Missing Value Imputation** → Median for numeric, Mode for categorical
3. **Categorical Encoding** → Label encoding for Gender, DiscountUsage, PreferredShoppingTime
4. **Outlier Removal** → IQR method (removed 20 outliers)
5. **Feature Scaling** → StandardScaler normalization
6. **Clustering** → K-Means with k=3
7. **Model Saving** → Pickle serialization

### Data Cleaning
- **Before Outlier Removal**: 100 customers
- **After Outlier Removal**: 80 customers
- **Outliers Removed**: 20 (8 from AnnualIncome, 5 from TotalSpent, 4 from AvgOrderValue)

## 🎨 Streamlit Dashboard Pages
1. **Home** - Overview and cluster information
2. **Predict Customer Cluster** - Interactive prediction form
3. **Cluster Analytics** - Visualizations and insights
4. **About** - System documentation

## 📊 Visualizations Available
- Customer count per cluster (Bar chart)
- Average spending per cluster (Bar chart)
- Average app usage per cluster (Bar chart)
- Income vs Spending scatter plot (Cluster separation)
- Cluster distribution (Pie chart in Streamlit)

## 💡 Use Cases
- **Marketing Teams**: Create targeted campaigns
- **Sales Teams**: Personalize customer interactions
- **Product Teams**: Understand customer preferences
- **Analytics Teams**: Track cluster evolution

## 🎁 Personalized Offers by Cluster

### High-Value Loyal Customers
- Exclusive early access to new products
- Premium membership with free express delivery

### Value-Seeking Regular Customers
- Festival discounts (10-15%)
- Loyalty reward points on every purchase

### Price-Sensitive Occasional Customers
- Flash sales and coupon-based discounts
- Free shipping on minimum order value

## 🔍 API Testing
Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## 📈 Model Evaluation
- **Algorithm**: K-Means Clustering
- **Number of Clusters**: 3 (based on business requirements)
- **Elbow Method**: Applied for validation
- **WCSS**: Calculated for k=1 to k=10

## ⚠️ Important Notes
- Ensure all `.pkl` files are in the same directory as the Python scripts
- Model was trained on 80 customers after outlier removal
- Features must be provided in the exact order during prediction
- API accepts categorical values as strings (e.g., "Male", "Female", "Low", "High")

## 🔄 Future Enhancements
- Add more visualization options
- Implement A/B testing for offers
- Add customer lifetime value prediction
- Integrate with CRM systems
- Deploy on cloud platforms

---

**Developed for Customer Analytics & Marketing Optimization**
