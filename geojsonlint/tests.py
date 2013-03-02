import json

from django.utils import unittest
from django.test.client import Client

import sample_geojson as samples

GOOD_RESPONSE = {
    'status': 'ok'
}
JSON = 'application/json'


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
                                    content_type=JSON)

        self.assertEqual(json.loads(response.content), bad_type_message)


class TestValidateGoodType(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.post('/validate',
                                    data=json.dumps(samples.point),
                                    content_type=JSON)

        self.assertEqual(json.loads(response.content), GOOD_RESPONSE)


class TestValidateNullProperties(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        null_properties_feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-100, 80]
            },
            "properties": None
        }

        response = self.client.post('/validate',
                                    data=json.dumps(null_properties_feature),
                                    content_type=JSON)

        self.assertEqual(json.loads(response.content), GOOD_RESPONSE)


class TestValidateNullGeometry(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        null_properties_feature = {
            "type": "Feature",
            "geometry": None,
            "properties": {
                "city": "Littleton"
            }
        }

        response = self.client.post('/validate',
                                    data=json.dumps(null_properties_feature),
                                    content_type=JSON)

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
                                    content_type=JSON)

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
                data=json.dumps(not_an_object), content_type=JSON)

        self.assertEqual(json.loads(response.content), not_an_object_message)


class TestValidateHTTPMethods(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        post_response = self.client.post('/validate',
                data=json.dumps(samples.point), content_type=JSON)
        get_response = self.client.get('/validate')
        put_response = self.client.put('/validate',
                data=json.dumps(samples.point), content_type=JSON)
        delete_response = self.client.delete('/validate')

        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(get_response.status_code, 405)
        self.assertEqual(put_response.status_code, 405)
        self.assertEqual(delete_response.status_code, 405)


class TestValidateValidThings(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        resp_point = self.client.post('/validate',
                data=json.dumps(samples.point), content_type=JSON)
        resp_point_three = self.client.post('/validate',
                data=json.dumps(samples.point_three), content_type=JSON)
        resp_multipoint = self.client.post('/validate',
                data=json.dumps(samples.multipoint), content_type=JSON)
        resp_linestring = self.client.post('/validate',
                data=json.dumps(samples.linestring), content_type=JSON)
        resp_multilinestring = self.client.post('/validate',
                data=json.dumps(samples.multilinestring), content_type=JSON)
        resp_polygon = self.client.post('/validate',
                data=json.dumps(samples.polygon), content_type=JSON)
        resp_multipolygon = self.client.post('/validate',
                data=json.dumps(samples.multipolygon), content_type=JSON)
        resp_feature = self.client.post('/validate',
                data=json.dumps(samples.feature), content_type=JSON)
        resp_featurecollection = self.client.post('/validate',
                data=json.dumps(samples.featurecollection), content_type=JSON)
        resp_geometrycollection = self.client.post('/validate',
                data=json.dumps(samples.geometrycollection), content_type=JSON)

        self.assertEqual(json.loads(resp_point.content), GOOD_RESPONSE)
        self.assertEqual(json.loads(resp_point_three.content), GOOD_RESPONSE)
        self.assertEqual(json.loads(resp_multipoint.content), GOOD_RESPONSE)
        self.assertEqual(json.loads(resp_linestring.content), GOOD_RESPONSE)
        self.assertEqual(json.loads(resp_multilinestring.content), GOOD_RESPONSE)
        self.assertEqual(json.loads(resp_polygon.content), GOOD_RESPONSE)
        self.assertEqual(json.loads(resp_multipolygon.content), GOOD_RESPONSE)
        self.assertEqual(json.loads(resp_feature.content), GOOD_RESPONSE)
        self.assertEqual(json.loads(resp_featurecollection.content), GOOD_RESPONSE)
        self.assertEqual(json.loads(resp_geometrycollection.content), GOOD_RESPONSE)
