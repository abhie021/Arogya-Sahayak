import streamlit as st
import pandas as pd
import joblib
import time
from datetime import datetime
import os

# --- App Configuration ---
st.set_page_config(
    page_title="Arogya Sahayak | Health Assistant",
    page_icon="🩺",
    layout="wide"
)

# --- Database File ---
DATABASE_FILE = "patient_database.csv"

# --- 1. TRANSLATION DICTIONARY (Expanded) ---
translations = {
    # --- General & Sidebar ---
    "sidebar_title": {"en": "Controls", "mr": "नियंत्रणे", "hi": "नियंत्रण"},
    "language_label": {"en": "Select Language", "mr": "भाषा निवडा", "hi": "भाषा चुनें"},
    "tool_choice_label": {"en": "Navigation", "mr": "मार्गदर्शन", "hi": "नेविगेशन"},
    "sidebar_info": {
        "en": "**Arogya Sahayak** is a functional prototype for tracking patient health and assisting in early disease detection.",
        "mr": "**आरोग्य सहायक** हे रुग्णांच्या आरोग्याचा मागोवा घेण्यासाठी आणि रोगाच्या लवकर निदानासाठी मदत करणारे एक कार्यात्मक प्रोटोटाइप आहे.",
        "hi": "**आरोग्य सहायक** रोगी के स्वास्थ्य पर नज़र रखने और बीमारी का शीघ्र पता लगाने में सहायता के लिए एक कार्यात्मक प्रोटोटाइप है।"
    },
    
    # --- Page Names ---
    "home_page_name": {"en": "🏠 Home", "mr": "🏠 मुख्यपृष्ठ", "hi": "🏠 होम पेज"},
    "dashboard_name": {"en": "📊 Dashboard", "mr": "📊 डॅशबोर्ड", "hi": "📊 डैशबोर्ड"},
    "maternal_tool_name": {"en": "👩‍⚕️ Maternal Health", "mr": "👩‍⚕️ माता आरोग्य", "hi": "👩‍⚕️ मातृ स्वास्थ्य"},
    "disease_tool_name": {"en": "🩺 Disease Prediction", "mr": "🩺 रोग निदान", "hi": "🩺 रोग निदान"},
    "reports_name": {"en": "📈 Patient Tracking", "mr": "📈 रुग्ण ट्रॅकिंग", "hi": "📈 रोगी ट्रैकिंग"},

    # --- Homepage ---
    "home_title": {"en": "Welcome to Arogya Sahayak", "mr": "आरोग्य सहायक मध्ये आपले स्वागत आहे", "hi": "आरोग्य सहायक में आपका स्वागत है"},
    "home_subtitle": {"en": "Your Health Assistant for Diagnosis and Patient Record Management", "mr": "निदान आणि रुग्ण रेकॉर्ड व्यवस्थापनासाठी तुमचा आरोग्य सहायक", "hi": "निदान और रोगी रिकॉर्ड प्रबंधन के लिए आपका स्वास्थ्य सहायक"},
    "get_started": {"en": "To get started, select a tool from the navigation panel on the left.", "mr": "सुरुवात करण्यासाठी, डावीकडील नेव्हिगेशन पॅनलमधून एक साधन निवडा.", "hi": "आरंभ करने के लिए, बाईं ओर नेविगेशन पैनल से एक उपकरण चुनें।"},
    "feature_dashboard_title": {"en": "📊 Live Dashboard", "mr": "📊 थेट डॅशबोर्ड", "hi": "📊 लाइव डैशबोर्ड"},
    "feature_dashboard_desc": {"en": "Monitor real-time patient statistics from your saved records.", "mr": "तुमच्या जतन केलेल्या नोंदींमधून रुग्णांची रिअल-टाइम आकडेवारी तपासा.", "hi": "अपने सहेजे गए रिकॉर्ड से वास्तविक समय के रोगी आँकड़ों की निगरानी करें।"},
    "feature_prediction_title": {"en": "🧠 AI-Powered Diagnosis", "mr": "🧠 एआय-शक्तीवर आधारित निदान", "hi": "🧠 एआई-संचालित निदान"},
    "feature_prediction_desc": {"en": "Use predictive models for insights on maternal health and general diseases.", "mr": "माता आरोग्य आणि सर्वसाधारण रोगांवरील माहितीसाठी भविष्यवाणी मॉडेल्स वापरा.", "hi": "मातृ स्वास्थ्य और सामान्य बीमारियों की जानकारी के लिए भविष्य कहनेवाला मॉडल का उपयोग करें।"},
    "feature_reports_title": {"en": "📈 Patient Tracking & Reports", "mr": "📈 रुग्ण ट्रॅकिंग आणि अहवाल", "hi": "📈 रोगी ट्रैकिंग और रिपोर्ट"},
    "feature_reports_desc": {"en": "Search, view, and track patient history. Download the entire database as a CSV file.", "mr": "रुग्णांचा इतिहास शोधा, पहा आणि ट्रॅक करा. संपूर्ण डेटाबेस CSV फाइल म्हणून डाउनलोड करा.", "hi": "रोगी का इतिहास खोजें, देखें और ट्रैक करें। संपूर्ण डेटाबेस को CSV फ़ाइल के रूप में डाउनलोड करें।"},

    # --- Dashboard Page ---
    "dashboard_title": {"en": "Live Clinic Dashboard", "mr": "थेट क्लिनिक डॅशबोर्ड", "hi": "लाइव क्लिनिक डैशबोर्ड"},
    "connectivity_status": {"en": "System Status", "mr": "प्रणाली स्थिती", "hi": "सिस्टम स्थिति"},
    "operational": {"en": "Operational", "mr": "कार्यरत", "hi": "चालू"},
    "patient_overview": {"en": "Patient Database Overview", "mr": "रुग्ण डेटाबेस आढावा", "hi": "रोगी डेटाबेस अवलोकन"},
    "total_patients_db": {"en": "Total Records in DB", "mr": "डेटाबेसमध्ये एकूण नोंदी", "hi": "डेटाबेस में कुल रिकॉर्ड"},
    "high_risk_patients": {"en": "High-Risk Patients", "mr": "उच्च-जोखीम असलेले रुग्ण", "hi": "उच्च-जोखिम वाले रोगी"},
    "avg_age_db": {"en": "Average Patient Age", "mr": "सरासरी रुग्ण वय", "hi": "औसत रोगी आयु"},
    "risk_level_dist": {"en": "Patient Risk Level Distribution", "mr": "रुग्ण जोखीम पातळी वितरण", "hi": "रोगी जोखिम स्तर वितरण"},
    "no_data_dashboard": {"en": "No patient data available. Please save a record first.", "mr": "रुग्णाची माहिती उपलब्ध नाही. कृपया आधी एक नोंद जतन करा.", "hi": "कोई रोगी डेटा उपलब्ध नहीं है। कृपया पहले एक रिकॉर्ड सहेजें।"},

    # --- Maternal Health Page ---
    "maternal_title": {"en": "Maternal Health - New Entry", "mr": "माता आरोग्य - नवीन नोंद", "hi": "मातृ स्वास्थ्य - नई प्रविष्टि"},
    "maternal_desc": { "en": "Enter patient details to assess health risk. The result will be saved to the permanent database.", "mr": "आरोग्य जोखीम मूल्यांकन करण्यासाठी रुग्णाचे तपशील प्रविष्ट करा. निकाल कायमस्वरूपी डेटाबेसमध्ये जतन केला जाईल.", "hi": "स्वास्थ्य जोखिम का आकलन करने के लिए रोगी का विवरण दर्ज करें। परिणाम स्थायी डेटाबेस में सहेजा जाएगा।"},
    "patient_id": {"en": "Patient Name or ID", "mr": "रुग्णाचे नाव किंवा आयडी", "hi": "रोगी का नाम या आईडी"},
    "vitals_header": {"en": "Enter Patient Vitals", "mr": "रुग्णाचे तपशील प्रविष्ट करा", "hi": "रोगी के महत्त्वपूर्ण आँकड़े दर्ज करें"},
    "age": {"en": "Age", "mr": "वय", "hi": "आयु"}, "systolic_bp": {"en": "Systolic BP", "mr": "सिस्टोलिक बीपी", "hi": "सिस्टोलिक बीपी"},
    "diastolic_bp": {"en": "Diastolic BP", "mr": "डायस्टोलिक बीपी", "hi": "डायस्टोलिक बीपी"}, "bs": {"en": "Blood Sugar (mmol/L)", "mr": "रक्त शर्करा (mmol/L)", "hi": "रक्त शर्करा (mmol/L)"},
    "body_temp": {"en": "Body Temp (°F)", "mr": "शरीराचे तापमान (°F)", "hi": "शरीर का तापमान (°F)"}, "heart_rate": {"en": "Heart Rate (bpm)", "mr": "हृदय गती (bpm)", "hi": "हृदय गति (bpm)"},
    "assess_and_save_button": {"en": "Assess and Save Record", "mr": "मूल्यांकन करा आणि नोंद जतन करा", "hi": "आकलन करें और रिकॉर्ड सहेजें"},
    "result_header": {"en": "Assessment Result", "mr": "मूल्यांकन परिणाम", "hi": "मूल्यांकन परिणाम"},
    "outcome_prefix": {"en": "Predicted Risk", "mr": "संभाव्य जोखीम", "hi": "अनुमानित जोखिम"},
    "record_saved_success": {"en": "Record successfully saved to the database!", "mr": "नोंद यशस्वीरित्या डेटाबेसमध्ये जतन झाली!", "hi": "रिकॉर्ड सफलतापूर्वक डेटाबेस में सहेज लिया गया है!"},
    "error_patient_id": {"en": "Patient Name/ID is required.", "mr": "रुग्णाचे नाव/आयडी आवश्यक आहे.", "hi": "रोगी का नाम/आईडी आवश्यक है।"},
    "low_risk_rec": {"en": "Low risk. Continue regular check-ups.", "mr": "कमी जोखीम. नियमित तपासणी सुरू ठेवा.", "hi": "कम जोखिम। नियमित जांच जारी रखें।"},
    "mid_risk_rec": {"en": "Medium risk. Schedule a consultation with a doctor.", "mr": "मध्यम जोखीम. डॉक्टरांचा सल्ला घ्या.", "hi": "मध्यम जोखिम। डॉक्टर से परामर्श करें।"},
    "high_risk_rec": {"en": "High risk. Seek immediate medical attention.", "mr": "उच्च जोखीम. तात्काळ वैद्यकीय मदत घ्या.", "hi": "उच्च जोखिम। तत्काल चिकित्सा सहायता लें।"},
    
    # --- Patient Tracking/Reports Page ---
    "reports_title": {"en": "Patient Tracking and Reports", "mr": "रुग्ण ट्रॅकिंग आणि अहवाल", "hi": "रोगी ट्रैकिंग और रिपोर्ट"},
    "reports_desc": {"en": "Search for patients by name/ID to view their complete record history. You can also download the entire database.", "mr": "रुग्णांचा संपूर्ण रेकॉर्ड इतिहास पाहण्यासाठी त्यांच्या नावाने/आयडीने शोधा. तुम्ही संपूर्ण डेटाबेस देखील डाउनलोड करू शकता.", "hi": "रोगी का पूरा रिकॉर्ड इतिहास देखने के लिए नाम/आईडी से खोजें। आप संपूर्ण डेटाबेस भी डाउनलोड कर सकते हैं।"},
    "search_patient": {"en": "Search Patient by Name or ID...", "mr": "रुग्णाला नावाने किंवा आयडीने शोधा...", "hi": "रोगी को नाम या आईडी से खोजें..."},
    "no_records_db": {"en": "The patient database is empty. Add a new entry from the 'Maternal Health' page.", "mr": "रुग्ण डेटाबेस रिक्त आहे. 'माता आरोग्य' पृष्ठावरून नवीन नोंद जोडा.", "hi": "रोगी डेटाबेस खाली है। 'मातृ स्वास्थ्य' पृष्ठ से एक नई प्रविष्टि जोड़ें।"},
    "showing_results_for": {"en": "Showing results for", "mr": "यासाठी निकाल दर्शवित आहे", "hi": "के लिए परिणाम दिखाए जा रहे हैं"},
    "download_db_button": {"en": "Download Full Database (CSV)", "mr": "संपूर्ण डेटाबेस डाउनलोड करा (CSV)", "hi": "पूर्ण डेटाबेस डाउनलोड करें (CSV)"},
    
    # --- Common ---
    "analyzing": {"en": "Analyzing and saving...", "mr": "विश्लेषण आणि जतन करत आहे...", "hi": "विश्लेषण और सहेजा जा रहा है..."},
}

# --- 2. HELPER & DATABASE FUNCTIONS ---
def T(key):
    """Fetches a translated string."""
    return translations.get(key, {}).get(st.session_state.lang, key)

@st.cache_data
def load_models():
    """Loads all machine learning models, cached for performance."""
    maternal_model = joblib.load('model/maternal_risk_model.joblib')
    disease_model = joblib.load('model/disease_model.joblib')
    disease_encoder = joblib.load('model/disease_label_encoder.joblib')
    return maternal_model, disease_model, disease_encoder

@st.cache_data
def load_symptom_list():
    """Loads the symptom list from the training data."""
    symptom_data = pd.read_csv('database/Training.csv')
    return symptom_data.columns[:-1].tolist()

def load_patient_database():
    """Loads the patient database from the CSV file. Creates the file if it doesn't exist."""
    if not os.path.exists(DATABASE_FILE):
        # Create empty dataframe with correct columns if file doesn't exist
        df = pd.DataFrame(columns=[
            'PatientID', 'Timestamp', 'Age', 'SystolicBP', 'DiastolicBP',
            'BloodSugar', 'BodyTemp_F', 'HeartRate', 'RiskPrediction'
        ])
        df.to_csv(DATABASE_FILE, index=False)
    return pd.read_csv(DATABASE_FILE)

def add_record_to_database(record):
    """Appends a new patient record to the CSV database."""
    df = pd.DataFrame([record])
    df.to_csv(DATABASE_FILE, mode='a', header=not os.path.exists(DATABASE_FILE), index=False)

# --- Initialize session state ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'

# --- Load Models & Data ---
maternal_model, disease_model, disease_encoder = load_models()
symptom_list = load_symptom_list()

# --- ======================================================= ---
# ---                         SIDEBAR                         ---
# --- ======================================================= ---
with st.sidebar:
    st.title("Arogya Sahayak")
    
    lang_map = {"English": "en", "मराठी": "mr", "हिन्दी": "hi"}
    lang_options = list(lang_map.keys())
    reverse_lang_map = {v: k for k, v in lang_map.items()}
    current_lang_name = reverse_lang_map[st.session_state.lang]
    current_lang_index = lang_options.index(current_lang_name)
    lang_choice = st.selectbox(T("language_label"), options=lang_options, index=current_lang_index)
    st.session_state.lang = lang_map[lang_choice]
    
    st.divider()

    app_mode = st.radio(
        T("tool_choice_label"),
        [T("home_page_name"), T("dashboard_name"), T("maternal_tool_name"), T("disease_tool_name"), T("reports_name")],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.info(T("sidebar_info"))

# --- ======================================================= ---
# ---                          HOMEPAGE                       ---
# --- ======================================================= ---
if app_mode == T("home_page_name"):
    st.title(T("home_title"))
    st.markdown(f"#### {T('home_subtitle')}")
    st.write(T("get_started"))
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.markdown(f"**{T('feature_dashboard_title')}**")
            st.write(T('feature_dashboard_desc'))
    with col2:
        with st.container(border=True):
            st.markdown(f"**{T('feature_prediction_title')}**")
            st.write(T('feature_prediction_desc'))
    with col3:
        with st.container(border=True):
            st.markdown(f"**{T('feature_reports_title')}**")
            st.write(T('feature_reports_desc'))

# --- ======================================================= ---
# ---                        DASHBOARD                        ---
# --- ======================================================= ---
elif app_mode == T("dashboard_name"):
    st.title(T("dashboard_title"))
    patient_df = load_patient_database()

    if patient_df.empty:
        st.warning(T("no_data_dashboard"))
    else:
        total_patients = patient_df.shape[0]
        high_risk_count = patient_df[patient_df['RiskPrediction'] == 'High Risk'].shape[0]
        avg_age = int(patient_df['Age'].mean())
        
        risk_dist = patient_df['RiskPrediction'].value_counts().reset_index()
        risk_dist.columns = ['Risk Level', 'Count']

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label=T("connectivity_status"), value=T("operational"))
        with col2:
            st.metric(label=T("total_patients_db"), value=total_patients)
        with col3:
            st.metric(label=T("high_risk_patients"), value=high_risk_count)
        with col4:
            st.metric(label=T("avg_age_db"), value=f"{avg_age} yrs")

        st.divider()
        st.subheader(T("risk_level_dist"))
        st.bar_chart(risk_dist, x='Risk Level', y='Count', color="#ff4b4b")

# --- ======================================================= ---
# ---               MATERNAL HEALTH - NEW ENTRY               ---
# --- ======================================================= ---
elif app_mode == T("maternal_tool_name"):
    st.title(T("maternal_title"))
    st.write(T("maternal_desc"))
    
    with st.form("vitals_form"):
        patient_id = st.text_input(T("patient_id"))
        st.subheader(T("vitals_header"))
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input(T("age"), 10, 70, 25, 1)
            systolic_bp = st.number_input(T("systolic_bp"), 70, 180, 120, 1)
            diastolic_bp = st.number_input(T("diastolic_bp"), 40, 120, 80, 1)
        with col2:
            bs = st.number_input(T("bs"), 6.0, 19.0, 7.5, 0.1, "%.1f")
            body_temp = st.number_input(T("body_temp"), 96.0, 104.0, 98.6, 0.1, "%.1f")
            heart_rate = st.number_input(T("heart_rate"), 60, 100, 75, 1)
        
        submitted = st.form_submit_button(T("assess_and_save_button"), use_container_width=True, type="primary")

    if submitted:
        if not patient_id:
            st.error(T("error_patient_id"))
        else:
            input_data = pd.DataFrame({'Age': [age], 'SystolicBP': [systolic_bp], 'DiastolicBP': [diastolic_bp], 'BS': [bs], 'BodyTemp': [body_temp], 'HeartRate': [heart_rate]})
            with st.spinner(T("analyzing")):
                time.sleep(0.5)
                prediction = maternal_model.predict(input_data)[0]
                risk_map = {"low risk": "Low Risk", "mid risk": "Medium Risk", "high risk": "High Risk"}
                risk_result = risk_map.get(prediction, "Unknown")

                new_record = {
                    'PatientID': patient_id,
                    'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'Age': age, 'SystolicBP': systolic_bp, 'DiastolicBP': diastolic_bp,
                    'BloodSugar': bs, 'BodyTemp_F': body_temp, 'HeartRate': heart_rate,
                    'RiskPrediction': risk_result
                }
                add_record_to_database(new_record)
            
            st.success(T("record_saved_success"), icon="✅")
            st.divider()
            st.subheader(T("result_header"))
            
            if prediction == 'low risk':
                st.info(f"**{T('outcome_prefix')}: {risk_result}** - {T('low_risk_rec')}")
            elif prediction == 'mid risk':
                st.warning(f"**{T('outcome_prefix')}: {risk_result}** - {T('mid_risk_rec')}")
            else:
                st.error(f"**{T('outcome_prefix')}: {risk_result}** - {T('high_risk_rec')}")

# --- ======================================================= ---
# ---               GENERAL DISEASE PREDICTOR                 ---
# --- ======================================================= ---
elif app_mode == T("disease_tool_name"):
    st.title(T("disease_tool_name"))
    st.write("Select patient symptoms for a preliminary, AI-based diagnosis. This tool is for informational purposes only.")
    
    selected_symptoms = st.multiselect("Select Symptoms", options=symptom_list)

    if st.button("Predict Disease", use_container_width=True, type="primary"):
        if selected_symptoms:
            input_vector = [0] * len(symptom_list)
            for symptom in selected_symptoms:
                if symptom in symptom_list:
                    input_vector[symptom_list.index(symptom)] = 1
            
            with st.spinner("Analyzing symptoms..."):
                time.sleep(0.5)
                numeric_prediction = disease_model.predict([input_vector])[0]
                disease_name = disease_encoder.inverse_transform([numeric_prediction])[0]

            st.divider()
            st.success(f"**Predicted Condition:** {disease_name.replace('_', ' ').title()}")
            st.warning("**Disclaimer:** This is a prediction, not a final diagnosis. Consult a qualified doctor.")
        else:
            st.warning("Please select at least one symptom.")

# --- ======================================================= ---
# ---                 PATIENT TRACKING & REPORTS              ---
# --- ======================================================= ---
elif app_mode == T("reports_name"):
    st.title(T("reports_title"))
    st.write(T("reports_desc"))
    
    patient_df = load_patient_database()
    
    if patient_df.empty:
        st.info(T("no_records_db"))
    else:
        search_query = st.text_input(T("search_patient"), "")
        
        if search_query:
            results_df = patient_df[patient_df['PatientID'].astype(str).str.contains(search_query, case=False)]
            st.write(f"{T('showing_results_for')}: **{search_query}**")
        else:
            results_df = patient_df
        
        # Display dataframe with sorted results
        st.dataframe(results_df.sort_values(by='Timestamp', ascending=False), use_container_width=True)
        
        # Download button
        csv = patient_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=T("download_db_button"),
            data=csv,
            file_name=f"arogya_sahayak_full_database_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv',
            use_container_width=True,
            type="primary"
        )
