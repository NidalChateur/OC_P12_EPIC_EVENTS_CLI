from src.models.contract_event import Contract, Fernet, no, slugify, unfilled, yes
from tests import MixinSetup


class TestContract(MixinSetup):
    def test_french_name(self):
        assert Contract.FRENCH_NAME == "contrat"

    def test_prompt_is_signed(self):
        self.clear_db()
        qs = self.create_contract_qs()
        contract = qs[0]

        assert contract.prompt_is_signed == "oui"

        contract.is_signed = False

        assert contract.prompt_is_signed == "non"

    def test_formatted_is_signed(self):
        self.clear_db()
        qs = self.create_contract_qs()
        contract = qs[0]

        assert contract.formatted_is_signed == yes

        contract.is_signed = False

        assert contract.formatted_is_signed == no

    def test_is_paid(self):
        self.clear_db()
        qs = self.create_contract_qs()
        contract = qs[0]

        assert isinstance(contract.is_paid, bool)
        assert contract.is_paid is False

    def test_formatted_is_paid(self):
        self.clear_db()
        qs = self.create_contract_qs()
        contract = qs[0]

        assert contract.formatted_is_paid == no

        contract.paid_amount = contract.total_amount

        assert contract.formatted_is_paid == yes

    def test_remaining_amount(self):
        self.clear_db()
        qs = self.create_contract_qs()
        contract = qs[0]

        assert contract.remaining_amount == contract.total_amount - contract.paid_amount

    def test_formatted_paid_amount(self):
        self.clear_db()
        qs = self.create_contract_qs()
        contract = qs[0]

        formatted_paid_amount = "{:,}".format(contract.paid_amount).replace(",", " ")

        assert contract.formatted_paid_amount == formatted_paid_amount

    def test_formatted_total_amount(self):
        self.clear_db()
        qs = self.create_contract_qs()
        contract = qs[0]

        formatted_total_amount = "{:,}".format(contract.total_amount).replace(",", " ")

        assert contract.formatted_total_amount == formatted_total_amount

    def test_formatted_remaining_amount(self):
        self.clear_db()
        qs = self.create_contract_qs()
        contract = qs[0]

        formatted_remaining_amount = "{:,}".format(contract.remaining_amount).replace(
            ",", " "
        )

        assert contract.formatted_remaining_amount == formatted_remaining_amount

    def test_customer_name(self):
        self.clear_db()
        qs = self.create_contract_qs()
        contract = qs[0]

        assert contract.customer_name == contract.customer.name

        contract.customer = None
        assert contract.customer_name == unfilled

    def test_customer_email(self):
        self.clear_db()
        qs = self.create_contract_qs()
        contract = qs[0]

        assert contract.customer_email == contract.customer.email

        contract.customer = None
        assert contract.customer_email == unfilled

    def test_customer_phone(self):
        self.clear_db()
        qs = self.create_contract_qs()
        contract = qs[0]

        assert contract.customer_phone == contract.customer.formatted_phone

        contract.customer = None
        assert contract.customer_phone == unfilled

    def test_commercial_name(self):
        self.clear_db()
        qs = self.create_contract_qs()
        contract = qs[0]

        assert contract.commercial_name == contract.customer.commercial_name

        contract.customer.commercial = None
        assert contract.commercial_name == unfilled

    def test_commercial_email(self):
        self.clear_db()
        qs = self.create_contract_qs()
        contract = qs[0]

        assert contract.commercial_email == Fernet.decrypt(
            contract.customer.commercial.email
        )

        contract.customer.commercial = None
        assert contract.commercial_email == unfilled

    def test_commercial_phone(self):
        self.clear_db()
        qs = self.create_contract_qs()
        contract = qs[0]

        assert contract.commercial_phone == contract.customer.commercial.formatted_phone

        contract.customer.commercial = None
        assert contract.commercial_phone == unfilled

    def test_is_ready_for_event(self):
        self.clear_db()
        qs = self.create_contract_qs()
        contract = qs[0]

        assert contract.is_ready_for_event(self.session) is True

        contract.is_signed = False

        assert contract.is_ready_for_event(self.session) is False

    def test_save(self):
        self.clear_db()
        qs = self.create_contract_qs()
        contract: Contract = qs[0]
        contract.save(self.session)

        slug = f"{contract.customer_name} {contract.commercial_name} {contract.total_amount}"
        assert contract.slug == slugify(f"{contract.id} {slug}")

        contract.customer = None
        contract.save(self.session)

        assert contract.slug == slugify(f"{contract.id} {contract.total_amount}")
