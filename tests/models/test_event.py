from src.models.contract_event import Event, slugify, unfilled
from tests import MixinSetup


class TestEvent(MixinSetup):
    def test_french_name(self):
        assert Event.FRENCH_NAME == "événement"

    def test_formatted_start_date(self):
        self.clear_db()
        qs = self.create_event_qs()
        event = qs[0]

        assert event.formatted_start_date == event.start_date.strftime(
            "%d/%m/%Y à %H:%M"
        )

    def test_prompt_start_date(self):
        event = self.session.get(Event, 1)

        assert event.prompt_start_date == event.start_date.strftime("%Y-%m-%d")

    def test_prompt_start_time(self):
        event = self.session.get(Event, 1)

        assert event.prompt_start_time == event.start_date.strftime("%H:%M")

    def test_formatted_end_date(self):
        event = self.session.get(Event, 1)

        assert event.formatted_end_date == event.end_date.strftime("%d/%m/%Y à %H:%M")

    def test_prompt_end_date(self):
        event = self.session.get(Event, 1)

        assert event.prompt_end_date == event.end_date.strftime("%Y-%m-%d")

    def test_prompt_end_time(self):
        event = self.session.get(Event, 1)

        assert event.prompt_end_time == event.end_date.strftime("%H:%M")

    def test_address(self):
        event = self.session.get(Event, 1)
        assert event.address == str(event.location)

        event.location = None
        assert event.address == unfilled

    def test_customer_name(self):
        event = self.session.get(Event, 1)
        assert event.customer_name == event.contract.customer_name

        event.contract = None
        assert event.customer_name == unfilled

    def test_customer_email(self):
        self.clear_db()
        qs = self.create_event_qs()
        event = qs[0]
        assert event.customer_email == event.contract.customer_email

        event.contract = None
        assert event.customer_email == unfilled

    def test_customer_phone(self):
        self.clear_db()
        qs = self.create_event_qs()
        event = qs[0]
        assert event.customer_phone == event.contract.customer_phone

        event.contract = None
        assert event.customer_phone == unfilled

    def test_commercial_name(self):
        self.clear_db()
        qs = self.create_event_qs()
        event = qs[0]
        assert event.commercial_name == event.contract.commercial_name

        event.contract = None
        assert event.commercial_name == unfilled

    def test_commercial_email(self):
        self.clear_db()
        qs = self.create_event_qs()
        event = qs[0]
        assert event.commercial_email == event.contract.commercial_email

        event.contract = None
        assert event.commercial_email == unfilled

    def test_commercial_phone(self):
        self.clear_db()
        qs = self.create_event_qs()
        event = qs[0]
        assert event.commercial_phone == event.contract.commercial_phone

        event.contract = None
        assert event.commercial_phone == unfilled

    def test_support_name(self):
        self.clear_db()
        qs = self.create_event_qs()
        event = qs[0]
        assert event.support_name == event.support.name

        event.support = None
        assert event.support_name == unfilled

    def test_support_email(self):
        self.clear_db()
        qs = self.create_event_qs()
        event = qs[0]
        assert event.support_email == event.support.email

        event.support = None
        assert event.support_email == unfilled

    def test_support_phone(self):
        self.clear_db()
        qs = self.create_event_qs()
        event = qs[0]
        assert event.support_phone == event.support.formatted_phone

        event.support = None
        assert event.support_phone == unfilled

    def test_save(self):
        self.clear_db()
        qs = self.create_event_qs()
        event = qs[0]
        event.save(self.session)

        # 1. building slug with event.contract is not None
        customer_name = slugify(event.customer_name)
        commercial_name = slugify(event.commercial_name)
        support_name = slugify(event.support_name)
        contract_id = event.contract.id

        slug = slugify(
            f"{event.id} {contract_id} {customer_name} {commercial_name} {support_name}"
        )

        assert event.slug == slug

        # 1. building slug with event.contract is None
        event.contract = None
        event.save(self.session)

        customer_name = slugify(event.customer_name)
        commercial_name = slugify(event.commercial_name)
        support_name = slugify(event.support_name)

        slug = slugify(f"{event.id} {customer_name} {commercial_name} {support_name}")
        assert event.slug == slug
