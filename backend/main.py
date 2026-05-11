# This is our FastAPI backend
# It receives an image, runs it through our AI model
# and returns the disease name and confidence

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
from PIL import Image
import io

# Create FastAPI app
app = FastAPI(title="Plant Disease Detection API")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load our trained model
print("Loading model...")
model = tf.keras.models.load_model("model/plant_disease_best.keras")
print("✅ Model loaded!")

# These are our 38 disease class names
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
    'Grape___Black_rot', 'Grape___Esca_(Black_Measles)',
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

@app.get("/")
def home():
    return {"message": "🌿 Plant Disease Detection API is running!"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read the uploaded image
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    
    # Convert to RGB (in case image is PNG with transparency)
    image = image.convert("RGB")
    
    # Resize to 224x224 — what our model expects
    image = image.resize((224, 224))
    
    # Convert to numpy array and preprocess
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)
    
    # Use EfficientNet preprocessing
    from tensorflow.keras.applications.efficientnet import preprocess_input
    img_array = preprocess_input(img_array)
    
    # Make prediction
    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions[0])
    confidence = float(np.max(predictions[0])) * 100
    disease_name = CLASS_NAMES[predicted_index]
    
    # Clean up the name for display
    parts = disease_name.split("___")
    plant = parts[0].replace("_", " ")
    condition = parts[1].replace("_", " ") if len(parts) > 1 else ""
    
    return {
        "plant": plant,
        "disease": condition,
        "confidence": f"{confidence:.2f}%",
        "full_name": disease_name,
        "is_healthy": "healthy" in disease_name.lower()
    }
