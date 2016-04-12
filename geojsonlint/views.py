import json

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response

from utils import validate_geojson, get_remote_json
from exc import GeoJSONValidationException, NonFetchableURLException


def home(request):
    """
    GET /

    Show the home page
    """
    return render_to_response('index.html')


@require_http_methods(['GET', 'POST'])
def validate(request):
    """
    POST /validate

    Validate GeoJSON data in POST body
    """

    testing = request.GET.get('testing')

    if request.method == 'POST':
        stringy_json = request.raw_post_data
    else:  # GET
        try:
            remote_url = request.GET['url']
            stringy_json = get_remote_json(remote_url)
        except KeyError:  # The "url" URL parameter was missing
            return _geojson_error('When validating via GET, a "url" URL parameter is required.', status=400)
        except NonFetchableURLException:
            return _geojson_error('The URL passed could not be fetched.')

    try:
        test_geojson = json.loads(stringy_json)
        if not isinstance(test_geojson, dict):
            return _geojson_error('Data was not a JSON object.', testing)
    except:
        return _geojson_error('Data was not JSON serializeable.', testing)

    if not 'type' in test_geojson:
        return _geojson_error('The "type" member is required and was not found.', testing)

    try:
        validate_geojson(test_geojson)
    except GeoJSONValidationException as e:
        return _geojson_error(str(e), testing)

    # Everything checked out. Return 'ok'.
    resp = {
        'status': 'ok',
    }
    return HttpResponse(json.dumps(resp), mimetype='application/json')


def _geojson_error(message, testing=False, status=200):
    resp = {
        'status': 'error',
        'message': message,
    }
    return HttpResponse(json.dumps(resp), mimetype='application/json', status=status)
