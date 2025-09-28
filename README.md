# 🩺 AI-Based Early Disease Detection Web App  

![App Banner](<img width="1919" height="1199" alt="Image" src="https://github.com/user-attachments/assets/5d18a2e6-eb04-4f26-a6ca-7aa3d4a7ebdd" />)  

🔗 **Live Demo on Streamlit:** [Click Here](https://your-streamlit-app-link.streamlit.app)  

## 🌍 Problem Statement  
In India’s rural areas, **shortage of doctors** and limited access to healthcare make **timely diagnosis** of diseases a challenge. Many patients go undiagnosed until conditions worsen.  

## 💡 Our Solution  
An **AI-assisted web application** that helps in **early detection of diseases** like:  
- 🍬 **Diabetes**  
- 🧠 **Stroke Risk**  
- 🤰 **Maternal Health Risks**  

The system leverages **patient symptoms, medical records, and wearable data** to generate predictions that can assist **healthcare workers & patients** in making informed decisions.  

---

## 🚀 Features  
✅ **Streamlit-based Web App** – lightweight and interactive UI  
✅ **Machine Learning Models** – trained for multiple health risks  
✅ **Early Detection** – assists in quicker diagnosis  
✅ **Scalable** – can be extended to other diseases  
✅ **Accessible** – designed for rural and low-resource areas  

---

## 🛠️ Tech Stack  
- **Frontend / UI**: Streamlit  
- **Backend**: Python  
- **ML Models**: Scikit-learn / Joblib  
- **Deployment**: Streamlit Cloud / GitHub  

---

## 📊 Workflow  
1. 📝 User enters **symptoms / health parameters**  
2. ⚙️ The app runs **ML models** on the input data  
3. 📌 Prediction is displayed with **risk category**  
4. 🏥 Helps patients & healthcare workers take **next steps**  

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
