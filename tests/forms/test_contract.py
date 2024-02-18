from werkzeug.datastructures import MultiDict

from src.forms.contract import ContractForm


class TestContractForm:
    def test_valid_form(self):
        data = {"total_amount": "150", "paid_amount": "100", "is_signed": False}

        form = ContractForm(MultiDict(data))

        assert form.validate() is True

    def test_invalid_form(self):
        # paid_amount > total_amount
        data = {"total_amount": "50", "paid_amount": "100", "is_signed": False}

        form = ContractForm(MultiDict(data))

        assert form.validate() is False

        # total_amount is not integer
        data = {"total_amount": "gfdsfvfdvdf", "paid_amount": "100", "is_signed": False}

        form = ContractForm(MultiDict(data))

        assert form.validate() is False
