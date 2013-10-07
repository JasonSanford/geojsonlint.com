import json
import requests

from django.http import HttpResponse
from django.shortcuts import render_to_response

from utils import track_validate, validate_geojson
from exc import GeoJSONValidationException


def home(request):
    """
    GET /

    Show the home page
    """
    return render_to_response('index.html')


def validate(request):
    """
    POST /validate

    Validate GeoJSON data in POST body
    """

    testing = request.GET.get('testing')
    if request.method == 'POST':
        raw_json = request.raw_post_data
    elif request.method == 'GET':
        if "" != request.GET.get('u'):
            try:
                r = requests.get(request.GET.get('u'))
                raw_json = r.text
            except Exception as e:
                return HttpResponse(json.dumps(_geojson_error(str(e))), mimetype='application/json')

    try:
        test_geojson = json.loads(raw_json)
        if not isinstance(test_geojson, dict):
            return HttpResponse(json.dumps(_geojson_error('Not a valid JSON object.', testing)), mimetype='application/json')
    except:
        return HttpResponse(json.dumps(_geojson_error('JSON not serializeable.', testing)), mimetype='application/json')

    if not 'type' in test_geojson:
        return HttpResponse(json.dumps(_geojson_error('The "type" member is requried and was not found.', testing)), mimetype='application/json')

    try:
        validate_geojson(test_geojson)
    except GeoJSONValidationException as e:
        return HttpResponse(json.dumps(_geojson_error(str(e))), mimetype='application/json')

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
    return resp
