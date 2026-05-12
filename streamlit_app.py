import streamlit as st
import numpy as np
from PIL import Image
import io
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input

# ── PAGE CONFIG ───────────────────────────────────────────
st.set_page_config(
    page_title="🌿 Plant Disease Detector",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── LOAD MODEL ────────────────────────────────────────────
@st.cache_resource
def load_model():
    # @st.cache_resource means load model only ONCE
    # Not every time user uploads image
    # Saves time and memory
    model = tf.keras.models.load_model(
        "model/plant_disease_best.keras"
    )
    return model

model = load_model()

# ── CLASS NAMES ───────────────────────────────────────────
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

# ── DISEASE DATABASE ──────────────────────────────────────
disease_info = {
    "Apple scab": {
        "cause": "Fungal — Venturia inaequalis",
        "symptoms": "Dark olive-green spots on leaves and fruits",
        "treatment": "Apply fungicide every 7-10 days. Remove infected leaves.",
        "severity": "Medium",
        "prevention": "Choose resistant varieties. Ensure good air circulation."
    },
    "Apple Black rot": {
        "cause": "Fungal — Botryosphaeria obtusa",
        "symptoms": "Brown circular lesions on leaves, black rot on fruits",
        "treatment": "Prune infected branches. Apply copper-based fungicides.",
        "severity": "High",
        "prevention": "Remove mummified fruits. Prune regularly."
    },
    "Tomato Early blight": {
        "cause": "Fungal — Alternaria solani",
        "symptoms": "Dark spots with concentric rings on lower leaves",
        "treatment": "Remove affected leaves. Apply copper-based fungicide.",
        "severity": "Medium",
        "prevention": "Avoid overhead watering. Rotate crops yearly."
    },
    "Tomato Late blight": {
        "cause": "Water mold — Phytophthora infestans",
        "symptoms": "Water-soaked lesions turning brown and papery",
        "treatment": "Apply copper fungicide immediately. Remove all infected plants.",
        "severity": "Critical",
        "prevention": "Plant resistant varieties. Avoid wet conditions."
    },
    "Potato Early blight": {
        "cause": "Fungal — Alternaria solani",
        "symptoms": "Small dark spots with yellow halos on older leaves",
        "treatment": "Apply fungicide every 7-10 days. Improve field drainage.",
        "severity": "Medium",
        "prevention": "Use certified seed potatoes. Maintain proper spacing."
    },
    "Potato Late blight": {
        "cause": "Water mold — Phytophthora infestans",
        "symptoms": "Large irregular brown patches spreading rapidly",
        "treatment": "Destroy all infected plants. Apply preventive fungicide.",
        "severity": "Critical",
        "prevention": "Monitor weather. Apply preventive sprays."
    },
    "Corn Common rust": {
        "cause": "Fungal — Puccinia sorghi",
        "symptoms": "Small reddish-brown pustules on both leaf surfaces",
        "treatment": "Apply fungicide at early stage detection.",
        "severity": "Medium",
        "prevention": "Plant resistant hybrid varieties."
    },
    "Grape Black rot": {
        "cause": "Fungal — Guignardia bidwellii",
        "symptoms": "Tan lesions with dark borders on leaves and fruits",
        "treatment": "Apply fungicide before bloom. Remove mummified fruits.",
        "severity": "High",
        "prevention": "Prune for air circulation. Remove all infected material."
    },
    "Strawberry Leaf scorch": {
        "cause": "Fungal — Diplocarpon earlianum",
        "symptoms": "Small purple spots that enlarge and turn brown",
        "treatment": "Apply fungicide. Remove infected leaves immediately.",
        "severity": "Medium",
        "prevention": "Avoid overhead irrigation. Use disease-free transplants."
    },
    "Tomato Bacterial spot": {
        "cause": "Bacterial — Xanthomonas campestris",
        "symptoms": "Small water-soaked spots on leaves and fruits",
        "treatment": "Apply copper bactericide. Remove infected plants.",
        "severity": "High",
        "prevention": "Use disease-free seeds. Avoid working when wet."
    },
    "Tomato Leaf Mold": {
        "cause": "Fungal — Passalora fulva",
        "symptoms": "Yellow patches on upper leaf surface, mold below",
        "treatment": "Improve ventilation. Apply fungicide.",
        "severity": "Medium",
        "prevention": "Reduce humidity. Space plants properly."
    },
}

# ── PREDICT FUNCTION ──────────────────────────────────────
def predict_disease(image):
    # Resize image to 224x224 — what EfficientNet expects
    image = image.convert("RGB")
    image = image.resize((224, 224))

    # Convert to array and preprocess
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Make prediction
    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions[0])
    confidence = float(np.max(predictions[0])) * 100
    disease_name = CLASS_NAMES[predicted_index]

    # Clean up name
    parts = disease_name.split("___")
    plant = parts[0].replace("_", " ")
    condition = parts[1].replace("_", " ") if len(parts) > 1 else ""
    is_healthy = "healthy" in disease_name.lower()

    return {
        "plant": plant,
        "disease": condition,
        "confidence": confidence,
        "is_healthy": is_healthy,
        "full_name": disease_name
    }

# ── CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
* { font-family: 'Poppins', sans-serif !important; }
[data-testid="stAppViewContainer"] {
    background: #f5faf3;
}
.topbar {
    background: #1a3a2a;
    padding: 20px 30px;
    border-radius: 15px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.topbar-title {
    color: white;
    font-size: 1.8em;
    font-weight: 700;
}
.topbar-sub {
    color: #90d078;
    font-size: 0.95em;
}
.stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    margin-bottom: 25px;
}
.stat-card {
    background: white;
    border-radius: 12px;
    padding: 15px;
    text-align: center;
    border: 1px solid #d4edda;
}
.stat-number {
    color: #2d6a1f;
    font-size: 1.8em;
    font-weight: 700;
    display: block;
}
.stat-label {
    color: #666;
    font-size: 0.8em;
}
.left-panel {
    background: white;
    border-radius: 15px;
    padding: 25px;
    border: 1px solid #d4edda;
    height: 100%;
}
.right-panel {
    background: white;
    border-radius: 15px;
    padding: 25px;
    border: 1px solid #d4edda;
    height: 100%;
}
.panel-title {
    color: #1a3a2a;
    font-size: 1.1em;
    font-weight: 600;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 2px solid #d4edda;
}
.healthy-box {
    background: #f0faf0;
    border: 2px solid #52b788;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    margin: 15px 0;
}
.sick-box {
    background: #fff5f5;
    border: 2px solid #ff6b6b;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    margin: 15px 0;
}
.plant-title {
    color: #1a3a2a;
    font-size: 1.5em;
    font-weight: 700;
    text-align: center;
    margin: 10px 0;
}
.disease-title-sick {
    color: #cc0000;
    font-size: 1.2em;
    font-weight: 600;
}
.disease-title-healthy {
    color: #2d6a1f;
    font-size: 1.2em;
    font-weight: 600;
}
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 15px;
}
.info-box {
    background: #f5faf3;
    border-radius: 10px;
    padding: 12px;
    border-left: 4px solid #52b788;
}
.info-box-red {
    background: #fff5f5;
    border-radius: 10px;
    padding: 12px;
    border-left: 4px solid #ff6b6b;
}
.info-label {
    color: #2d6a1f;
    font-size: 0.75em;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 5px;
}
.info-label-red {
    color: #cc0000;
    font-size: 0.75em;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 5px;
}
.info-text {
    color: #333333;
    font-size: 0.9em;
    line-height: 1.4;
}
.conf-text {
    color: #2d6a1f;
    font-weight: 600;
    font-size: 0.95em;
}
.stButton > button {
    background: #1a3a2a !important;
    color: white !important;
    border-radius: 25px !important;
    padding: 12px 30px !important;
    font-size: 1em !important;
    font-weight: 600 !important;
    width: 100% !important;
    border: none !important;
}
.stButton > button:hover {
    background: #2d6a1f !important;
}
.stProgress > div > div {
    background: #2d6a1f !important;
    border-radius: 10px !important;
}
.footer {
    text-align: center;
    color: #888;
    font-size: 0.85em;
    padding: 20px;
    border-top: 1px solid #d4edda;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ── TOP BAR ───────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div>
        <div class="topbar-title">🌿 Plant Disease Detector</div>
        <div class="topbar-sub">
            AI-powered plant disease detection system
        </div>
    </div>
    <div style="text-align:right">
        <div style="color:#90d078;font-weight:600">
            96.45% Accuracy
        </div>
        <div style="color:#aaa;font-size:0.85em">
            EfficientNetB3 Model
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── STATS ROW ─────────────────────────────────────────────
st.markdown("""
<div class="stats-row">
    <div class="stat-card">
        <span class="stat-number">96.45%</span>
        <span class="stat-label">Model Accuracy</span>
    </div>
    <div class="stat-card">
        <span class="stat-number">38</span>
        <span class="stat-label">Disease Classes</span>
    </div>
    <div class="stat-card">
        <span class="stat-number">54K+</span>
        <span class="stat-label">Training Images</span>
    </div>
    <div class="stat-card">
        <span class="stat-number">14</span>
        <span class="stat-label">Crop Types</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── MAIN CONTENT ──────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="panel-title">📸 Upload Plant Image</div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image,
                caption="Your Plant Leaf",
                use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
        analyze = st.button("🔍 DETECT DISEASE NOW")

with col2:
    st.markdown("""
    <div class="panel-title">📊 Analysis Results</div>
    """, unsafe_allow_html=True)

    if not uploaded_file:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:#aaa;">
            <div style="font-size:4em">🌿</div>
            <div style="font-size:1.1em;margin-top:10px">
                Upload a plant leaf image to get started
            </div>
            <div style="font-size:0.85em;margin-top:5px">
                Supports JPG, JPEG, PNG
            </div>
        </div>
        """, unsafe_allow_html=True)

    if uploaded_file and 'analyze' in dir() and analyze:
        with st.spinner("🤖 AI analyzing your plant..."):
            image = Image.open(uploaded_file)
            result = predict_disease(image)

            # Plant name
            st.markdown(f"""
            <div class="plant-title">🌱 {result['plant']}</div>
            """, unsafe_allow_html=True)

            # Healthy or sick
            if result['is_healthy']:
                st.markdown(f"""
                <div class="healthy-box">
                    <div style="font-size:2.5em">✅</div>
                    <div class="disease-title-healthy">
                        Plant is Healthy!
                    </div>
                    <div style="color:#555;margin-top:8px;font-size:0.9em">
                        No disease detected.
                        Keep up the good care!
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="sick-box">
                    <div style="font-size:2.5em">⚠️</div>
                    <div class="disease-title-sick">
                        {result['disease']} Detected
                    </div>
                    <div style="color:#555;margin-top:8px;font-size:0.9em">
                        Disease identified —
                        see treatment below
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Confidence
            st.markdown(f"""
            <div class="conf-text">
                🎯 Confidence: {result['confidence']:.2f}%
            </div>
            """, unsafe_allow_html=True)
            st.progress(int(result['confidence']))

            # Disease info cards
            if not result['is_healthy']:
                disease_key = (
                    f"{result['plant']} {result['disease']}"
                )
                info = disease_info.get(disease_key, None)

                if info:
                    st.markdown(f"""
                    <div class="info-grid">
                        <div class="info-box">
                            <div class="info-label">Cause</div>
                            <div class="info-text">
                                {info['cause']}
                            </div>
                        </div>
                        <div class="info-box-red">
                            <div class="info-label-red">
                                Severity
                            </div>
                            <div class="info-text">
                                {info['severity']}
                            </div>
                        </div>
                        <div class="info-box">
                            <div class="info-label">Symptoms</div>
                            <div class="info-text">
                                {info['symptoms']}
                            </div>
                        </div>
                        <div class="info-box">
                            <div class="info-label">Treatment</div>
                            <div class="info-text">
                                {info['treatment']}
                            </div>
                        </div>
                    </div>
                    <div class="info-box" style="margin-top:10px">
                        <div class="info-label">Prevention</div>
                        <div class="info-text">
                            {info['prevention']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info(
                        f"Consult an agricultural expert "
                        f"for {result['disease']} treatment."
                    )

# ── HOW IT WORKS ──────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#1a3a2a;
     font-size:1.3em;font-weight:700;margin-bottom:15px">
    ⚡ How It Works
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
steps = [
    ("📸", "Upload Image", "Take a clear photo of your plant leaf"),
    ("🤖", "AI Analysis", "EfficientNetB3 analyzes 54K+ features"),
    ("🔬", "Detection", "Identifies from 38 disease classes"),
    ("💊", "Treatment", "Get instant treatment advice"),
]
for col, (icon, title, text) in zip([c1,c2,c3,c4], steps):
    with col:
        st.markdown(f"""
        <div style="background:white;border-radius:12px;
             padding:20px;text-align:center;
             border:1px solid #d4edda;height:100%">
            <div style="font-size:2em">{icon}</div>
            <div style="color:#1a3a2a;font-weight:600;
                 margin:8px 0">{title}</div>
            <div style="color:#666;font-size:0.85em">
                {text}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🌿 Plant Disease Detection System |
    EfficientNetB3 | Accuracy: 96.45% |
    TensorFlow + Streamlit
</div>
""", unsafe_allow_html=True)
