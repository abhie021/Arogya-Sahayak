# AI-Based Early Disease Detection Web App

## Overview
India’s rural areas face a shortage of doctors, and timely diagnosis of health conditions can be challenging. This project is an **AI-assisted solution** designed to help in **early detection of diseases** such as diabetes, stroke risk, and maternal health risks using patient symptoms, medical records, or wearable data.  

The web application is built using **Streamlit** and leverages **machine learning models** to provide predictions that can assist healthcare workers and patients in making informed decisions.

---

## Features
- Predicts **maternal health risk** based on patient medical records.
- Can be extended to other conditions like **diabetes** and **stroke risk**.
- User-friendly **web interface** using Streamlit.
- Uses trained **RandomForestClassifier models** for prediction.
- Works with structured patient data and can be adapted for wearable inputs.

---

## Folder Structure

project/
│ app.py
│ requirements.txt
│
├───database
│ Maternal-Health-Risk.csv
│ Testing.csv
│ Training.csv
│
└───model
disease_label_encoder.joblib
disease_model.joblib
maternal_risk_model.joblib
train_model.py
train_multidisease_model.py


- `app.py`: Main Streamlit app file.  
- `database/`: CSV files containing patient records used for training and testing.  
- `model/`: Pre-trained models and scripts used to train models.

---

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/abhie021/Arogya-Sahayak.git
cd <repo-name>
```

2. **Create a virtual environment**
```bash
python -m venv venv
# Activate the environment
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the app**
```bash
streamlit run app.py
```

### Usage

- Open the Streamlit app in your browser.

- Input patient symptoms, medical records, or relevant health parameters.

- Click Predict to get the risk assessment.

- Use the prediction to assist healthcare decisions or early interventions.

### Dependencies

Python 3.8+

Streamlit

pandas

scikit-learn

joblib

- All dependencies are listed in requirements.txt.

### Notes

- This AI model is assistance-only and does not replace professional medical advice.

- Designed with rural healthcare workers in mind; minimal training required for usage.

- Ensure the input data format matches the training data for accurate predictions.

### Future Improvements

- Integrate wearable device data for real-time monitoring.

- Extend prediction to additional diseases such as diabetes, hypertension, and stroke.

- Build a mobile-friendly interface for easier field deployment.

### License

This project is licensed under the MIT License.

### Contact

- Developer: Abhi Murkute
- Email : murkutehemant21@gmail.com
