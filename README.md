# geojsonlint.com

<img src="https://api.travis-ci.org/JasonSanford/geojsonlint.com.png">

A simple Django app to validate your GeoJSON. This app is available at http://geojsonlint.com but can run locally with minimal effort.

More info at http://geojason.info/2012/geojson-validation-via-geojsonlint.com/

## Getting Started

1. Clone the repo and cd into it
2. Create a python virtual environment `virtualenv venv --distribute`
3. Source to the virtual environment `source venv/bin/activate`
4. Install requirements `pip install -r requirements.txt`
5. Run the server `python manage.py runserver`
6. Enjoy http://localhost:8000

## Tests

Since this is a simple web app with no database requirements, a custom test runner is defined in settings (`TEST_RUNNER = 'testrunner.NoDbTestRunner'`) so there are no database setup or teardown.

1. Source to the virtual environment `source venv/bin/activate`
2. python manage.py test geojsonlint
