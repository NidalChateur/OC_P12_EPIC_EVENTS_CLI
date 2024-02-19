# pylint: disable=no-member
from ..models.abstract import slugify
from ..models.collaborator import Collaborator
from ..models.department import Department
from ..utils.fernet import Fernet
from ..utils.session import session_is_expired
from ..views.collaborator import View

model1 = Collaborator
model2 = Department


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

        if choice == 4:
            self._create(session)

        if choice == 5:
            self._update(session)

        if choice == 6:
            self._delete(session)

        self.return_to_menu(session, user)

    @classmethod
    def _list(self, session):
        qs = (
            session.query(Collaborator).order_by(Collaborator.edition_time.desc()).all()
        )

        list_name = f"Tous les {View.name}s"
        View.print_list(qs, list_name)

    @classmethod
    def _search(self, session):
        search = View.get_searched_value()

        qs = (
            session.query(Collaborator)
            .filter(Collaborator.slug.like(f"%{slugify(search)}%"))
            .order_by(Collaborator.edition_time.desc())
            .all()
        )

        list_name = f"Résultat recherche {View.name}"
        View.print_list(qs, list_name)

    @classmethod
    def _detail(self, session):
        obj_id = View.get_id(View.name)
        if obj_id != 0:
            obj = session.get(Collaborator, obj_id)
            View.print_detail(obj)

    @classmethod
    def _email_is_unique(self, session, form) -> bool:
        email = form.email.data
        obj = Collaborator.get_with_clear_email(session, email)
        if obj:
            View.print_email_is_not_unique()

            return False

        return True

    @classmethod
    def _create_collaborator(self, session, form) -> Collaborator:
        if self._email_is_unique(session, form):
            user = Collaborator(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=Fernet.encrypt(form.email.data),
                birthdate=form.birthdate.data,
                phone=form.phone.data,
            )
            user.create(session)
            user.save(session)

            return user

    @classmethod
    def _save_department(self, session, user, form) -> Collaborator:
        """get or create the department then save user.department"""

        # check if the department exists
        obj = session.query(Department).filter_by(name=form.name.data).first()

        if user and obj:
            # get existant department
            user.department = obj
            user.save(session)

            return user

        if user and not obj:
            # create department
            department = Department(name=form.name.data)
            department.create(session)
            department.save(session)

            user.department = department
            user.save(session)

            return user

    @classmethod
    def _create(self, session):
        form1 = View.get_collaborator_data_to_create()
        form2 = View.get_department_data_to_create()

        if all([form1.validate(), form2.validate()]):
            user = self._create_collaborator(session, form1)
            user = self._save_department(session, user, form2)
            View.print_create_success(user)

        else:
            View.print_forms_errors(form1, form2)

    @classmethod
    def _update_collaborator(self, session, user, form, email_is_unchanged):
        if user and (email_is_unchanged or self._email_is_unique(session, form)):
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = Fernet.encrypt(form.email.data)
            user.birthdate = form.birthdate.data
            user.phone = form.phone.data

            user.save(session)

            return user

    @classmethod
    def _update(self, session):
        obj_id = View.get_id(View.name)
        if obj_id == 0:
            return None

        obj = session.get(Collaborator, obj_id)
        if not obj:
            View.print_permission_denied()

            return None

        View.print_detail(obj)

        form1, email_is_unchanged = View.get_collaborator_data_to_update(obj)
        form2 = View.get_department_data_to_update(obj)
        if all([form1.validate(), form2.validate()]):
            obj = self._update_collaborator(session, obj, form1, email_is_unchanged)
            obj = self._save_department(session, obj, form2)
            View.print_update_success(obj)

        else:
            View.print_forms_errors(form1, form2)

    @classmethod
    def _delete(self, session):
        obj_id = View.get_id(View.name)

        if obj_id == 0:
            return None

        obj = session.get(Collaborator, obj_id)
        if not obj:
            View.print_permission_denied()

            return None

        View.print_detail(obj)
        choice = View.print_delete_confirm(obj)
        if choice == "o":
            obj.delete(session)
            View.print_delete_success(obj_id)
