from pyga.requests import Tracker
from pyga.entities import Event, Session, Visitor


def track_validate(valid=True):
    value = 1 if valid else 0
    tracker = Tracker(account_id='UA-7385360-18', domain_name='geojsonlint.com')
    event = Event(category='server', action='validate', value=value)
    session = Session()
    visitor = Visitor()
    tracker.track_event(event, session, visitor)
