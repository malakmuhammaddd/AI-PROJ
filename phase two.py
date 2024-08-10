# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load the Breast Cancer dataset from the local CSV file
local_path = r"D:\AI\AI PROJ\AI PROJ\Breast_cancer_data.csv"
data = pd.read_csv(local_path, index_col="id")

# Map diagnosis to binary labels (Malignant: 1, Benign: 0)
data["diagnosis"] = data["diagnosis"].map({"M": 1, "B": 0})

# Drop the 'Unnamed: 32' column
data = data.drop(columns=['Unnamed: 32'])

# Separate features and target variable
X = data.drop("diagnosis", axis=1)
y = data["diagnosis"]

# Check for missing values
missing_values = X.isnull().sum()
if missing_values.any():
    print("Handling missing values...")
    
    # Impute missing values
    imputer = SimpleImputer(strategy="mean")
    X_imputed = imputer.fit_transform(X)
    X = pd.DataFrame(X_imputed, columns=X.columns)
else:
    print("No missing values found.")

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create a logistic regression model
model = LogisticRegression(random_state=42)

# Train the model
model.fit(X_train_scaled, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test_scaled)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

# Display the results
print(f"Accuracy: {accuracy:.4f}")
print("\nConfusion Matrix:")
print(conf_matrix)
print("\nClassification Report:")
print(classification_rep)
