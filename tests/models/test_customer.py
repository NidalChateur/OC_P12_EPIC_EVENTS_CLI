from src.models.customer import Customer, slugify, unfilled
from tests import MixinSetup


class TestCustomer(MixinSetup):
    def test_french_name(self):
        assert Customer.FRENCH_NAME == "client"

    def test_str(self):
        self.clear_db()
        qs = self.create_customer_qs()
        obj = qs[0]

        assert str(obj) == f"{obj.first_name.capitalize()} {obj.last_name.capitalize()}"

    def test_repr(self):
        obj = self.session.get(Customer, 1)

        assert str(obj) == repr(obj)

    def test_name(self):
        obj = self.session.get(Customer, 1)

        assert str(obj) == obj.name

    def test_formatted_phone(self):
        obj = self.session.get(Customer, 1)

        assert obj.formatted_phone == " ".join(
            [obj.phone[i: i + 2] for i in range(0, len(obj.phone), 2)]
        )

        obj.phone = ""
        assert obj.formatted_phone == unfilled

    def test_prompt_phone(self):
        self.clear_db()
        qs = self.create_customer_qs()
        obj = qs[0]

        assert obj.prompt_phone == obj.phone

        obj.phone = ""
        assert obj.prompt_phone == ""

    def test_slug_first_name(self):
        obj = self.session.get(Customer, 1)

        assert obj.slug_first_name == slugify(obj.first_name)

    def test_slug_last_name(self):
        obj = self.session.get(Customer, 1)

        assert obj.slug_last_name == slugify(obj.last_name)

    def test_slug_email(self):
        obj = self.session.get(Customer, 1)

        assert obj.slug_email == slugify(obj.email)

    def test_prompt_company_name(self):
        obj = self.session.get(Customer, 1)

        assert obj.prompt_company_name == str(obj.company)

        obj.company = None
        assert obj.prompt_company_name == ""

    def test_company_name(self):
        self.clear_db()
        qs = self.create_customer_qs()
        obj = qs[0]

        assert obj.company_name == str(obj.company)

        obj.company = None
        assert obj.company_name == unfilled

    def test_commercial_name(self):
        obj = self.session.get(Customer, 1)

        assert obj.commercial_name == obj.commercial.name

        obj.commercial = None
        assert obj.commercial_name == unfilled

    def test_slug_commercial_name(self):
        self.clear_db()
        qs = self.create_customer_qs()
        obj = qs[0]

        assert obj.slug_commercial_name == slugify(obj.commercial.name)

        obj.commercial = None
        assert obj.slug_commercial_name == ""

    def test_save(self):
        self.clear_db()
        qs = self.create_customer_qs()
        obj = qs[0]
        obj.save(self.session)

        slug_company = slugify(obj.prompt_company_name)
        slug_commercial = obj.slug_commercial_name
        slug = f"{obj.id}-{obj.slug_first_name}-{obj.slug_last_name}-{slug_company}-{slug_commercial}"

        assert obj.slug == slug
