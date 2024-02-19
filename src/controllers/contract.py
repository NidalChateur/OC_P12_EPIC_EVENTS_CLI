# pylint: disable=no-member

from ..models.contract_event import Contract
from ..models.customer import Customer
from ..utils.session import session_is_expired
from ..utils.slugify import slugify
from ..views.contract import View

model1 = Contract
model2 = Customer


class Controller:
    @classmethod
    def run(self, session, user):
        self._menu(session, user)

    @classmethod
    def return_to_menu(self, session, user):
        self._menu(session, user)

    @classmethod
    def _menu(self, session, user) -> bool:
        if session_is_expired(user):
            View.logout()

            return None

        if user.role == "Gestion":
            View.print_gestion_menu()

        if user.role == "Commercial":
            View.print_commercial_menu()

        if user.role == "Support":
            View.print_menu()

        choice = View.get_user_choice()

        if choice == 0:
            back_to_home_menu = True

            return back_to_home_menu

        if choice == 1:
            self._list(session)

        if choice == 2:
            self._search(session)

        if choice == 3:
            self._detail(session)

        if choice == 4 and user.role in ["Gestion", "Commercial"]:
            self._unsigned_contracts(session)

        if choice == 5 and user.role in ["Gestion", "Commercial"]:
            self._unpaid_contracts(session)

        if choice == 6 and user.role in ["Gestion", "Commercial"]:
            self._update(session, user)

        if choice == 7 and user.role == "Gestion":
            self._create(session)

        if choice == 8 and user.role == "Gestion":
            self._delete(session)

        self.return_to_menu(session, user)

    @classmethod
    def _list(self, session):
        qs = session.query(Contract).order_by(Contract.edition_time.desc()).all()

        list_name = f"Tous les {View.name}s"
        View.print_list(qs, list_name)

    @classmethod
    def _search(self, session):
        search = View.get_searched_value()

        qs = (
            session.query(Contract)
            .filter(Contract.slug.like(f"%{slugify(search)}%"))
            .order_by(Contract.edition_time.desc())
            .all()
        )

        list_name = f"Résultat recherche {View.name}"
        View.print_list(qs, list_name)

    @classmethod
    def _detail(self, session):
        obj_id = View.get_id(View.name)
        if obj_id != 0:
            obj = session.get(Contract, obj_id)
            View.print_detail(obj)

    @classmethod
    def _unsigned_contracts(self, session):
        qs = (
            session.query(Contract)
            .filter(Contract.is_signed == 0)
            .order_by(Contract.edition_time.desc())
            .all()
        )
        list_name = f"Tous les {View.name}s non signés"
        View.print_list(qs, list_name)

    @classmethod
    def _unpaid_contracts(self, session):
        qs = (
            session.query(Contract)
            .filter(Contract.paid_amount < Contract.total_amount)
            .order_by(Contract.edition_time.desc())
            .all()
        )
        list_name = f"Tous les {View.name}s non payés"
        View.print_list(qs, list_name)

    @classmethod
    def _get_customer(self, session) -> Customer:
        customer_id = View.get_id(Customer.FRENCH_NAME)
        if customer_id == 0:
            return None

        obj = session.get(Customer, customer_id)

        if obj:
            return obj

        else:
            View.print_permission_denied()

    @classmethod
    def _create_contract(self, session, customer: Customer):
        form = View.get_contract_data_to_create()

        if form.validate():
            contract = Contract(
                total_amount=form.total_amount.data,
                paid_amount=form.paid_amount.data,
                is_signed=form.is_signed.data,
                customer=customer,
            )
            contract.create(session)
            contract.save(session)

            View.print_create_success(contract)
            View.print_signature_success(session, contract)

        else:
            View.print_forms_errors(form)

    @classmethod
    def _create(self, session):
        customer = self._get_customer(session)
        response = False

        if customer:
            response = View.print_create_confirm(customer)

        if response is True:
            self._create_contract(session, customer)

    @classmethod
    def _update(self, session, user):
        """only possible for the customer commercial or the gestion"""

        obj_id = View.get_id(View.name)

        if obj_id == 0:
            return None

        obj = session.get(Contract, obj_id)

        if not obj:
            View.print_permission_denied()

            return None

        if user.role == "Commercial" and obj.customer.commercial != user:
            View.print_permission_denied()

            return None

        View.print_detail(obj)

        form = View.get_contract_data_to_update(obj)
        if form.validate():
            obj.total_amount = form.total_amount.data
            obj.paid_amount = form.paid_amount.data
            obj.is_signed = form.is_signed.data
            obj.save(session)

            View.print_update_success(obj)
            View.print_signature_success(session, obj)

        else:
            View.print_forms_errors(form)

    @classmethod
    def _delete(self, session):
        obj_id = View.get_id(View.name)

        if obj_id == 0:
            return None

        obj = session.get(Contract, obj_id)
        if not obj:
            View.print_permission_denied()

            return None

        View.print_detail(obj)
        choice = View.print_delete_confirm(obj)
        if choice == "o":
            obj.delete(session)
            View.print_delete_success(obj_id)
