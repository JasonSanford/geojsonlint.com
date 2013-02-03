import json

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render_to_response

import validictory

from schemas import point, multipoint, linestring, multilinestring, polygon, multipolygon, geometrycollection, feature, featurecollection


def home(request):
    """
    GET /

    Show the home page
    """
    return render_to_response('index.html')


@require_POST
def validate(request):
    """
    POST /validate

    Validate GeoJSON data in POST body
    """

    try:
        test_geojson = json.loads(request.raw_post_data)
        if not isinstance(test_geojson, dict):
            return _geojson_error('POSTed data was not a JSON object.')
    except:
        return _geojson_error('POSTed data was not JSON serializeable.')

    if not 'type' in test_geojson:
        return _geojson_error('The "type" member is requried and was not found.')

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
        return _geojson_error('"%s" is not a valid GeoJSON type.' % test_geojson['type'])

    try:
        validictory.validate(test_geojson, geojson_types[test_geojson['type']])
    except validictory.validator.ValidationError as error:
        return _geojson_error(str(error))

    # Everything checked out. Return 'ok'.
    resp = {
        'status': 'ok',
    }
    return HttpResponse(json.dumps(resp), mimetype='application/json')


def _geojson_error(message):
    resp = {
        'status': 'error',
        'message': message,
    }
    return HttpResponse(json.dumps(resp), mimetype='application/json')
