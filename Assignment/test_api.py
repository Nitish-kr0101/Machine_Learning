import requests
import json

# Test the FastAPI endpoints

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("=" * 60)
    print("Testing Health Check Endpoint")
    print("=" * 60)
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_get_clusters():
    """Test the get clusters endpoint"""
    print("=" * 60)
    print("Testing Get Clusters Endpoint")
    print("=" * 60)
    response = requests.get(f"{BASE_URL}/clusters")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Number of Clusters: {len(data['clusters'])}")
    for cluster in data['clusters']:
        print(f"\nCluster {cluster['cluster_id']}: {cluster['cluster_name']}")
    print()

def test_prediction():
    """Test the prediction endpoint"""
    print("=" * 60)
    print("Testing Prediction Endpoint")
    print("=" * 60)
    
    # Test Case 1: High-Value Customer
    print("\nTest Case 1: High-Value Customer")
    customer_data_1 = {
        "Age": 45,
        "Gender": "M",
        "AnnualIncome": 900000,
        "TotalSpent": 500000,
        "MonthlyPurchases": 15,
        "AvgOrderValue": 6000,
        "AppTimeMinutes": 110,
        "DiscountUsage": "Low",
        "PreferredShoppingTime": "Night"
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=customer_data_1)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Predicted Cluster: {result['cluster_name']}")
        print(f"Suggested Offers: {', '.join(result['suggested_offers'])}")
    else:
        print(f"Error: {response.text}")
    
    # Test Case 2: Price-Sensitive Customer
    print("\n" + "-" * 60)
    print("Test Case 2: Price-Sensitive Customer")
    customer_data_2 = {
        "Age": 28,
        "Gender": "F",
        "AnnualIncome": 350000,
        "TotalSpent": 50000,
        "MonthlyPurchases": 3,
        "AvgOrderValue": 1500,
        "AppTimeMinutes": 30,
        "DiscountUsage": "High",
        "PreferredShoppingTime": "Day"
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=customer_data_2)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Predicted Cluster: {result['cluster_name']}")
        print(f"Suggested Offers: {', '.join(result['suggested_offers'])}")
    else:
        print(f"Error: {response.text}")
    
    # Test Case 3: Value-Seeking Customer
    print("\n" + "-" * 60)
    print("Test Case 3: Value-Seeking Customer")
    customer_data_3 = {
        "Age": 35,
        "Gender": "F",
        "AnnualIncome": 600000,
        "TotalSpent": 250000,
        "MonthlyPurchases": 8,
        "AvgOrderValue": 3500,
        "AppTimeMinutes": 70,
        "DiscountUsage": "Medium",
        "PreferredShoppingTime": "Night"
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=customer_data_3)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Predicted Cluster: {result['cluster_name']}")
        print(f"Suggested Offers: {', '.join(result['suggested_offers'])}")
    else:
        print(f"Error: {response.text}")
    
    print()

if __name__ == "__main__":
    print("\n🔍 CUSTOMER CLUSTERING API - TEST SUITE\n")
    
    try:
        # Test all endpoints
        test_health_check()
        test_get_clusters()
        test_prediction()
        
        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API")
        print("Make sure the FastAPI server is running:")
        print("  python fastapi_app.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
