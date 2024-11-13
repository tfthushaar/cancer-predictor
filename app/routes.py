from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from firebase_admin import auth, firestore
from app.models.user import User
from app.models import load_ml_models
from datetime import datetime
import numpy as np  # Add this import

# Initialize Firestore and load models
db = firestore.client()
model, scaler = load_ml_models()

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])  # Make sure this route exists
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            # Create user in Firebase
            firebase_user = auth.create_user(
                email=email,
                password=password
            )
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Registration error: {str(e)}', 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            firebase_user = auth.get_user_by_email(email)
            user = User(firebase_user.uid, firebase_user.email)
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        except Exception as e:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/home')
@login_required
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    if request.method == 'POST':
        try:
            # Get all form inputs
            feature_names = [
                'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
                'compactness_mean', 'concavity_mean', 'concave_points_mean', 'symmetry_mean',
                'fractal_dimension_mean', 'radius_se', 'texture_se', 'perimeter_se', 'area_se',
                'smoothness_se', 'compactness_se', 'concavity_se', 'concave_points_se',
                'symmetry_se', 'fractal_dimension_se', 'radius_worst', 'texture_worst',
                'perimeter_worst', 'area_worst', 'smoothness_worst', 'compactness_worst',
                'concavity_worst', 'concave_points_worst', 'symmetry_worst', 'fractal_dimension_worst'
            ]
            
            # Collect features from form
            features = []
            for feature in feature_names:
                value = float(request.form.get(feature, 0))
                features.append(value)
            
            # Convert to numpy array and reshape
            features_array = np.array(features).reshape(1, -1)
            
            # Make prediction
            features_scaled = scaler.transform(features_array)
            prediction = model.predict(features_scaled)
            
            # Determine result
            result = "Malignant" if prediction[0][0] > 0.5 else "Benign"
            probability = float(prediction[0][0]) * 100
            
            # Store prediction in Firestore
            doc_ref = db.collection('predictions').document()
            doc_ref.set({
                'user_id': current_user.id,
                'features': dict(zip(feature_names, features)),
                'prediction': result,
                'probability': probability,
                'timestamp': datetime.now()
            })
            
            return render_template('result.html', 
                                 prediction=result, 
                                 probability=f"{probability:.2f}")
                                 
        except Exception as e:
            flash(f'Error making prediction: {str(e)}', 'error')
            return redirect(url_for('home'))

@app.route('/history')
@login_required
def history():
    predictions = db.collection('predictions')\
        .where('user_id', '==', current_user.id)\
        .order_by('timestamp', direction=firestore.Query.DESCENDING)\
        .limit(10)\
        .stream()
    
    history_list = []
    for pred in predictions:
        data = pred.to_dict()
        history_list.append(data)
    
    return render_template('history.html', predictions=history_list)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500