# READ THIS

This code used to power https://geojsonlint.com - I let the domain registration expire but someone else picked it up and forked this code to keep it running. Any changes to this repo will not be reflected at https://geojsonlint.com, I'm not even sure who manages that domain.

<img src="https://api.travis-ci.org/JasonSanford/geojsonlint.com.png">

A simple Django app to validate your GeoJSON.

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
