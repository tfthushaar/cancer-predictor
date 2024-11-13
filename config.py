import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    FIREBASE_CONFIG = os.path.join(basedir, 'firebase_config.json')
    MODEL_PATH = os.path.join(basedir, 'app', 'models', 'cancer_model.h5')
    SCALER_PATH = os.path.join(basedir, 'app', 'models', 'scaler.pkl')