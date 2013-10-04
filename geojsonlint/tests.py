import json

from django.utils import unittest
from django.test.client import Client

import sample_geojson as samples

GOOD_RESPONSE = {
    'status': 'ok'
}
JSON = 'application/json'


class RequestTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

class TestHome(RequestTestCase):

    def test_home(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)


class TestValidateBadType(RequestTestCase):

    def test_bad_type(self):
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


class TestValidateGoodType(RequestTestCase):

    def test_good_type(self):
        response = self.client.post('/validate',
                                    data=json.dumps(samples.point),
                                    content_type=JSON)

        self.assertEqual(json.loads(response.content), GOOD_RESPONSE)


class TestValidateBadPosition(RequestTestCase):

    def test_bad_position(self):
        response = self.client.post('/validate',
                                    data=json.dumps(samples.point_with_strings),
                                    content_type=JSON)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['status'], 'error')


class TestValidateNullProperties(RequestTestCase):

    def test_null_properties(self):
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


class TestValidateNullGeometry(RequestTestCase):

    def test_null_geometry(self):
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


class TestValidateFeatureBadGeometry(RequestTestCase):

    def test_bad_feature_collection_geom(self):
        bad_geom = {
            "features": [
                {
                    "geometry": {
                        "type": "BROKEN"
                    },
                    "properties": {},
                    "type": "Feature"
                }
            ],
            "type": "FeatureCollection"
        }

        response = self.client.post('/validate',
                                    data=json.dumps(bad_geom),
                                    content_type=JSON)
        self.assertEqual(json.loads(response.content), {'status': 'error', 'message': '"BROKEN" is not a valid GeoJSON type.'})

    def test_bad_feature_geom(self):
        bad_geom = {
            "geometry": {
                "type": "BROKEN"
            },
            "properties": {},
            "type": "Feature"
        }

        response = self.client.post('/validate',
                                    data=json.dumps(bad_geom),
                                    content_type=JSON)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['status'], 'error')

class TestFeatureCollectionBadFeatures(RequestTestCase):

    def test_is_not_list_or_tuple(self):
        bad_fc = {
            "type": "FeatureCollection",
            "features": 'lobster'
        }
        response = self.client.post('/validate',
                                    data=json.dumps(bad_fc),
                                    content_type=JSON)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['status'], 'error')
        self.assertEqual(response_json['message'], 'A FeatureCollection\'s "features" property must be an array.')

    def test_no_features(self):
        bad_fc = {
            "type": "FeatureCollection",
        }
        response = self.client.post('/validate',
                                    data=json.dumps(bad_fc),
                                    content_type=JSON)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['status'], 'error')
        self.assertEqual(response_json['message'], 'A FeatureCollection must have a "features" property.')


class TestGeometryCollectionBadGeometries(RequestTestCase):

    def test_is_not_list_or_tuple(self):
        bad_gc = {
            "type": "GeometryCollection",
            "geometries": 'lobster'
        }
        response = self.client.post('/validate',
                                    data=json.dumps(bad_gc),
                                    content_type=JSON)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['status'], 'error')
        self.assertEqual(response_json['message'], 'A GeometryCollection\'s "geometries" property must be an array.')

    def test_no_geometries(self):
        bad_gc = {
            "type": "GeometryCollection",
        }
        response = self.client.post('/validate',
                                    data=json.dumps(bad_gc),
                                    content_type=JSON)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['status'], 'error')
        self.assertEqual(response_json['message'], 'A GeometryCollection must have a "geometries" property.')


class TestValidateBadJSON(RequestTestCase):

    def test_bad_json(self):
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


class TestValidateNotAnObject(RequestTestCase):

    def test_not_an_object(self):
        not_an_object = [1, 2, 3, 'cat', 'house']
        not_an_object_message = {
            'status': 'error',
            'message': 'POSTed data was not a JSON object.'
        }

        response = self.client.post('/validate',
                                    data=json.dumps(not_an_object),
                                    content_type=JSON)

        self.assertEqual(json.loads(response.content), not_an_object_message)


class TestValidateHTTPMethods(RequestTestCase):

    def test_post(self):
        post_response = self.client.post('/validate',
                                         data=json.dumps(samples.point),
                                         content_type=JSON)
        self.assertEqual(post_response.status_code, 200)

    def test_get(self):
        get_response = self.client.get('/validate')
        self.assertEqual(get_response.status_code, 405)

    def test_put(self):
        put_response = self.client.put('/validate',
                                       data=json.dumps(samples.point),
                                       content_type=JSON)
        self.assertEqual(put_response.status_code, 405)

    def test_delete(self):
        delete_response = self.client.delete('/validate')
        self.assertEqual(delete_response.status_code, 405)


class TestValidateValidThings(RequestTestCase):

    def test_point(self):
        resp_point = self.client.post('/validate',
                                      data=json.dumps(samples.point),
                                      content_type=JSON)
        self.assertEqual(json.loads(resp_point.content), GOOD_RESPONSE)

    def test_point_three(self):
        resp_point_three = self.client.post('/validate',
                                            data=json.dumps(samples.point_three),
                                            content_type=JSON)
        self.assertEqual(json.loads(resp_point_three.content), GOOD_RESPONSE)

    def test_multipoint(self):
        resp_multipoint = self.client.post('/validate',
                                           data=json.dumps(samples.multipoint),
                                           content_type=JSON)
        self.assertEqual(json.loads(resp_multipoint.content), GOOD_RESPONSE)

    def test_linestring(self):
        resp_linestring = self.client.post('/validate',
                                           data=json.dumps(samples.linestring),
                                           content_type=JSON)
        self.assertEqual(json.loads(resp_linestring.content), GOOD_RESPONSE)

    def test_multilinestring(self):
        resp_multilinestring = self.client.post('/validate',
                                                data=json.dumps(samples.multilinestring),
                                                content_type=JSON)
        self.assertEqual(json.loads(resp_multilinestring.content), GOOD_RESPONSE)

    def test_polygon(self):
        resp_polygon = self.client.post('/validate',
                                        data=json.dumps(samples.polygon),
                                        content_type=JSON)
        self.assertEqual(json.loads(resp_polygon.content), GOOD_RESPONSE)

    def test_multipolygon(self):
        resp_multipolygon = self.client.post('/validate',
                                             data=json.dumps(samples.multipolygon),
                                             content_type=JSON)
        self.assertEqual(json.loads(resp_multipolygon.content), GOOD_RESPONSE)

    def test_feature(self):
        resp_feature = self.client.post('/validate',
                                        data=json.dumps(samples.feature),
                                        content_type=JSON)
        self.assertEqual(json.loads(resp_feature.content), GOOD_RESPONSE)

    def test_featurecollection(self):
        resp_featurecollection = self.client.post('/validate',
                                                  data=json.dumps(samples.featurecollection),
                                                  content_type=JSON)
        self.assertEqual(json.loads(resp_featurecollection.content), GOOD_RESPONSE)

    def test_geometrycollection(self):
        resp_geometrycollection = self.client.post('/validate',
                                                   data=json.dumps(samples.geometrycollection),
                                                   content_type=JSON)
        self.assertEqual(json.loads(resp_geometrycollection.content), GOOD_RESPONSE)
