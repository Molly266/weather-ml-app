
import unittest
from unittest.mock import patch
from app import app, classify_weather, load_model
import numpy as np


class TestUnit(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    # Test proper handling of missing input
    def test_post_missing_field(self):
        form_data = {
            'temperature': '270.277',
            'pressure': '1006',
            'humidity': '84',
            'wind_deg': '274',
            'rain_1h': '0',
            'rain_3h': '0',
            'snow': '0',
            'clouds': '9'
        }

        response = self.client.post('/', data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error processing input', response.data)

    # Test that the model can be loaded
    def test_model_can_be_loaded(self):
        model = load_model()
        self.assertIsNotNone(model)

    # Test clear classification
    def test_clear_classification_output(self):
        test_input = np.array(
            [269.686, 1002, 78, 0, 23, 0, 0, 0, 0]
        ).reshape(1, -1)

        class_result, _ = classify_weather(test_input)
        self.assertEqual(class_result, 'clear')

    # Test rainy classification
    def test_rainy_classification_output(self):
        test_input = np.array(
            [279.626, 998, 99, 1, 314, 0.3, 0, 0, 88]
        ).reshape(1, -1)

        class_result, _ = classify_weather(test_input)
        self.assertEqual(class_result, 'rainy')

    # Test that prediction index 3 maps to foggy
    @patch('app.load_model')
    def test_foggy_classification_output(self, mock_load_model):

        mock_model = mock_load_model.return_value
        mock_model.predict.return_value = [3]


        test_input = np.array(
            [289.47, 1015, 88, 2, 300, 0, 0, 0, 20]
        ).reshape(1, -1)

        class_result, _ = classify_weather(test_input)
        self.assertEqual(class_result, 'foggy')


if __name__ == '__main__':
    unittest.main()
