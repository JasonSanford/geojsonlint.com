import json

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render_to_response

from utils import track_validate, validate_geojson
from exc import GeoJSONValidationException


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

    testing = request.GET.get('testing')

    try:
        test_geojson = json.loads(request.raw_post_data)
        if not isinstance(test_geojson, dict):
            return _geojson_error('POSTed data was not a JSON object.', testing)
    except:
        return _geojson_error('POSTed data was not JSON serializeable.', testing)

    if not 'type' in test_geojson:
        return _geojson_error('The "type" member is requried and was not found.', testing)

    try:
        validate_geojson(test_geojson)
    except GeoJSONValidationException as e:
        return _geojson_error(str(e), testing)

    # Everything checked out. Return 'ok'.
    if not testing:
        track_validate()
    resp = {
        'status': 'ok',
    }
    return HttpResponse(json.dumps(resp), mimetype='application/json')


def _geojson_error(message, testing=False):
    if not testing:
        track_validate(valid=False)
    resp = {
        'status': 'error',
        'message': message,
    }
    return HttpResponse(json.dumps(resp), mimetype='application/json')
