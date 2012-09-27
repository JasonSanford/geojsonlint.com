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
    resp = dict(
        status = 'ok',
    )
    return HttpResponse(json.dumps(resp), mimetype='application/json')