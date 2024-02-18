from werkzeug.datastructures import MultiDict

from src.forms.location import LocationForm, slugify


class TestLocationForm:
    def test_valid_forms(self):
        data = {
            "name": "Tour Eiffel",
            "number": "5",
            "street_type": "avenue",
            "street_name": "Anatole France",
            "zip_code": "75000",
            "city": "Paris",
        }

        form = LocationForm(MultiDict(data))

        assert form.validate() is True

        name = form.name.data
        number = form.number.data
        street_type = form.street_type.data
        street_name = form.street_name.data
        zip_code = form.zip_code.data
        city = form.city.data
        slug_form = slugify(
            f"{name} {number} {street_type} {street_name} {zip_code} {city}"
        )

        assert form.slug_form.data == slug_form

        # 2. test the smallest valid form
        data = {
            "zip_code": "75000",
            "city": "Paris",
        }

        form = LocationForm(MultiDict(data))

        assert form.validate() is True
        assert form.slug_form.data == slugify(f"{zip_code} {city}")

    def test_invalid_forms(self):
        # zip_code is not digit
        data = {
            "zip_code": "wrong",
            "city": "Paris",
        }

        form = LocationForm(MultiDict(data))

        assert form.validate() is False
        
        # zip_code is too long
        data = {
            "zip_code": "88888888",
            "city": "Paris",
        }

        form = LocationForm(MultiDict(data))
        assert form.validate() is False
