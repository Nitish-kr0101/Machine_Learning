import pandas as pd

# Read CSV file
df = pd.read_csv('employees.csv')

print("=== Display First 5 Rows ===")
print(df.head())

print("\n=== Data Info ===")
print(df.info())

print("\n=== Dataset Shape ===")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n=== Display Specific Columns ===")
print(df[['Name', 'Department', 'Salary']])

print("\n=== Statistical Summary ===")
print(df.describe())

print("\n=== Filter IT Department ===")
it_employees = df[df['Department'] == 'IT']
print(it_employees)

print("\n=== Average Salary by Department ===")
print(df.groupby('Department')['Salary'].mean())

print("\n=== Sorted by Salary (Descending) ===")
print(df.sort_values('Salary', ascending=False)[['Name', 'Department', 'Salary']])

print("\n=== Count Employees by Department ===")
print(df['Department'].value_counts())
