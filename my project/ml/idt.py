# ==============================
# AI-Based Crime Pattern Analysis
# ==============================

# 1. Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, classification_report

# 2. Load Dataset
df = pd.read_csv("delhi_500_dataset.csv")

print("Dataset Loaded Successfully!\n")
print(df.head())

# 3. Data Preprocessing
# ----------------------

# Drop missing values
df.dropna(inplace=True)

# Convert date column if exists
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day

# Label Encoding
le = LabelEncoder()

categorical_columns = []

for col in df.columns:
    if df[col].dtype == 'object' or df[col].dtype == 'str':
        categorical_columns.append(col)

for col in categorical_columns:
    df[col] = le.fit_transform(df[col])

print("\nData after preprocessing:\n", df.head())
print(df.dtypes)

# 4. Feature Selection
# ----------------------

# Ensure target exists
if 'Case_Closed' not in df.columns:
    raise Exception("Column 'Case_Closed' not found in dataset!")

X = df.drop('Case_Closed', axis=1)
y = df['Case_Closed']

# Feature Scaling (important for ML)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 5. Train-Test Split
# ----------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# =====================================
# 6. Logistic Regression Model
# =====================================
print("\n--- Logistic Regression ---")

lr_model = LogisticRegression(max_iter=200)
lr_model.fit(X_train, y_train)

y_pred_lr = lr_model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred_lr))
print(classification_report(y_test, y_pred_lr))

# =====================================
# 7. Random Forest Model
# =====================================
print("\n--- Random Forest ---")

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

y_pred_rf = rf_model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred_rf))
print(classification_report(y_test, y_pred_rf))

# =====================================
# 8. K-Means Clustering (Hotspots)
# =====================================
print("\n--- K-Means Clustering ---")

# Choose only few features for clustering (avoid target)
kmeans_features = X_scaled

kmeans = KMeans(n_clusters=5, random_state=42)
clusters = kmeans.fit_predict(kmeans_features)

df['Cluster'] = clusters

# Plot clusters (first 2 features)
plt.figure()
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=clusters)
plt.title("Crime Hotspot Clusters")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.show()

# =====================================
# 9. Save Models
# =====================================
joblib.dump(lr_model, "logistic_model.pkl")
joblib.dump(rf_model, "random_forest_model.pkl")
joblib.dump(kmeans, "kmeans_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("\nModels saved successfully!")

# =====================================
# 10. Test Prediction (Sample)
# =====================================
print("\n--- Sample Prediction ---")

sample = X_test[0].reshape(1, -1)

lr_pred = lr_model.predict(sample)
rf_pred = rf_model.predict(sample)

print("Logistic Prediction:", lr_pred)
print("Random Forest Prediction:", rf_pred)