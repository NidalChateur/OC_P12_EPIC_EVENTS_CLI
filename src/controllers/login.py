from ..forms.collaborator import FirstConnexionForm
from ..models.bruteforce import BruteForce
from ..models.collaborator import Collaborator
from ..models.department import Department
from ..settings.settings import init_db
from ..utils.fernet import Fernet
from ..views.login import View
from . import home


class Controller:
    session = init_db()

    @classmethod
    def run(self):
        collaborators = self.session.query(Collaborator).all()

        if collaborators:
            self._menu(self.session)
        else:
            self._create_gestion_account(self.session)

        self.re_run()

    @classmethod
    def re_run(self):
        self.run()

    @classmethod
    def return_to_menu(self, session):
        self._menu(session)

    @classmethod
    def _menu(self, session):
        View.print_menu()

        choice = View.get_user_choice()

        if choice == 0:
            # 1. quit
            View.logout()

            return None

        if choice == 1:
            # 1. login
            user = self._login(session)
            self._redirect_to_home(session, user)

        if choice == 2:
            # 2. change password
            user = self._login(session)
            self._change_password(session, user)

        if choice == 3:
            # 3. first connexion
            user = self._first_login(session)
            self._create_password(session, user)

        self.return_to_menu(session)

    @classmethod
    def _create_gestion_account(self, session):
        form1 = View.get_gestion_data()
        form2 = View.create_password()

        if all([form1.validate(), form2.validate()]):
            department = Department(name="Gestion")
            department.create(session)
            department.save(session)

            collaborator = Collaborator(
                first_name=form1.first_name.data,
                last_name=form1.last_name.data,
                email=Fernet.encrypt(form1.email.data),
                birthdate=form1.birthdate.data,
                phone=form1.phone.data,
                department_id=1,
            )
            collaborator.create(session)
            collaborator.set_password(form2.password.data)
            collaborator.save(session)

            View.print_create_gestion_account_success()
        else:
            View.print_forms_errors(form1, form2)

    @classmethod
    def _login(self, session) -> Collaborator:
        form = View.get_user_ids()

        if form.validate():
            email = form.email.data
            password = form.password.data
            user = self._authenticate(session, email, password)

            return user

        else:
            View.print_login_failure()

    @classmethod
    def _authenticate(self, session, email: str, password: str) -> Collaborator:
        user = Collaborator.get_with_clear_email(session, email)

        if BruteForce.attack_is_detected(session, user):
            View.print_brute_force_attack_message()

            return None

        authenticated_user = Collaborator.authenticate(session, email, password)

        if authenticated_user:
            BruteForce.reset_data(session, authenticated_user)
            View.print_login_success(authenticated_user)

            return user

        else:
            BruteForce.save_data(session, user)
            View.print_login_failure()

    @classmethod
    def _change_password(self, session, user: Collaborator):
        if not user:
            return None

        form = View.change_password()

        if form.validate():
            user.set_password(form.password.data)
            session.commit()
            View.print_password_update_success()
        else:
            View.print_forms_errors(form)

    @classmethod
    def _redirect_to_home(self, session, user: Collaborator):
        if user:
            home.Controller.run(session, user)

    @classmethod
    def _get_user(self, session, form: FirstConnexionForm) -> Collaborator:
        email = form.email.data
        user = Collaborator.get_with_clear_email(session, email)

        return user

    @classmethod
    def _check_user(self, user, form: FirstConnexionForm) -> bool:
        # authenticate for first login
        if not user:
            return False

        if user.last_login is not None:
            return False

        if user.id != form.id.data:
            return False

        if user.birthdate != form.birthdate.data:
            return False

        return user

    @classmethod
    def _first_login(self, session) -> Collaborator:
        form = View.get_first_connexion_data()

        if form.validate():
            user = self._get_user(session, form)
            user = self._check_user(user, form)

            return user

        else:
            View.print_login_failure()

    @classmethod
    def _create_password(self, session, user):
        if not user:
            return None

        View.print_valid_forms()

        form = View.create_password()

        if form.validate():
            user.set_password(form.password.data)
            session.commit()
            View.print_password_update_success()
        else:
            View.print_forms_errors(form)
