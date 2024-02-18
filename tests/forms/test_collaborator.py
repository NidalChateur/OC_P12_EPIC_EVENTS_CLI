from werkzeug.datastructures import MultiDict

from src.forms.collaborator import CollaboratorForm, PasswordForm


class TestPasswordForm:
    def test_valid_form(self):
        data = {
            "password": "00000000pW-",
            "password_confirm": "00000000pW-",
        }

        form = PasswordForm(MultiDict(data))

        assert form.validate() is True

    def test_invalid_forms(self):
        # too short
        data1 = {
            "password": "John",
            "password_confirm": "John",
        }

        # no letter
        data2 = {
            "password": "12345678910",
            "password_confirm": "12345678910",
        }

        # no number
        data3 = {
            "password": "adsdfvdfbfdgb",
            "password_confirm": "adsdfvdfbfdgb",
        }

        # no upper
        data4 = {
            "password": "adsdfvdfbfdgb12",
            "password_confirm": "adsdfvdfbfdgb12",
        }

        # no lower
        data5 = {
            "password": "AAAAAAAAAAAAAAAA12",
            "password_confirm": "AAAAAAAAAAAAAAAA12",
        }

        # no special character
        data6 = {
            "password": "AAAAAAAAAAAAAAAAgttgt12",
            "password_confirm": "AAAAAAAAAAAAAAAAgttgt12",
        }

        assert PasswordForm(MultiDict(data1)).validate() is False
        assert PasswordForm(MultiDict(data2)).validate() is False
        assert PasswordForm(MultiDict(data3)).validate() is False
        assert PasswordForm(MultiDict(data4)).validate() is False
        assert PasswordForm(MultiDict(data5)).validate() is False
        assert PasswordForm(MultiDict(data6)).validate() is False


class TestCollaboratorForm:
    def test_minor_invalid_birthdate(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@gmail.com",
            "phone": "0102030405",
            "birthdate": "2024-01-01",
        }

        form = CollaboratorForm(MultiDict(data))

        assert form.validate() is False
