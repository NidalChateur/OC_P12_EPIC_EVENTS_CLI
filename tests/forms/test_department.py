from werkzeug.datastructures import MultiDict

from src.forms.department import DepartmentForm


class TestDepartmentForm:
    def test_valid_form(self):
        data = {"name": "Gestion"}

        form = DepartmentForm(MultiDict(data))

        assert form.validate() is True

    def test_invalid_form(self):
        # wrong department name
        data = {"name": "Unknown Department"}

        form = DepartmentForm(MultiDict(data))

        assert form.validate() is False
