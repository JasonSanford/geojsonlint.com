import json
import requests

from django.http import HttpResponse
from django.shortcuts import render_to_response

from utils import validate_json, track_validate


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
        validate_json(raw_json)
    except TypeError as error:
        return HttpResponse(json.dumps(_geojson_error(str(error))), mimetype='application/json')

    # Everything checked out. Return 'ok'.
    track_validate()
    resp = {
        'status': 'ok',
    }
    return HttpResponse(json.dumps(resp), mimetype='application/json')


def _geojson_error(message):
    track_validate(valid=False)
    resp = {
        'status': 'error',
        'message': message,
    }
    return resp
