from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
from typing import Dict, List

app = FastAPI(title="Customer Clustering API", version="1.0")

# Load the saved models and metadata
with open('customer_clustering_model.pkl', 'rb') as f:
    kmeans_model = pickle.load(f)

with open('customer_scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('cluster_metadata.pkl', 'rb') as f:
    metadata = pickle.load(f)

cluster_names = metadata['cluster_names']
cluster_characteristics = metadata['cluster_characteristics']
cluster_offers = metadata['cluster_offers']
features = metadata['features']


class CustomerInput(BaseModel):
    Age: int
    Gender: str  # 'M' or 'F'
    AnnualIncome: float
    TotalSpent: float
    MonthlyPurchases: int
    AvgOrderValue: float
    AppTimeMinutes: int
    DiscountUsage: str  # 'Low', 'Medium', 'High'
    PreferredShoppingTime: str  # 'Day' or 'Night'


class ClusterResponse(BaseModel):
    cluster_id: int
    cluster_name: str
    characteristics: List[str]
    suggested_offers: List[str]
    customer_profile: Dict


@app.get("/")
def root():
    return {
        "message": "Customer Clustering API",
        "endpoints": {
            "/predict": "POST - Predict customer cluster",
            "/clusters": "GET - Get all cluster information",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": True}


@app.get("/clusters")
def get_clusters():
    """Get information about all clusters"""
    clusters_info = []
    for cluster_id, name in cluster_names.items():
        clusters_info.append({
            "cluster_id": cluster_id,
            "cluster_name": name,
            "characteristics": cluster_characteristics[name],
            "suggested_offers": cluster_offers[name]
        })
    return {"clusters": clusters_info}


@app.post("/predict", response_model=ClusterResponse)
def predict_cluster(customer: CustomerInput):
    """Predict the cluster for a new customer"""
    try:
        # Encode categorical variables
        gender_encoded = 0 if customer.Gender.upper() == 'M' else 1
        
        discount_map = {'LOW': 0, 'MEDIUM': 1, 'HIGH': 2}
        discount_encoded = discount_map.get(customer.DiscountUsage.upper(), 1)
        
        time_encoded = 0 if customer.PreferredShoppingTime.upper() == 'DAY' else 1
        
        # Create feature array in the correct order
        customer_features = np.array([[
            customer.Age,
            gender_encoded,
            customer.AnnualIncome,
            customer.TotalSpent,
            customer.MonthlyPurchases,
            customer.AvgOrderValue,
            customer.AppTimeMinutes,
            discount_encoded,
            time_encoded
        ]])
        
        # Scale the features
        customer_scaled = scaler.transform(customer_features)
        
        # Predict cluster
        predicted_cluster = int(kmeans_model.predict(customer_scaled)[0])
        cluster_name = cluster_names[predicted_cluster]
        
        # Prepare response
        response = ClusterResponse(
            cluster_id=predicted_cluster,
            cluster_name=cluster_name,
            characteristics=cluster_characteristics[cluster_name],
            suggested_offers=cluster_offers[cluster_name],
            customer_profile={
                "Age": customer.Age,
                "Gender": customer.Gender,
                "AnnualIncome": customer.AnnualIncome,
                "TotalSpent": customer.TotalSpent,
                "MonthlyPurchases": customer.MonthlyPurchases,
                "AvgOrderValue": customer.AvgOrderValue,
                "AppTimeMinutes": customer.AppTimeMinutes,
                "DiscountUsage": customer.DiscountUsage,
                "PreferredShoppingTime": customer.PreferredShoppingTime
            }
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
