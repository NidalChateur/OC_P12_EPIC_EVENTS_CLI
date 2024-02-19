from datetime import date, datetime

from src.models.collaborator import Collaborator
from src.models.company import Company
from src.models.contract_event import Contract, Event
from src.models.customer import Customer
from src.models.department import Department
from src.models.location import Location
from src.settings.settings import init_test_db
from src.utils.fernet import Fernet


class MixinSetup:
    CLEAR_EMAIL = "john@gmail.com"
    CLEAR_PASSWORD = "00000000pW-"

    session = init_test_db()

    def clear_db(self):
        models = [
            Department,
            Collaborator,
            Company,
            Customer,
            Contract,
            Location,
            Event,
        ]
        for model in models:
            self.session.query(model).delete()

    def mock_prompt_ask(self, *args, **kwargs) -> str:
        return "user_entry"

    def mock_permission_denied(self, *args, **kwargs):
        """used to mock forbidden access in controllers during tests"""

        raise PermissionError("access denied")

    def create_department(self, department_name: str) -> Department:
        department = Department(name=department_name)
        department.create(self.session)

        return department

    def create_collaborator(self, department_name: str) -> Collaborator:
        collaborator = Collaborator(
            first_name="John",
            last_name="Doe",
            email=Fernet.encrypt(self.CLEAR_EMAIL),
            birthdate=date(2000, 1, 1),
            phone="0102030405",
            department=self.create_department(department_name),
        )
        collaborator.create(self.session)

        return collaborator

    def create_contract(self) -> Contract:
        contract = Contract(total_amount=100, paid_amount=100, is_signed=True)
        contract.create(self.session)

        return contract

    def create_customer_qs(self) -> list[Customer]:
        commercial = self.create_collaborator(department_name="Commercial")

        company = Company(name="company")
        company.create(self.session)

        for i in range(6):
            customer = Customer(
                first_name=f"John{i}",
                last_name="Doe",
                email=f"john{i}@gmail.com",
                phone="0102030405",
                company=company,
                commercial=commercial,
            )
            customer.create(self.session)

        return self.session.query(Customer).all()

    def create_collaborator_qs(self) -> list[Collaborator]:
        department = self.create_department("Commercial")

        for i in range(6):
            obj = Collaborator(
                first_name=f"John{i}",
                last_name="Doe",
                email=Fernet.encrypt(f"john{i}@gmail.com"),
                birthdate=date(2000, 1, 1),
                department=department,
            )
            obj.create(self.session)

        return self.session.query(Collaborator).all()

    def create_contract_qs(self) -> list[Contract]:
        self.create_customer_qs()
        customer = self.session.get(Customer, 1)
        for i in range(6):
            contract = Contract(
                customer=customer,
                total_amount=5,
                paid_amount=i,
                is_signed=True,
            )
            contract.create(self.session)

        return self.session.query(Contract).all()

    def create_location(self) -> Location:
        location = Location(zip_code="75000", city="Paris")
        location.create(self.session)

        return location

    def create_event_qs(self) -> list[Event]:
        self.create_contract_qs()
        location = self.create_location()
        support = self.create_collaborator(department_name="Support")

        for i in range(6):
            event = Event(
                location=location,
                contract=self.session.get(Contract, i + 1),
                support=support,
                start_date=datetime(2000, 1, 1, 0, 0),
                end_date=datetime(2000, 1, 1, 23, 59),
                attendees=50,
                note="important moment",
            )
            event.create(self.session)

        return self.session.query(Event).all()
