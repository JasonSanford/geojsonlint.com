import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response

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
    if not request.method == 'POST':
        resp = dict(
            status = 'error',
            message = 'GeoJSON data must be POSTed',
        )
        return HttpResponseBadRequest(json.dumps(resp), mimetype='application/json')
    try:
        test_geojson = json.loads(request.raw_post_data)
    except json.JSONDecodeError as e:
        return _geojson_error('POSTed data was not JSON parseable.')
    # Everything checked out. Return 'ok'.
    resp = dict(
        status = 'ok',
    )
    return HttpResponse(json.dumps(resp), mimetype='application/json')

def _geojson_error(message):
    resp = dict(
        status = 'error',
        message = message,
    )
    return HttpResponse(resp, mimetype='application/json')