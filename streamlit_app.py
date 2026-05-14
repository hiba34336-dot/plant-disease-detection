import os
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input

st.set_page_config(
    page_title="🌿 Plant Disease Detector",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def load_model():
    model = tf.keras.models.load_model(
        "model/plant_disease_best.keras"
    )
    return model

model = load_model()

CLASS_NAMES = [
    'Apple___Apple_scab', 'Apple___Black_rot',
    'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight', 'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy', 'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch', 'Strawberry___healthy',
    'Tomato___Bacterial_spot', 'Tomato___Early_blight',
    'Tomato___Late_blight', 'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

disease_info = {
    "Apple scab": {
        "cause": "Fungal — Venturia inaequalis",
        "symptoms": "Dark olive-green spots on leaves and fruits",
        "treatment": "Apply fungicide sprays every 7-10 days. Remove infected leaves.",
        "prevention": "Choose resistant varieties. Ensure good air circulation.",
        "severity": "🟡 Medium"
    },
    "Apple Black rot": {
        "cause": "Fungal — Botryosphaeria obtusa",
        "symptoms": "Brown circular lesions on leaves, black rot on fruits",
        "treatment": "Prune infected branches. Apply copper-based fungicides.",
        "prevention": "Remove mummified fruits. Keep orchard clean.",
        "severity": "🔴 High"
    },
    "Tomato Early blight": {
        "cause": "Fungal — Alternaria solani",
        "symptoms": "Dark spots with concentric rings on lower leaves",
        "treatment": "Remove affected leaves. Apply copper-based fungicide.",
        "prevention": "Avoid overhead watering. Rotate crops yearly.",
        "severity": "🟡 Medium"
    },
    "Tomato Late blight": {
        "cause": "Water mold — Phytophthora infestans",
        "symptoms": "Water-soaked lesions turning brown and papery",
        "treatment": "Apply copper fungicide immediately. Remove infected plants.",
        "prevention": "Plant resistant varieties. Avoid wet conditions.",
        "severity": "🔴 Critical"
    },
    "Potato Early blight": {
        "cause": "Fungal — Alternaria solani",
        "symptoms": "Small dark spots with yellow halos on older leaves",
        "treatment": "Apply fungicide every 7-10 days. Improve drainage.",
        "prevention": "Use certified seed potatoes. Maintain plant spacing.",
        "severity": "🟡 Medium"
    },
    "Potato Late blight": {
        "cause": "Water mold — Phytophthora infestans",
        "symptoms": "Large irregular brown patches spreading rapidly",
        "treatment": "Destroy infected plants. Apply preventive fungicide.",
        "prevention": "Monitor weather. Apply preventive sprays regularly.",
        "severity": "🔴 Critical"
    },
    "Corn Common rust": {
        "cause": "Fungal — Puccinia sorghi",
        "symptoms": "Reddish-brown pustules on both leaf surfaces",
        "treatment": "Apply fungicide at early stage detection.",
        "prevention": "Plant resistant hybrid varieties.",
        "severity": "🟡 Medium"
    },
    "Grape Black rot": {
        "cause": "Fungal — Guignardia bidwellii",
        "symptoms": "Tan lesions with dark borders on leaves",
        "treatment": "Apply fungicide before bloom. Remove mummified fruits.",
        "prevention": "Prune for air circulation. Remove infected material.",
        "severity": "🔴 High"
    },
    "Strawberry Leaf scorch": {
        "cause": "Fungal — Diplocarpon earlianum",
        "symptoms": "Small purple spots enlarging and turning brown",
        "treatment": "Apply fungicide. Remove infected leaves immediately.",
        "prevention": "Avoid overhead irrigation. Use disease-free transplants.",
        "severity": "🟡 Medium"
    },
}

def predict_disease(image):
    image = image.convert("RGB")
    image = image.resize((224, 224))
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions[0])
    confidence = float(np.max(predictions[0])) * 100
    disease_name = CLASS_NAMES[predicted_index]
    parts = disease_name.split("___")
    plant = parts[0].replace("_", " ")
    condition = parts[1].replace("_", " ") if len(parts) > 1 else ""
    is_healthy = "healthy" in disease_name.lower()
    return {
        "plant": plant,
        "disease": condition,
        "confidence": confidence,
        "is_healthy": is_healthy
    }

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Poppins', sans-serif !important; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stAppViewContainer"] { background: #f0f7f0; }
.navbar {
    background: linear-gradient(90deg, #1b4332, #2d6a4f, #40916c);
    padding: 18px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-radius: 0 0 20px 20px;
    margin-bottom: 30px;
    box-shadow: 0 4px 20px rgba(27,67,50,0.3);
}
.navbar-brand { color: white; font-size: 1.6em; font-weight: 700; }
.navbar-stat {
    background: rgba(255,255,255,0.15);
    color: white; padding: 6px 16px;
    border-radius: 50px; font-size: 0.85em;
    border: 1px solid rgba(255,255,255,0.3);
    margin-left: 10px;
}
.page-title { text-align: center; margin-bottom: 35px; }
.page-title h1 { color: #1b4332; font-size: 2.8em; font-weight: 800; }
.page-title p { color: #40916c; font-size: 1.1em; }
.result-plant {
    text-align: center;
    background: linear-gradient(135deg, #d8f3dc, #b7e4c7);
    border-radius: 16px; padding: 20px; margin-bottom: 20px;
}
.result-plant-label {
    color: #40916c; font-size: 0.8em;
    font-weight: 600; text-transform: uppercase; letter-spacing: 2px;
}
.result-plant-name { color: #1b4332; font-size: 2em; font-weight: 800; }
.result-healthy {
    background: linear-gradient(135deg, #d8f3dc, #95d5b2);
    border: 2px solid #52b788; border-radius: 16px;
    padding: 20px; text-align: center; margin-bottom: 20px;
}
.result-disease {
    background: linear-gradient(135deg, #fff5f5, #ffe3e3);
    border: 2px solid #ff6b6b; border-radius: 16px;
    padding: 20px; text-align: center; margin-bottom: 20px;
}
.result-disease-text { color: #c0392b; font-size: 1.3em; font-weight: 700; margin-top: 8px; }
.result-healthy-text { color: #1b4332; font-size: 1.3em; font-weight: 700; margin-top: 8px; }
.confidence-box {
    background: #f8fffe; border-radius: 12px;
    padding: 15px 20px; margin-bottom: 20px;
    border: 1px solid #d8f3dc;
}
.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 15px; }
.info-card {
    background: #f8fffe; border-radius: 12px; padding: 14px;
    border: 1px solid #d8f3dc; border-top: 3px solid #40916c;
}
.info-card-red {
    background: #fff8f8; border-radius: 12px; padding: 14px;
    border: 1px solid #ffe3e3; border-top: 3px solid #ff6b6b;
}
.info-title { color: #40916c; font-size: 0.75em; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
.info-title-red { color: #e74c3c; font-size: 0.75em; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
.info-text { color: #2d6a4f; font-size: 0.88em; line-height: 1.5; }
.stButton > button {
    background: linear-gradient(135deg, #2d6a4f, #40916c) !important;
    color: white !important; border: none !important;
    border-radius: 50px !important; padding: 14px 40px !important;
    font-size: 1em !important; font-weight: 600 !important;
    width: 100% !important; margin-top: 15px !important;
}
.stProgress > div > div {
    background: linear-gradient(90deg, #2d6a4f, #74c69d) !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploadDropzone"] {
    background: #f8fffe !important;
    border: 2px dashed #74c69d !important;
    border-radius: 16px !important;
}
.how-step { text-align: center; padding: 20px 15px; }
.how-step-icon { font-size: 2.5em; margin-bottom: 12px; display: block; }
.how-step-title { color: #2d6a4f; font-weight: 700; font-size: 1em; margin-bottom: 8px; }
.how-step-text { color: #74c69d; font-size: 0.85em; line-height: 1.5; }
.footer {
    text-align: center; margin-top: 40px; padding: 25px;
    color: #74c69d; font-size: 0.85em;
    border-top: 1px solid #d8f3dc;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="navbar">
    <div class="navbar-brand">🌿 PlantGuard AI</div>
    <div>
        <span class="navbar-stat">⚡ EfficientNetB3</span>
        <span class="navbar-stat">🎯 96.45% Accuracy</span>
        <span class="navbar-stat">🌿 38 Diseases</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-title">
    <h1>🔬 Plant Disease Detection</h1>
    <p>Upload a plant leaf image and get instant AI-powered disease diagnosis</p>
</div>
""", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.markdown("""
    <div style="color:#1b4332;font-size:1.3em;font-weight:700;
         text-align:center;margin-bottom:5px">
         📸 Upload Leaf Image
    </div>
    <div style="color:#74c69d;font-size:0.9em;text-align:center;
         margin-bottom:20px">
         Clear well-lit photos give best results
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload leaf image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="📸 Your Plant Leaf",
                use_container_width=True)
        analyze = st.button("🔍 DETECT DISEASE NOW")
    else:
        st.markdown("""
        <div style="text-align:center;padding:40px 20px;
             background:white;border-radius:16px;
             border:2px dashed #95d5b2;margin-top:10px">
            <div style="font-size:4em">🌿</div>
            <div style="color:#74c69d;font-size:1em;
                 font-weight:500;margin-top:10px">
                Upload a plant leaf image to get started
            </div>
        </div>
        """, unsafe_allow_html=True)
        analyze = False

with right_col:
    st.markdown("""
    <div style="color:#1b4332;font-size:1.3em;font-weight:700;
         text-align:center;margin-bottom:20px;padding-bottom:15px;
         border-bottom:2px solid #d8f3dc">
         📊 Analysis Results
    </div>
    """, unsafe_allow_html=True)

    if not uploaded_file:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:#95d5b2">
            <div style="font-size:4em">🔬</div>
            <div style="color:#95d5b2;font-size:1.1em;
                 font-weight:600;margin-top:15px">
                Waiting for image...
            </div>
            <div style="color:#b7e4c7;font-size:0.9em;margin-top:10px">
                Upload a plant leaf image on the left
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif uploaded_file and not analyze:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px">
            <div style="font-size:4em">✅</div>
            <div style="color:#40916c;font-size:1.1em;
                 font-weight:600;margin-top:15px">
                Image uploaded!
            </div>
            <div style="color:#74c69d;font-size:0.9em;margin-top:10px">
                Click DETECT DISEASE NOW to analyze
            </div>
        </div>
        """, unsafe_allow_html=True)

    if analyze and uploaded_file:
        with st.spinner("🤖 AI analyzing your plant..."):
            image = Image.open(uploaded_file)
            result = predict_disease(image)

            st.markdown(f"""
            <div class="result-plant">
                <div class="result-plant-label">🌱 Plant Identified</div>
                <div class="result-plant-name">{result['plant']}</div>
            </div>
            """, unsafe_allow_html=True)

            if result['is_healthy']:
                st.markdown("""
                <div class="result-healthy">
                    <div style="font-size:2.5em">✅</div>
                    <div class="result-healthy-text">Plant is Healthy!</div>
                    <div style="color:#40916c;font-size:0.9em;margin-top:5px">
                        No disease detected. Keep up the good care!
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-disease">
                    <div style="font-size:2.5em">⚠️</div>
                    <div class="result-disease-text">
                        {result['disease']} Detected
                    </div>
                    <div style="color:#e74c3c;font-size:0.9em;margin-top:5px">
                        Disease identified — treatment advice below
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="confidence-box">
                <div style="display:flex;justify-content:space-between">
                    <span style="color:#1b4332;font-size:0.85em;font-weight:600">
                        🎯 Confidence Score
                    </span>
                    <span style="color:#40916c;font-size:0.85em;font-weight:700">
                        {result['confidence']:.2f}%
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(int(result['confidence']))

            if not result['is_healthy']:
                disease_key = f"{result['plant']} {result['disease']}"
                info = disease_info.get(disease_key, None)
                if info:
                    st.markdown(f"""
                    <div class="info-grid">
                        <div class="info-card">
                            <div class="info-title">🔬 Cause</div>
                            <div class="info-text">{info['cause']}</div>
                        </div>
                        <div class="info-card-red">
                            <div class="info-title-red">⚠️ Severity</div>
                            <div class="info-text">{info['severity']}</div>
                        </div>
                        <div class="info-card-red">
                            <div class="info-title-red">👁️ Symptoms</div>
                            <div class="info-text">{info['symptoms']}</div>
                        </div>
                        <div class="info-card">
                            <div class="info-title">💊 Treatment</div>
                            <div class="info-text">{info['treatment']}</div>
                        </div>
                        <div class="info-card"
                             style="grid-column:span 2">
                            <div class="info-title">🛡️ Prevention</div>
                            <div class="info-text">{info['prevention']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info(f"Consult an agricultural expert for {result['disease']} treatment.")

c1, c2, c3, c4 = st.columns(4)
steps = [
    ("📸", "Upload Image", "Take a clear photo of your plant leaf"),
    ("🤖", "AI Analysis", "EfficientNetB3 processes 54K+ features"),
    ("🔬", "Detection", "Identifies from 38 disease classes"),
    ("💊", "Get Treatment", "Instant treatment and prevention tips"),
]
for col, (icon, title, text) in zip([c1,c2,c3,c4], steps):
    with col:
        st.markdown(f"""
        <div class="how-step">
            <span class="how-step-icon">{icon}</span>
            <div class="how-step-title">{title}</div>
            <div class="how-step-text">{text}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    🌿 PlantGuard AI &nbsp;|&nbsp;
    Powered by EfficientNetB3 &nbsp;|&nbsp;
    96.45% Accuracy &nbsp;|&nbsp;
    TensorFlow + Streamlit
</div>
""", unsafe_allow_html=True)
