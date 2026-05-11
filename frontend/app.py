import streamlit as st
import requests
from PIL import Image
import io

# ── PAGE CONFIG ───────────────────────────────────────────
st.set_page_config(
    page_title="🌿 Plant Disease Detector",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Poppins', sans-serif !important; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* Page background */
[data-testid="stAppViewContainer"] {
    background: #f0f7f0;
}

/* Top navbar */
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

.navbar-brand {
    color: white;
    font-size: 1.6em;
    font-weight: 700;
    letter-spacing: 1px;
}

.navbar-stats {
    display: flex;
    gap: 25px;
}

.navbar-stat {
    background: rgba(255,255,255,0.15);
    color: white;
    padding: 6px 16px;
    border-radius: 50px;
    font-size: 0.85em;
    font-weight: 500;
    border: 1px solid rgba(255,255,255,0.3);
}

/* Page title */
.page-title {
    text-align: center;
    margin-bottom: 35px;
}

.page-title h1 {
    color: #1b4332;
    font-size: 2.8em;
    font-weight: 800;
    margin-bottom: 8px;
}

.page-title p {
    color: #40916c;
    font-size: 1.1em;
    font-weight: 400;
}

/* Left panel — upload */
.upload-panel {
    background: white;
    border-radius: 24px;
    padding: 35px 30px;
    box-shadow: 0 8px 30px rgba(27,67,50,0.1);
    border: 1px solid #d8f3dc;
    height: 100%;
}

.upload-panel-title {
    color: #1b4332;
    font-size: 1.3em;
    font-weight: 700;
    margin-bottom: 5px;
    text-align: center;
}

.upload-panel-sub {
    color: #74c69d;
    font-size: 0.9em;
    text-align: center;
    margin-bottom: 20px;
}

/* Right panel — results */
.result-panel {
    background: white;
    border-radius: 24px;
    padding: 35px 30px;
    box-shadow: 0 8px 30px rgba(27,67,50,0.1);
    border: 1px solid #d8f3dc;
    height: 100%;
}

.result-panel-title {
    color: #1b4332;
    font-size: 1.3em;
    font-weight: 700;
    margin-bottom: 20px;
    text-align: center;
    padding-bottom: 15px;
    border-bottom: 2px solid #d8f3dc;
}

/* Waiting state */
.waiting-state {
    text-align: center;
    padding: 60px 20px;
    color: #95d5b2;
}

.waiting-icon {
    font-size: 4em;
    margin-bottom: 15px;
}

.waiting-text {
    color: #74c69d;
    font-size: 1em;
}

/* Plant result */
.result-plant {
    text-align: center;
    background: linear-gradient(135deg, #d8f3dc, #b7e4c7);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
}

.result-plant-label {
    color: #40916c;
    font-size: 0.8em;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.result-plant-name {
    color: #1b4332;
    font-size: 2em;
    font-weight: 800;
}

/* Healthy result */
.result-healthy {
    background: linear-gradient(135deg, #d8f3dc, #95d5b2);
    border: 2px solid #52b788;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    margin-bottom: 20px;
}

.result-healthy-icon {
    font-size: 2.5em;
}

.result-healthy-text {
    color: #1b4332;
    font-size: 1.3em;
    font-weight: 700;
    margin-top: 8px;
}

.result-healthy-sub {
    color: #40916c;
    font-size: 0.9em;
    margin-top: 5px;
}

/* Disease result */
.result-disease {
    background: linear-gradient(135deg, #fff5f5, #ffe3e3);
    border: 2px solid #ff6b6b;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    margin-bottom: 20px;
}

.result-disease-icon {
    font-size: 2.5em;
}

.result-disease-text {
    color: #c0392b;
    font-size: 1.3em;
    font-weight: 700;
    margin-top: 8px;
}

.result-disease-sub {
    color: #e74c3c;
    font-size: 0.9em;
    margin-top: 5px;
}

/* Confidence */
.confidence-box {
    background: #f8fffe;
    border-radius: 12px;
    padding: 15px 20px;
    margin-bottom: 20px;
    border: 1px solid #d8f3dc;
}

.confidence-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
}

.confidence-title {
    color: #1b4332;
    font-size: 0.85em;
    font-weight: 600;
}

.confidence-value {
    color: #40916c;
    font-size: 0.85em;
    font-weight: 700;
}

/* Info cards */
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 15px;
}

.info-card {
    background: #f8fffe;
    border-radius: 12px;
    padding: 14px;
    border: 1px solid #d8f3dc;
    border-top: 3px solid #40916c;
}

.info-card-red {
    background: #fff8f8;
    border-radius: 12px;
    padding: 14px;
    border: 1px solid #ffe3e3;
    border-top: 3px solid #ff6b6b;
}

.info-title {
    color: #40916c;
    font-size: 0.75em;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}

.info-title-red {
    color: #e74c3c;
    font-size: 0.75em;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}

.info-text {
    color: #2d6a4f;
    font-size: 0.88em;
    line-height: 1.5;
    font-weight: 400;
}

/* Analyze button */
.stButton > button {
    background: linear-gradient(135deg, #2d6a4f, #40916c) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 14px 40px !important;
    font-size: 1em !important;
    font-weight: 600 !important;
    width: 100% !important;
    margin-top: 15px !important;
    box-shadow: 0 4px 15px rgba(45,106,79,0.3) !important;
    letter-spacing: 1px !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(45,106,79,0.4) !important;
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #2d6a4f, #74c69d) !important;
    border-radius: 10px !important;
}

/* File uploader */
[data-testid="stFileUploadDropzone"] {
    background: #f8fffe !important;
    border: 2px dashed #74c69d !important;
    border-radius: 16px !important;
}

/* How it works */
.how-section {
    margin-top: 50px;
    padding: 40px 30px;
    background: white;
    border-radius: 24px;
    box-shadow: 0 8px 30px rgba(27,67,50,0.08);
    border: 1px solid #d8f3dc;
}

.how-title {
    text-align: center;
    color: #1b4332;
    font-size: 1.8em;
    font-weight: 700;
    margin-bottom: 30px;
}

.how-step {
    text-align: center;
    padding: 20px 15px;
}

.how-step-icon {
    font-size: 2.5em;
    margin-bottom: 12px;
    display: block;
}

.how-step-title {
    color: #2d6a4f;
    font-weight: 700;
    font-size: 1em;
    margin-bottom: 8px;
}

.how-step-text {
    color: #74c69d;
    font-size: 0.85em;
    line-height: 1.5;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 40px;
    padding: 25px;
    color: #74c69d;
    font-size: 0.85em;
    border-top: 1px solid #d8f3dc;
}
</style>
""", unsafe_allow_html=True)

# ── DISEASE DATABASE ──────────────────────────────────────
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

# ══════════════════════════════════════════════════════════
# NAVBAR
# ══════════════════════════════════════════════════════════
st.markdown("""
<div class="navbar">
    <div class="navbar-brand">🌿 PlantGuard AI</div>
    <div class="navbar-stats">
        <span class="navbar-stat">⚡ EfficientNetB3</span>
        <span class="navbar-stat">🎯 96.45% Accuracy</span>
        <span class="navbar-stat">🌿 38 Diseases</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PAGE TITLE
# ══════════════════════════════════════════════════════════
st.markdown("""
<div class="page-title">
    <h1>🔬 Plant Disease Detection</h1>
    <p>Upload a plant leaf image and get instant AI-powered disease diagnosis</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SPLIT SCREEN — LEFT + RIGHT
# ══════════════════════════════════════════════════════════
left_col, right_col = st.columns([1, 1], gap="large")

# ── LEFT PANEL ────────────────────────────────────────────
with left_col:
    st.markdown("""
    <div class="upload-panel">
        <div class="upload-panel-title">📸 Upload Leaf Image</div>
        <div class="upload-panel-sub">
            Clear, well-lit photos give best results
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload leaf image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(
            image,
            caption="📸 Your Plant Leaf",
            use_container_width=True
        )
        analyze = st.button("🔍 DETECT DISEASE NOW")
    else:
        st.markdown("""
        <div style="text-align:center; padding:40px 20px;
             background:white; border-radius:16px;
             border: 2px dashed #95d5b2; margin-top:10px">
            <div style="font-size:4em">🌿</div>
            <div style="color:#74c69d; font-size:1em;
                 font-weight:500; margin-top:10px">
                Upload a plant leaf image<br>to get started
            </div>
            <div style="color:#b7e4c7; font-size:0.8em;
                 margin-top:8px">
                JPG, JPEG, PNG supported
            </div>
        </div>
        """, unsafe_allow_html=True)
        analyze = False

# ── RIGHT PANEL ───────────────────────────────────────────
with right_col:
    st.markdown("""
    <div class="result-panel-title">📊 Analysis Results</div>
    """, unsafe_allow_html=True)

    if not uploaded_file:
        st.markdown("""
        <div class="waiting-state">
            <div class="waiting-icon">🔬</div>
            <div style="color:#95d5b2; font-size:1.1em;
                 font-weight:600">
                Waiting for image...
            </div>
            <div class="waiting-text" style="margin-top:10px">
                Upload a plant leaf image on the left
                to see the AI diagnosis here
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif uploaded_file and not analyze:
        st.markdown("""
        <div class="waiting-state">
            <div class="waiting-icon">✅</div>
            <div style="color:#40916c; font-size:1.1em;
                 font-weight:600">
                Image uploaded!
            </div>
            <div class="waiting-text" style="margin-top:10px">
                Click the
                <strong style="color:#2d6a4f">
                    DETECT DISEASE NOW
                </strong>
                button to analyze
            </div>
        </div>
        """, unsafe_allow_html=True)

    if analyze and uploaded_file:
        with st.spinner("🤖 AI analyzing your plant..."):
            try:
                uploaded_file.seek(0)
                files = {"file": (
                    uploaded_file.name,
                    uploaded_file,
                    "image/jpeg"
                )}
                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    files=files
                )
                result = response.json()

                # Plant name
                st.markdown(f"""
                <div class="result-plant">
                    <div class="result-plant-label">
                        🌱 Plant Identified
                    </div>
                    <div class="result-plant-name">
                        {result['plant']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Healthy or diseased
                if result['is_healthy']:
                    st.markdown("""
                    <div class="result-healthy">
                        <div class="result-healthy-icon">✅</div>
                        <div class="result-healthy-text">
                            Plant is Healthy!
                        </div>
                        <div class="result-healthy-sub">
                            No disease detected.
                            Your plant looks great!
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-disease">
                        <div class="result-disease-icon">⚠️</div>
                        <div class="result-disease-text">
                            {result['disease']}
                        </div>
                        <div class="result-disease-sub">
                            Disease detected —
                            treatment advice below
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Confidence
                confidence_val = float(
                    result['confidence'].replace('%', ''))
                st.markdown(f"""
                <div class="confidence-box">
                    <div class="confidence-header">
                        <span class="confidence-title">
                            🎯 Confidence Score
                        </span>
                        <span class="confidence-value">
                            {result['confidence']}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(int(confidence_val))

                # Disease info cards
                if not result['is_healthy']:
                    disease_key = (
                        f"{result['plant']} {result['disease']}"
                    )
                    info = disease_info.get(disease_key, None)

                    if info:
                        st.markdown(f"""
                        <div class="info-grid">
                            <div class="info-card">
                                <div class="info-title">
                                    🔬 Cause
                                </div>
                                <div class="info-text">
                                    {info['cause']}
                                </div>
                            </div>
                            <div class="info-card">
                                <div class="info-title">
                                    ⚠️ Severity
                                </div>
                                <div class="info-text">
                                    {info['severity']}
                                </div>
                            </div>
                            <div class="info-card-red">
                                <div class="info-title-red">
                                    👁️ Symptoms
                                </div>
                                <div class="info-text">
                                    {info['symptoms']}
                                </div>
                            </div>
                            <div class="info-card">
                                <div class="info-title">
                                    💊 Treatment
                                </div>
                                <div class="info-text">
                                    {info['treatment']}
                                </div>
                            </div>
                            <div class="info-card"
                                 style="grid-column: span 2">
                                <div class="info-title">
                                    🛡️ Prevention
                                </div>
                                <div class="info-text">
                                    {info['prevention']}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="info-card">
                            <div class="info-title">
                                💊 Recommendation
                            </div>
                            <div class="info-text">
                                Consult an agricultural expert
                                for {result['disease']}
                                treatment advice.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            except Exception as e:
                st.error(
                    "❌ Backend not running! Start uvicorn first.")

# ══════════════════════════════════════════════════════════
# HOW IT WORKS
# ══════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="how-section">
    <div class="how-title">⚡ How It Works</div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
steps = [
    ("📸", "Upload Image",
     "Take a clear photo of your plant leaf"),
    ("🤖", "AI Analysis",
     "EfficientNetB3 processes 54K+ features"),
    ("🔬", "Disease Detection",
     "Identifies from 38 disease classes"),
    ("💊", "Get Treatment",
     "Instant treatment and prevention tips"),
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

# ── FOOTER ────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🌿 PlantGuard AI &nbsp;|&nbsp;
    Powered by EfficientNetB3 &nbsp;|&nbsp;
    96.45% Accuracy &nbsp;|&nbsp;
    TensorFlow + FastAPI + Streamlit
</div>
""", unsafe_allow_html=True)