from werkzeug.datastructures import MultiDict

from src.forms.company import CompanyForm


class TestCompanyForm:
    def test_valid_form(self):
        data = {"name": "Apple"}

        form = CompanyForm(MultiDict(data))

        assert form.validate() is True

    def test_invalid_form(self):
        data = {"name": ""}

        form = CompanyForm(MultiDict(data))

        assert form.validate() is False
