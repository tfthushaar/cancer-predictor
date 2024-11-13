from flask import Flask
from flask_login import LoginManager
from config import Config
import firebase_admin
from firebase_admin import credentials
from app.models.user import User

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Firebase
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(app.config['FIREBASE_CONFIG'])
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Firebase initialization error: {e}")

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Import routes after app initialization
from app import routes