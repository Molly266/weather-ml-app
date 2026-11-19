
import unittest
from app import app


class TestModelAppIntegration(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_model_app_integration(self):
        # Valid test input
        form_data = {
            'temperature': '275.15',
            'pressure': '1013',
            'humidity': '85',
            'wind_speed': '3.6',
            'wind_deg': '180',
            'rain_1h': '0',
            'rain_3h': '0',
            'snow': '0',
            'clouds': '20'
        }

        response = self.client.post('/', data=form_data)

        # Check successful response
        self.assertEqual(response.status_code, 200)

        # Ensure that the result page includes a weather prediction
        self.assertIn(b'The weather is:', response.data)

        # Ensure that the result page includes prediction time
        self.assertIn(b'Prediction time:', response.data)

        # Check that classification is one of the valid classes
        html_text = response.data.decode('utf-8').lower()

        valid_classes = [
            'clear', 'cloudy', 'drizzly', 'foggy', 'hazey',
            'misty', 'rainy', 'smokey', 'thunderstorm'
        ]

        found = any(weather in html_text for weather in valid_classes)

        self.assertTrue(
            found,
            "The prediction is not one of the valid weather classes."
        )


if __name__ == '__main__':
    unittest.main()

