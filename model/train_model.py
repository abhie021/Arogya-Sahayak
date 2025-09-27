import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Go up one directory (from 'model' to 'Cummins_Hackathon') and then into 'database'
data_path = '../database/Maternal-Health-Risk.csv'
data = pd.read_csv(data_path)

# --- The rest of the script is the same ---

# Define Features (X) and Target (y)
features = ['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate']
target = 'RiskLevel'
X = data[features]
y = data[target]

# Initialize and Train the Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the trained model in the current folder ('model')
joblib.dump(model, 'maternal_risk_model.joblib')

print("✅ Model trained and saved in the 'model' folder!")