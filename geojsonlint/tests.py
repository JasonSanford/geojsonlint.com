import json
from urllib import urlencode

from django.utils import unittest
from django.test.client import Client

import sample_geojson as samples
from utils import validate_geojson
from exc import GeoJSONValidationException

GOOD_RESPONSE = {
    'status': 'ok'
}
JSON = 'application/json'
validate_url = '/validate'

#
# Functional Tests
#

class RequestTestCase(unittest.TestCase):
    def setUp(self):
        self.geojson_url = 'http://gitspatial.com/api/v1/JasonSanford/mecklenburg-gis-opendata/parks?lat=35.255&lon=-80.855&distance=1750'
        self.geojson_url_bad1 = 'http://www.lobsterscatsdogsotheranimals.com'
        self.geojson_url_bad2 = 'http://gitspatial.com/api/v1/JasonSanford/mecklenburg-gis-opendata/lobsters?lat=35.255&lon=-80.855&distance=1750'
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

        response = self.client.post(validate_url, data=json.dumps(bad_type),
                                    content_type=JSON)

        self.assertEqual(json.loads(response.content), bad_type_message)


class TestValidateGoodType(RequestTestCase):

    def test_good_type(self):
        response = self.client.post(validate_url,
                                    data=json.dumps(samples.point),
                                    content_type=JSON)

        self.assertEqual(json.loads(response.content), GOOD_RESPONSE)


class TestValidateBadPosition(RequestTestCase):

    def test_bad_position(self):
        response = self.client.post(validate_url,
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

        response = self.client.post(validate_url,
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

        response = self.client.post(validate_url,
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

        response = self.client.post(validate_url,
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

        response = self.client.post(validate_url,
                                    data=json.dumps(bad_geom),
                                    content_type=JSON)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['status'], 'error')

    def test_no_geom(self):
        no_geom = {
            "properties": {},
            "type": "Feature"
        }

        response = self.client.post(validate_url,
                                    data=json.dumps(no_geom),
                                    content_type=JSON)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['status'], 'error')
        self.assertEqual(response_json['message'], 'A Feature must have a "geometry" property.')

    def test_no_properties(self):
        no_props = {
            "geometry": None,
            "type": "Feature"
        }

        response = self.client.post(validate_url,
                                    data=json.dumps(no_props),
                                    content_type=JSON)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['status'], 'error')
        self.assertEqual(response_json['message'], 'A Feature must have a "properties" property.')

class TestFeatureCollectionBadFeatures(RequestTestCase):

    def test_is_not_list_or_tuple(self):
        bad_fc = {
            "type": "FeatureCollection",
            "features": 'lobster'
        }
        response = self.client.post(validate_url,
                                    data=json.dumps(bad_fc),
                                    content_type=JSON)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['status'], 'error')
        self.assertEqual(response_json['message'], 'A FeatureCollection\'s "features" property must be an array.')

    def test_no_features(self):
        bad_fc = {
            "type": "FeatureCollection",
        }
        response = self.client.post(validate_url,
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
        response = self.client.post(validate_url,
                                    data=json.dumps(bad_gc),
                                    content_type=JSON)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['status'], 'error')
        self.assertEqual(response_json['message'], 'A GeometryCollection\'s "geometries" property must be an array.')

    def test_no_geometries(self):
        bad_gc = {
            "type": "GeometryCollection",
        }
        response = self.client.post(validate_url,
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
            'message': 'Data was not JSON serializeable.'
        }

        response = self.client.post(validate_url, data=bad_json,
                                    content_type=JSON)

        self.assertEqual(json.loads(response.content), bad_json_message)


class TestValidateNoType(RequestTestCase):

    def test_bad_json(self):
        # Missing ending curly brace
        no_type_json = {
            'coordinates': [56, 79]
        }
        no_type_message = {
            'status': 'error',
            'message': 'The "type" member is required and was not found.'
        }

        response = self.client.post(validate_url, data=json.dumps(no_type_json),
                                    content_type=JSON)

        self.assertEqual(json.loads(response.content), no_type_message)


class TestValidateNotAnObject(RequestTestCase):

    def test_not_an_object(self):
        not_an_object = [1, 2, 3, 'cat', 'house']
        not_an_object_message = {
            'status': 'error',
            'message': 'Data was not a JSON object.'
        }

        response = self.client.post(validate_url,
                                    data=json.dumps(not_an_object),
                                    content_type=JSON)

        self.assertEqual(json.loads(response.content), not_an_object_message)


class TestValidateHTTPMethods(RequestTestCase):

    def test_post(self):
        post_response = self.client.post(validate_url,
                                         data=json.dumps(samples.point),
                                         content_type=JSON)
        self.assertEqual(post_response.status_code, 200)

    def test_get(self):
        encoded = urlencode({'url': self.geojson_url})
        get_response = self.client.get(validate_url + ('?%s' % encoded))
        self.assertEqual(get_response.status_code, 200)

    def test_put(self):
        put_response = self.client.put(validate_url,
                                       data=json.dumps(samples.point),
                                       content_type=JSON)
        self.assertEqual(put_response.status_code, 405)

    def test_delete(self):
        delete_response = self.client.delete(validate_url)
        self.assertEqual(delete_response.status_code, 405)


class TestValidateValidThings(RequestTestCase):

    def test_point(self):
        resp_point = self.client.post(validate_url,
                                      data=json.dumps(samples.point),
                                      content_type=JSON)
        self.assertEqual(json.loads(resp_point.content), GOOD_RESPONSE)

    def test_point_three(self):
        resp_point_three = self.client.post(validate_url,
                                            data=json.dumps(samples.point_three),
                                            content_type=JSON)
        self.assertEqual(json.loads(resp_point_three.content), GOOD_RESPONSE)

    def test_multipoint(self):
        resp_multipoint = self.client.post(validate_url,
                                           data=json.dumps(samples.multipoint),
                                           content_type=JSON)
        self.assertEqual(json.loads(resp_multipoint.content), GOOD_RESPONSE)

    def test_linestring(self):
        resp_linestring = self.client.post(validate_url,
                                           data=json.dumps(samples.linestring),
                                           content_type=JSON)
        self.assertEqual(json.loads(resp_linestring.content), GOOD_RESPONSE)

    def test_multilinestring(self):
        resp_multilinestring = self.client.post(validate_url,
                                                data=json.dumps(samples.multilinestring),
                                                content_type=JSON)
        self.assertEqual(json.loads(resp_multilinestring.content), GOOD_RESPONSE)

    def test_polygon(self):
        resp_polygon = self.client.post(validate_url,
                                        data=json.dumps(samples.polygon),
                                        content_type=JSON)
        self.assertEqual(json.loads(resp_polygon.content), GOOD_RESPONSE)

    def test_multipolygon(self):
        resp_multipolygon = self.client.post(validate_url,
                                             data=json.dumps(samples.multipolygon),
                                             content_type=JSON)
        self.assertEqual(json.loads(resp_multipolygon.content), GOOD_RESPONSE)

    def test_feature(self):
        resp_feature = self.client.post(validate_url,
                                        data=json.dumps(samples.feature),
                                        content_type=JSON)
        self.assertEqual(json.loads(resp_feature.content), GOOD_RESPONSE)

    def test_featurecollection(self):
        resp_featurecollection = self.client.post(validate_url,
                                                  data=json.dumps(samples.featurecollection),
                                                  content_type=JSON)
        self.assertEqual(json.loads(resp_featurecollection.content), GOOD_RESPONSE)

    def test_geometrycollection(self):
        resp_geometrycollection = self.client.post(validate_url,
                                                   data=json.dumps(samples.geometrycollection),
                                                   content_type=JSON)
        self.assertEqual(json.loads(resp_geometrycollection.content), GOOD_RESPONSE)

class TestURLParameters(RequestTestCase):

    def test_url(self):
        encoded = urlencode({'url': self.geojson_url})
        resp = self.client.get(validate_url + ('?%s' % encoded))
        json_content = json.loads(resp.content)
        expected = {'status': 'ok'}
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json_content, expected)

    def test_bad_url_parameter(self):
        encoded = urlencode({'urlzzz': self.geojson_url})
        resp = self.client.get(validate_url + ('?%s' % encoded))
        json_content = json.loads(resp.content)
        expected = {'status': 'error', 'message': 'When validating via GET, a "url" URL parameter is required.'}
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(json_content, expected)

    def test_could_not_be_fetched_no_domain(self):
        # This domain cannot even be reached
        encoded = urlencode({'url': self.geojson_url_bad1})
        resp = self.client.get(validate_url + ('?%s' % encoded))
        json_content = json.loads(resp.content)
        expected = {'status': 'error', 'message': 'The URL passed could not be fetched.'}
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json_content, expected)

    def test_could_not_be_fetched(self):
        # A valid domain, but should get a 404 for the requested URL
        encoded = urlencode({'url': self.geojson_url_bad2})
        resp = self.client.get(validate_url + ('?%s' % encoded))
        json_content = json.loads(resp.content)
        expected = {'status': 'error', 'message': 'The URL passed could not be fetched.'}
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json_content, expected)
#
# Unit Tests
#
class UnitTestValidGeoJSON(unittest.TestCase):
    s = samples
    valids = [
        s.point,
        s.point_three,
        s.multipoint,
        s.linestring,
        s.multilinestring,
        s.polygon,
        s.multipolygon,
        s.feature,
        s.featurecollection,
        s.geometrycollection,
    ]
    for valid in valids:
        # A GeoJSONValidationException will be raised if something is invalid, so just looping is fine.
        validate_geojson(valid)


class UnitTestInvalidGeoJSON(unittest.TestCase):
    def test_invalid_geojson(self):
        s = samples
        invalids = [
            s.point_with_strings,
            s.featurecollection_bad_geom,
            s.bad_type,
        ]
        valids = 0
        for invalid in invalids:
            try:
                validate_geojson(invalid)
                valids += 1
            except GeoJSONValidationException:
                pass
        self.assertEqual(valids, 0)