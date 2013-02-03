import json

from django.utils import unittest
from django.test.client import Client

GOOD_RESPONSE = {
    'status': 'ok'
}


class TestHome(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Validate your GeoJSON' in response.content)


class TestValidateBadType(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        bad_type = {
            "type": "Rhombus",
            "coordinates": [1, 2, 3, 4, 5]
        }
        bad_type_message = {
            'status': 'error',
            'message': '"Rhombus" is not a valid GeoJSON type.'
        }

        response = self.client.post('/validate', data=json.dumps(bad_type),
                                    content_type='application/json')

        self.assertEqual(json.loads(response.content), bad_type_message)


class TestValidateGoodType(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        good_type = {
            "type": "Point",
            "coordinates": [1, 2]
        }

        response = self.client.post('/validate', data=json.dumps(good_type),
                                    content_type='application/json')

        self.assertEqual(json.loads(response.content), GOOD_RESPONSE)


class TestValidateBadJSON(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        # Missing ending curly brace
        bad_json = """
        {
            "type": "LineString",
            "coordinates": [
                [1, 2],
                [3, 4],
                [5, 6]
            ]
        """
        bad_json_message = {
            'status': 'error',
            'message': 'POSTed data was not JSON serializeable.'
        }

        response = self.client.post('/validate', data=bad_json,
                                    content_type='application/json')

        self.assertEqual(json.loads(response.content), bad_json_message)


class TestValidateNotAnObject(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        not_an_object = [1, 2, 3, 'cat', 'house']
        not_an_object_message = {
            'status': 'error',
            'message': 'POSTed data was not a JSON object.'
        }

        response = self.client.post('/validate',
                                    data=json.dumps(not_an_object),
                                    content_type='application/json')

        self.assertEqual(json.loads(response.content), not_an_object_message)


class TestValidateHTTPMethods(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        geojson = {
            "type": "Point",
            "coordinates": [1, 2]
        }

        post_response = self.client.post('/validate',
                                         data=json.dumps(geojson),
                                         content_type='application/json')
        get_response = self.client.get('/validate')
        put_response = self.client.put('/validate',
                                         data=json.dumps(geojson),
                                         content_type='application/json')
        delete_response = self.client.delete('/validate')

        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(get_response.status_code, 405)
        self.assertEqual(put_response.status_code, 405)
        self.assertEqual(delete_response.status_code, 405)
