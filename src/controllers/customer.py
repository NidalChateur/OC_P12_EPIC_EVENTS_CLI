# pylint: disable=no-member
from ..models.company import Company
from ..models.customer import Customer
from ..utils.slugify import slugify
from ..views.customer import View


class Controller:
    @classmethod
    def run(self, session, user):
        self._menu(session, user)

    @classmethod
    def _menu(self, session, user) -> bool:
        if user.role == "Commercial":
            View.print_commercial_menu()
        else:
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

        if choice == 4 and user.role == "Commercial":
            self._create(session, user)

        if choice == 5 and user.role == "Commercial":
            self._update(session, user)

        if choice == 6 and user.role == "Commercial":
            self._delete(session, user)

        self._menu(session, user)

    @classmethod
    def _list(self, session):
        qs = session.query(Customer).order_by(Customer.edition_time.desc()).all()
        list_name = f"Tous les {View.name}s"
        View.print_list(qs, list_name)

    @classmethod
    def _search(self, session):
        search = View.get_searched_value()

        qs = (
            session.query(Customer)
            .filter(Customer.slug.like(f"%{slugify(search)}%"))
            .order_by(Customer.edition_time.desc())
            .all()
        )

        list_name = f"Résultat recherche {View.name}"
        View.print_list(qs, list_name)

    @classmethod
    def _detail(self, session):
        obj_id = View.get_id(View.name)
        if obj_id != 0:
            obj = session.get(Customer, obj_id)
            View.print_detail(obj)

    @classmethod
    def _email_is_unique(self, session, form) -> bool:
        email = form.email.data
        obj = session.query(Customer).filter_by(email=email).first()
        if obj:
            View.print_email_is_not_unique()

            return False

        return True

    @classmethod
    def _create_customer(self, session, user, form) -> Customer:
        if self._email_is_unique(session, form):
            customer = Customer(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                phone=form.phone.data,
                commercial=user,
            )
            customer.create(session)
            customer.save(session)

            return customer

    @classmethod
    def _save_company(self, session, customer, form) -> Customer:
        """get or create the company then save customer.company"""

        # check if the company exists
        slug_name = slugify(form.name.data)
        obj = session.query(Company).filter_by(slug_name=slug_name).first()

        if customer and obj:
            # get the existant company
            customer.company = obj
            customer.save(session)

            return customer

        if customer and not obj:
            # create company
            company = Company(name=form.name.data)
            company.create(session)
            company.save(session)

            customer.company = company
            customer.save(session)

            return customer

    @classmethod
    def _create(self, session, user):
        form1 = View.get_customer_data_to_create()
        form2 = View.get_company_data_to_create()

        if all([form1.validate(), form2.validate()]):
            customer = self._create_customer(session, user, form1)
            customer = self._save_company(session, customer, form2)
            View.print_create_success(customer)

        else:
            View.print_forms_errors(form1, form2)

    @classmethod
    def _update_customer(self, session, obj, form, email_is_unchanged):
        if email_is_unchanged or self._email_is_unique(session, form):
            obj.first_name = form.first_name.data
            obj.last_name = form.last_name.data
            obj.email = form.email.data
            obj.phone = form.phone.data

            obj.save(session)

            return obj

    @classmethod
    def _update(self, session, user):
        obj_id = View.get_id(View.name)
        if obj_id == 0:
            return None

        obj = session.get(Customer, obj_id)
        if not obj or obj.commercial != user:
            View.print_permission_denied()

            return None

        View.print_detail(obj)

        form1, email_is_unchanged = View.get_customer_data_to_update(obj)
        form2 = View.get_company_data_to_update(obj)
        if all([form1.validate(), form2.validate()]):
            obj = self._update_customer(session, obj, form1, email_is_unchanged)
            obj = self._save_company(session, obj, form2)
            View.print_update_success(obj)

        else:
            View.print_forms_errors(form1, form2)

    @classmethod
    def _delete(self, session, user):
        obj_id = View.get_id(View.name)

        if obj_id == 0:
            return None

        obj = session.get(Customer, obj_id)
        if not obj or obj.commercial != user:
            View.print_permission_denied()

            return None

        View.print_detail(obj)
        choice = View.print_delete_confirm(obj)
        if choice == "o":
            obj.delete(session)
            View.print_delete_success(obj_id)
