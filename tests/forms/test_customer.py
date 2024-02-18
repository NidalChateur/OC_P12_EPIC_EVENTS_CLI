from werkzeug.datastructures import MultiDict

from src.forms.customer import CustomerForm


class TestCustomerForm:
    def test_valid_form(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@gmail.com",
            "phone": "0102030405",
        }

        form = CustomerForm(MultiDict(data))

        assert form.validate() is True

    def test_invalid_forms(self):
        # phone does not start with 0
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@gmail.com",
            "phone": "10203040500",
        }

        form = CustomerForm(MultiDict(data))

        assert form.validate() is False

        # phone is not digit
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@gmail.com",
            "phone": "gfghfhghfgfgddfg",
        }

        form = CustomerForm(MultiDict(data))

        assert form.validate() is False

        # phone is too short
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@gmail.com",
            "phone": "099",
        }

        form = CustomerForm(MultiDict(data))

        assert form.validate() is False
