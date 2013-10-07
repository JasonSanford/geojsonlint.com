from pyga.requests import Tracker
from pyga.entities import Event, Session, Visitor

import json
from schemas import point, multipoint, linestring, multilinestring, polygon, multipolygon, geometrycollection, feature, featurecollection
import validictory

def track_validate(valid=True):
    value = 1 if valid else 0
    tracker = Tracker(account_id='UA-7385360-18', domain_name='geojsonlint.com')
    event = Event(category='server', action='validate', value=value)
    session = Session()
    visitor = Visitor()
    tracker.track_event(event, session, visitor)


def validate_json(raw_json):
    try:
        test_geojson = json.loads(raw_json)
        if not isinstance(test_geojson, dict):
            raise TypeError('Not a JSON object.')
    except:
        raise TypeError('Not a JSON object.')

    if not 'type' in test_geojson:
        raise TypeError('Not a valid GEOJSON object (missing type attribute).')

    geojson_types = {
        'Point': point,
        'MultiPoint': multipoint,
        'LineString': linestring,
        'MultiLineString': multilinestring,
        'Polygon': polygon,
        'MultiPolygon': multipolygon,
        'GeometryCollection': geometrycollection,
        'Feature': feature,
        'FeatureCollection': featurecollection,
    }

    if not test_geojson['type'] in geojson_types:
        raise TypeError('"%s" is not a valid GeoJSON type.' % test_geojson['type'])

    try:
        validictory.validate(test_geojson, geojson_types[test_geojson['type']])
    except validictory.validator.ValidationError as error:
        raise TypeError(str(error))