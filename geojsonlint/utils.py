from pyga.requests import Tracker
from pyga.entities import Event, Session, Visitor
import validictory

from .exc import GeoJSONValidationException
from .schemas import point, multipoint, linestring, multilinestring, polygon, multipolygon, geometrycollection, feature, featurecollection


def track_validate(valid=True):
    value = 1 if valid else 0
    tracker = Tracker(account_id='UA-7385360-18', domain_name='geojsonlint.com')
    event = Event(category='server', action='validate', value=value)
    session = Session()
    visitor = Visitor()
    tracker.track_event(event, session, visitor)


def validate_geojson(test_geojson):
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
        raise GeoJSONValidationException('"%s" is not a valid GeoJSON type.' % test_geojson['type'])

    if test_geojson['type'] in ('Feature', 'FeatureCollection', 'GeometryCollection'):
        #
        # These are special cases that every JSON schema library
        # I've tried doesn't seem to handle properly.
        #
        _validate_special_case(test_geojson)
    else:
        try:
            validictory.validate(test_geojson, geojson_types[test_geojson['type']])
        except validictory.validator.ValidationError as error:
            raise GeoJSONValidationException(str(error))

    return

def _validate_special_case(test_geojson):

    def _validate_feature_ish_thing(test_geojson):
        if 'geometry' not in test_geojson:
            raise GeoJSONValidationException('A Feature must have a "geometry" property.')
        if 'properties' not in test_geojson:
            raise GeoJSONValidationException('A Feature must have a "properties" property.')
        if test_geojson['geometry'] is not None:
            validate_geojson(test_geojson['geometry'])

    if test_geojson['type'] == 'Feature':
        _validate_feature_ish_thing(test_geojson)
    elif test_geojson['type'] == 'FeatureCollection':
        if 'features' not in test_geojson:
            raise GeoJSONValidationException('A FeatureCollection must have a "features" property.')
        elif not isinstance(test_geojson['features'], (list, tuple,)):
            raise GeoJSONValidationException('A FeatureCollection\'s "features" property must be an array.')
        for feature in test_geojson['features']:
            _validate_feature_ish_thing(feature)
    elif test_geojson['type'] == 'GeometryCollection':
        if 'geometries' not in test_geojson:
            raise GeoJSONValidationException('A GeometryCollection must have a "geometries" property.')
        elif not isinstance(test_geojson['geometries'], (list, tuple,)):
            raise GeoJSONValidationException('A GeometryCollection\'s "geometries" property must be an array.')
        for geometry in test_geojson['geometries']:
            if geometry is not None:
                validate_geojson(geometry)
