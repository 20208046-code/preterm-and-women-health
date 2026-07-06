import os
import io
# Use the legacy Keras 2 API (tf-keras). The ultrasound model is trained/saved
# with it, and tensorflow-metal is incompatible with the bundled Keras 3.
os.environ.setdefault("TF_USE_LEGACY_KERAS", "1")

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import traceback

# === For image prediction ===
import numpy as np

# TensorFlow / Keras are OPTIONAL. The ultrasound CNN feature only works if
# TensorFlow is installed AND the trained model file is present. If either is
# missing, the rest of the API (SVM/KNN tabular predictions) must still run, so
# we import lazily and degrade gracefully instead of crashing the whole server.
try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing import image
    TF_AVAILABLE = True
except Exception as e:  # ImportError or backend init failure
    load_model = None
    image = None
    TF_AVAILABLE = False
    print("[WARN] TensorFlow not available; ultrasound feature disabled:", e)

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# === Load SVM Model ===
try:
    svm_model = joblib.load(os.path.join(BASE_DIR, "svm_model.joblib"))
    svm_encoders = joblib.load(os.path.join(BASE_DIR, "svm_encoders.joblib"))
    svm_scaler = joblib.load(os.path.join(BASE_DIR, "svm_scaler.joblib"))
    print("[OK] Loaded SVM components")
except Exception as e:
    print("Error loading SVM:", e)
    svm_model = svm_encoders = svm_scaler = None

# === Load KNN Model ===
try:
    knn_model = joblib.load(os.path.join(BASE_DIR, "knn_model.joblib"))
    knn_encoders = joblib.load(os.path.join(BASE_DIR, "knn_encoders.joblib"))
    knn_scaler = joblib.load(os.path.join(BASE_DIR, "knn_scaler.joblib"))
    print("[OK] Loaded KNN components")
except Exception as e:
    print("Error loading KNN:", e)
    knn_model = knn_encoders = knn_scaler = None

# === Load Ultrasound Model (optional) ===
ULTRASOUND_MODEL_PATH = os.path.join(BASE_DIR, "efficientnet_fetal_ultrasound_model.h5")
ultrasound_labels = ['benign', 'malignant', 'normal']  # Alphabetical order of the dataset class folders
ultrasound_model = None
if TF_AVAILABLE and os.path.exists(ULTRASOUND_MODEL_PATH):
    try:
        ultrasound_model = load_model(ULTRASOUND_MODEL_PATH)
        print("[OK] Loaded ultrasound model")
    except Exception as e:
        print("Error loading ultrasound model:", e)
        ultrasound_model = None
else:
    print("[WARN] Ultrasound model not loaded (TensorFlow missing or model file absent).")

# Column order the scalers/models were fit on. The scaler enforces this exact
# order, so we must reindex to it before transforming (dict order is not enough).
FEATURE_ORDER = [
    "age_group",
    "reported_race_ethnicity",
    "previous_births",
    "tobacco_use_during_pregnancy",
    "adequate_prenatal_care",
]

# === Preprocess for Tabular Models ===
def preprocess_input(data, encoders):
    df = pd.DataFrame([data])
    df["previous_births"] = (
        df["previous_births"]
        .replace({"None": 0, "One": 1, "Two": 2, "Three or More": 3})
        .infer_objects(copy=False)
        .fillna(0)
        .astype(int)
    )

    categorical_columns = ["age_group", "reported_race_ethnicity", "tobacco_use_during_pregnancy", "adequate_prenatal_care"]
    for col in categorical_columns:
        if col in df.columns and col in encoders:
            df[col] = encoders[col].transform([df[col].values[0]])

    # Enforce the exact column order the model was trained on.
    return df[FEATURE_ORDER]

# === Health Check ===
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "models": {
            "svm": svm_model is not None,
            "knn": knn_model is not None,
            "ultrasound": ultrasound_model is not None,
        },
        "tensorflow_available": TF_AVAILABLE,
    })

# === Tabular Prediction Endpoint ===
@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = request.json
        model_type = input_data.get("model", "svm")
        features = input_data.get("features")

        if not features:
            return jsonify({"error": "Missing input features."}), 400

        if model_type == "svm" and svm_model:
            df = preprocess_input(features, svm_encoders)
            scaled = svm_scaler.transform(df)
            prediction = svm_model.predict(scaled)[0]
            return jsonify({"model": "svm", "prediction": int(prediction)})

        elif model_type == "knn" and knn_model:
            df = preprocess_input(features, knn_encoders)
            scaled = knn_scaler.transform(df)
            prediction = knn_model.predict(scaled)[0]
            return jsonify({"model": "knn", "prediction": int(prediction)})

        return jsonify({"error": "Model not found or invalid model type."}), 400

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

# === Ultrasound Image Prediction Endpoint ===
@app.route("/predict_ultrasound", methods=["POST"])
def predict_ultrasound():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files['image']
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return jsonify({"error": "Unsupported file format"}), 400

        if ultrasound_model is None:
            return jsonify({
                "error": "Ultrasound model is not available on this server. "
                         "Install TensorFlow and add 'efficientnet_fetal_ultrasound_model.h5'."
            }), 503

        # Preprocess image. EfficientNet expects raw [0, 255] pixels (it normalizes
        # internally), so do NOT divide by 255 — must match training in train_model.py.
        img = image.load_img(io.BytesIO(file.read()), target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)

        prediction = ultrasound_model.predict(img_array)[0]
        predicted_index = int(np.argmax(prediction))
        confidence = float(np.max(prediction)) * 100
        predicted_label = ultrasound_labels[predicted_index]

        return jsonify({
            "predicted_class": predicted_label,
            "confidence": round(confidence, 2),
            "probabilities": {ultrasound_labels[i]: round(float(p)*100, 2) for i, p in enumerate(prediction)}
        })

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

if __name__ == "__main__":
    app.run(debug=True)
