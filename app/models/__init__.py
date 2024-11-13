from tensorflow.keras.models import load_model
import joblib
from config import Config
import os

def load_ml_models():
    """Load the trained model and scaler"""
    try:
        model_path = Config.MODEL_PATH
        scaler_path = Config.SCALER_PATH

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
        if not os.path.exists(scaler_path):
            raise FileNotFoundError(f"Scaler not found at {scaler_path}")

        model = load_model(model_path)
        scaler = joblib.load(scaler_path)
        return model, scaler
    except Exception as e:
        print(f"Error loading models: {e}")
        return None, None