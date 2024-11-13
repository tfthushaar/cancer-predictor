import unittest
import numpy as np
from app.models import load_ml_models
from config import Config
import os

class TestMLModels(unittest.TestCase):
    def setUp(self):
        self.model, self.scaler = load_ml_models()
        
    def test_model_loading(self):
        self.assertIsNotNone(self.model)
        self.assertIsNotNone(self.scaler)
        
    def test_prediction(self):
        # Sample test data
        test_data = np.array([[
            17.99, 10.38, 122.8, 1001, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871,
            1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193,
            25.38, 17.33, 184.6, 2019, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189
        ]])
        
        # Scale the data
        scaled_data = self.scaler.transform(test_data)
        
        # Make prediction
        prediction = self.model.predict(scaled_data)
        
        # Check if prediction is in the expected range [0,1]
        self.assertTrue(0 <= prediction[0][0] <= 1)
        
    def test_scaler_transformation(self):
        # Test data
        test_data = np.array([[
            17.99, 10.38, 122.8, 1001, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871,
            1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193,
            25.38, 17.33, 184.6, 2019, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189
        ]])
        
        # Transform and inverse transform
        scaled_data = self.scaler.transform(test_data)
        reconstructed_data = self.scaler.inverse_transform(scaled_data)
        
        # Check if reconstruction is close to original
        np.testing.assert_array_almost_equal(test_data, reconstructed_data)

if __name__ == '__main__':
    unittest.main()