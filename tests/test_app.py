import unittest
from app import app
import json
import numpy as np
from firebase_admin import auth, firestore

class TestCancerPredictor(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.db = firestore.client()
        
        # Test user credentials
        self.test_email = "test@example.com"
        self.test_password = "testpassword123"
        
        # Create test user if doesn't exist
        try:
            self.test_user = auth.get_user_by_email(self.test_email)
        except:
            self.test_user = auth.create_user(
                email=self.test_email,
                password=self.test_password
            )

    def tearDown(self):
        # Clean up test data
        predictions = self.db.collection('predictions')\
            .where('user_id', '==', self.test_user.uid)\
            .stream()
        
        for pred in predictions:
            pred.reference.delete()

    def test_home_redirect_if_not_logged_in(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/login' in response.location)

    def test_login(self):
        response = self.app.post('/login', data={
            'email': self.test_email,
            'password': self.test_password
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_prediction(self):
        # Login first
        self.app.post('/login', data={
            'email': self.test_email,
            'password': self.test_password
        })

        # Test data
        test_data = {
            'radius_mean': 17.99,
            'texture_mean': 10.38,
            'perimeter_mean': 122.8,
            'area_mean': 1001,
            'smoothness_mean': 0.1184,
            'compactness_mean': 0.2776,
            'concavity_mean': 0.3001,
            'concave_points_mean': 0.1471,
            'symmetry_mean': 0.2419,
            'fractal_dimension_mean': 0.07871,
            'radius_se': 1.095,
            'texture_se': 0.9053,
            'perimeter_se': 8.589,
            'area_se': 153.4,
            'smoothness_se': 0.006399,
            'compactness_se': 0.04904,
            'concavity_se': 0.05373,
            'concave_points_se': 0.01587,
            'symmetry_se': 0.03003,
            'fractal_dimension_se': 0.006193,
            'radius_worst': 25.38,
            'texture_worst': 17.33,
            'perimeter_worst': 184.6,
            'area_worst': 2019,
            'smoothness_worst': 0.1622,
            'compactness_worst': 0.6656,
            'concavity_worst': 0.7119,
            'concave_points_worst': 0.2654,
            'symmetry_worst': 0.4601,
            'fractal_dimension_worst': 0.1189
        }

        response = self.app.post('/predict', 
                               data=test_data,
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Prediction Result' in response.data)

    def test_history(self):
        # Login first
        self.app.post('/login', data={
            'email': self.test_email,
            'password': self.test_password
        })

        response = self.app.get('/history')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Prediction History' in response.data)

    def test_logout(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Login' in response.data)

if __name__ == '__main__':
    unittest.main()