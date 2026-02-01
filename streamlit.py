import streamlit as st
import pandas as pd

st.set_page_config(page_title="Employee Dashboard", layout="wide")

st.title("📊 Employee Data Dashboard")

# Load data
df = pd.read_csv("employees.csv")

# ---------------- Filters ----------------
st.sidebar.header("Filter Employees")

department = st.sidebar.selectbox(
    "Department",
    ["All"] + sorted(df["department"].unique().tolist())
)

city = st.sidebar.selectbox(
    "City",
    ["All"] + sorted(df["city"].unique().tolist())
)

designation = st.sidebar.selectbox(
    "Designation",
    ["All"] + sorted(df["designation"].unique().tolist())
)

# Apply filters
filtered_df = df.copy()

if department != "All":
    filtered_df = filtered_df[filtered_df["department"] == department]

if city != "All":
    filtered_df = filtered_df[filtered_df["city"] == city]

if designation != "All":
    filtered_df = filtered_df[filtered_df["designation"] == designation]

# ---------------- Data Table ----------------
st.subheader("📋 Employee Records")
st.dataframe(filtered_df, use_container_width=True)

# ---------------- Visualizations ----------------
st.subheader("📈 Data Insights")

col1, col2 = st.columns(2)

# 1. Average Salary by Department
with col1:
    st.markdown("**Average Salary by Department**")
    avg_salary = (
        filtered_df.groupby("department")["salary"]
        .mean()
        .reset_index()
    )
    st.bar_chart(avg_salary.set_index("department"))

# 2. Experience vs Salary
with col2:
    st.markdown("**Experience vs Salary**")
    st.scatter_chart(
        filtered_df,
        x="experience",
        y="salary"
    )

# 3. Employee Count by City
st.markdown("**Employee Count by City**")
city_count = filtered_df["city"].value_counts()
st.bar_chart(city_count)
