# File: Z:\Cummins_Hackathon\model\train_multidisease_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# 1. Load the new dataset
try:
    data = pd.read_csv('../database/Training.csv')
except FileNotFoundError:
    print("Error: 'Training.csv' not found. Make sure it's in the 'database' folder.")
    exit()

# 2. Prepare the data
# The last column 'prognosis' is our target, everything else is a feature.
X = data.drop('prognosis', axis=1)
y = data['prognosis']

# 3. Encode the target labels
# Machine learning models need numbers, not text. LabelEncoder converts disease names to numbers (0, 1, 2...).
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# 4. Train the Random Forest Model
# n_estimators=100 means it will use 100 decision trees.
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y_encoded)

# 5. Save the Model and the Encoder
# We need to save the encoder to translate predictions back to disease names later.
joblib.dump(model, 'disease_model.joblib')
joblib.dump(le, 'disease_label_encoder.joblib')

print("✅ Multi-disease model and label encoder saved successfully in the 'model' folder!")
print(f"Model trained on {len(X.columns)} symptoms to predict {len(le.classes_)} diseases.")