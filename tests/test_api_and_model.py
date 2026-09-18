import unittest
import json
import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app import app
from backend.model_service import model_service

class TestAccidentSeverityFramework(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'online')
        self.assertEqual(data['active_model'], 'V4')

    def test_feature_schema(self):
        response = self.app.get('/api/features')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('city', data['features'])
        self.assertIn('road_type', data['features'])

    def test_model_info(self):
        response = self.app.get('/api/model-info')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['model']['accuracy'], '68.90%')

    def test_prediction_api_v4(self):
        sample_payload = {
            "features": {
                "city": "Kolkata",
                "state": "West Bengal",
                "hour": 4,
                "day_of_week": "Saturday",
                "is_weekend": 1,
                "road_type": "highway",
                "lanes": 3,
                "traffic_signal": 0,
                "weather": "clear",
                "visibility": "high",
                "temperature": 33,
                "traffic_density": "low",
                "cause": "distraction",
                "vehicles_involved": 5,
                "is_peak_hour": 0
            }
        }
        response = self.app.post('/api/predict', data=json.dumps(sample_payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        # Verify exact required response structure
        self.assertTrue(data['success'])
        self.assertIn('prediction', data)
        self.assertIn(data['prediction']['class'], ['Minor', 'Major', 'Fatal'])
        self.assertIn('class_id', data['prediction'])
        self.assertIn('probability', data['prediction'])
        self.assertIn('explanation', data)
        self.assertGreater(len(data['explanation']), 0)
        self.assertIn('feature', data['explanation'][0])
        self.assertIn('importance', data['explanation'][0])
        self.assertEqual(data['model']['version'], 'V4')

    def test_invalid_payload_error_handling(self):
        response = self.app.post('/api/predict', data="invalid json string", content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
