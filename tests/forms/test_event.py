from werkzeug.datastructures import MultiDict

from src.forms.event import EventForm


class TestEventForm:
    def test_valid_form(self):
        data = {
            "start_date": "2024-01-01",
            "start_time": "00:00",
            "end_date": "2024-01-01",
            "end_time": "23:59",
            "attendees": "50",
            "note": "new year",
        }

        form = EventForm(MultiDict(data))

        assert form.validate() is True

    def test_invalid_form(self):
        # start_date > end_date
        data = {
            "start_date": "2024-01-01",
            "start_time": "00:00",
            "end_date": "2022-01-01",
            "end_time": "23:59",
            "attendees": "50",
            "note": "new year",
        }

        form = EventForm(MultiDict(data))

        assert form.validate() is False

        # empty attendees
        data = {
            "start_date": "2024-01-01",
            "start_time": "00:00",
            "end_date": "2024-01-01",
            "end_time": "23:59",
            "attendees": "",
            "note": "new year",
        }

        form = EventForm(MultiDict(data))

        assert form.validate() is False
