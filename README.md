# Breast Cancer Prediction Web Application

A Flask-based web application that uses machine learning to predict breast cancer diagnosis based on tumor characteristics. The application integrates with Firebase for user authentication and data storage.

## Features

- User Authentication (Register/Login)
- Breast Cancer Prediction using Machine Learning
- Prediction History Tracking
- Secure Data Storage using Firebase
- Responsive Web Design

## Technologies Used

- Python 3.x
- Flask
- Firebase Authentication
- Cloud Firestore
- TensorFlow/Keras
- scikit-learn
- HTML/CSS
- Bootstrap


## Installation

1. Clone the repository:
   git clone <https://github.com/tfthushaar/cancer-predictor>
   cd cancer_predictor


2. Create a virtual environment and activate it:
   python -m venv venv


3. Install required packages:
   pip install -r requirements.txt


4. Set up Firebase:
- Create a new Firebase project
- Enable Authentication and Firestore
- Download your Firebase configuration file and save it as `firebase_config.json`

5. Create a `.env` file in the root directory:
   SECRET_KEY=your-secret-key
   FLASK_APP=run.py
   FLASK_ENV=development


## Running the Application

1. Make sure your virtual environment is activated
2. Run the Flask application: python run.py


## Usage

1. Register a new account or login with existing credentials
2. Enter tumor characteristics in the prediction form
3. Submit the form to get a prediction
4. View prediction history in the history page
5. Logout when finished


## Input Features

The prediction form requires the following tumor characteristics:

### Mean Values
- Radius
- Texture
- Perimeter
- Area
- Smoothness
- Compactness
- Concavity
- Concave points
- Symmetry
- Fractal dimension

### Standard Error Values
- All of the above measurements' standard errors

### Worst Values
- All of the above measurements' worst values


## Model Information

The machine learning model is trained on the Wisconsin Breast Cancer dataset. It uses the following features to make predictions:
- 30 input features (mean, standard error, and worst values)
- Binary classification (Benign/Malignant)
- Standardized input using StandardScaler


## Security

- User authentication is handled by Firebase Authentication
- Sensitive data is stored in Cloud Firestore
- CSRF protection enabled
- Password hashing handled by Firebase
- Environment variables for sensitive configuration


## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request


## Acknowledgments

- Wisconsin Breast Cancer Dataset
- Firebase Documentation
- Flask Documentation
- scikit-learn Documentation


## Future Improvements

- Add email verification
- Implement password reset functionality
- Add more detailed prediction explanations
- Implement user profile management
- Add data visualization for prediction history
- Implement batch prediction functionality
