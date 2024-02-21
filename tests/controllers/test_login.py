import pytest

from src.controllers.home import Controller as HomeMenu
from src.controllers.login import Collaborator, Controller, Fernet
from src.views.login import (
    CollaboratorForm,
    FirstConnexionForm,
    LoginForm,
    MultiDict,
    PasswordForm,
    View,
)
from tests import MixinSetup


class TestController(MixinSetup):
    def test_create_the_first_gestion_account(self, monkeypatch):
        self.clear_db()

        # forbidden paths
        monkeypatch.setattr(View, "print_forms_errors", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "return_to_menu", self.mock_permission_denied)

        # building data to mock View.get_gestion_data
        input_data = {
            "first_name": "John99",
            "last_name": "Doe99",
            "email": "john@gmail99.com",
            "birthdate": "2000-01-01",
            "phone": "0102030405",
        }
        form1 = CollaboratorForm(MultiDict(input_data))

        # building data to mock View.create_password
        input_data2 = {"password": "00000000pW-", "password_confirm": "00000000pW-"}
        form2 = PasswordForm(MultiDict(input_data2))

        # allowed path
        monkeypatch.setattr(Controller, "re_run", lambda *args, **kwargs: None)
        monkeypatch.setattr(Controller, "session", self.session)
        monkeypatch.setattr(View, "get_gestion_data", lambda *args, **kwargs: form1)
        monkeypatch.setattr(View, "create_password", lambda *args, **kwargs: form2)
        monkeypatch.setattr(
            View, "print_create_gestion_account_success", lambda *args, **kwargs: None
        )
        monkeypatch.setattr(Controller, "_menu", lambda *args, **kwargs: None)

        # run paths
        Controller.run()

        # check if the gestion user is created
        created_gestion = self.session.get(Collaborator, 1)
        assert created_gestion
        assert Fernet.decrypt(created_gestion.email) == input_data.get("email")

    def test_run_and_quit(self, monkeypatch):
        self.clear_db()

        # forbidden paths
        monkeypatch.setattr(
            Controller, "_create_gestion_account", self.mock_permission_denied
        )

        monkeypatch.setattr(Controller, "return_to_menu", self.mock_permission_denied)

        # allowed path
        monkeypatch.setattr(Controller, "re_run", lambda *args, **kwargs: None)
        monkeypatch.setattr(Controller, "session", self.session)
        monkeypatch.setattr(View, "print_menu", lambda *args, **kwargs: None)
        monkeypatch.setattr(View, "get_user_choice", lambda *args, **kwargs: 0)
        monkeypatch.setattr(View, "logout", lambda *args, **kwargs: None)

        # run paths
        self.create_collaborator("Gestion")
        Controller.run()

    def test_login(self, monkeypatch):
        self.clear_db()
        # setup user data
        user = self.create_collaborator("Gestion")
        user.set_password(self.CLEAR_PASSWORD)
        user.save(self.session)

        assert user.last_login is None

        # building LoginForm to mock View.get_user_ids()
        input_data = {"email": self.CLEAR_EMAIL, "password": self.CLEAR_PASSWORD}
        form = LoginForm(MultiDict(input_data))

        # forbidden paths
        monkeypatch.setattr(
            Controller, "_create_gestion_account", self.mock_permission_denied
        )
        monkeypatch.setattr(View, "logout", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_change_password", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_first_login", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_create_password", self.mock_permission_denied)
        monkeypatch.setattr(View, "print_login_failure", self.mock_permission_denied)

        # allowed path
        monkeypatch.setattr(Controller, "re_run", lambda *args, **kwargs: None)
        monkeypatch.setattr(Controller, "session", self.session)
        monkeypatch.setattr(View, "print_menu", lambda *args, **kwargs: None)
        monkeypatch.setattr(View, "get_user_choice", lambda *args, **kwargs: 1)
        monkeypatch.setattr(View, "get_user_ids", lambda *args, **kwargs: form)
        monkeypatch.setattr(View, "print_login_success", lambda *args, **kwargs: None)
        monkeypatch.setattr(HomeMenu, "run", lambda *args, **kwargs: None)
        monkeypatch.setattr(Controller, "return_to_menu", lambda *args, **kwargs: None)

        # run paths
        Controller.run()
        user = self.session.get(Collaborator, 1)
        assert user
        assert user.last_login

    def test_login_failure(self, monkeypatch):
        self.clear_db()

        # setup data
        assert len(self.session.query(Collaborator).all()) == 0
        user = self.create_collaborator("Gestion")

        assert Fernet.decrypt(user.email) != "wrong"
        assert Collaborator.check_password("wrong", user.password) is False

        # building LoginForm to mock View.get_user_ids()
        input_data = {"email": "wrong", "password": "wrong"}
        form = LoginForm(MultiDict(input_data))

        # forbidden paths
        monkeypatch.setattr(
            Controller, "_create_gestion_account", self.mock_permission_denied
        )
        monkeypatch.setattr(View, "logout", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_change_password", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_first_login", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_create_password", self.mock_permission_denied)
        monkeypatch.setattr(View, "print_login_success", self.mock_permission_denied)
        monkeypatch.setattr(HomeMenu, "run", self.mock_permission_denied)

        # allowed path
        monkeypatch.setattr(Controller, "re_run", lambda *args, **kwargs: None)
        monkeypatch.setattr(Controller, "session", self.session)
        monkeypatch.setattr(View, "print_menu", lambda *args, **kwargs: None)
        monkeypatch.setattr(View, "get_user_choice", lambda *args, **kwargs: 1)
        monkeypatch.setattr(View, "get_user_ids", lambda *args, **kwargs: form)
        monkeypatch.setattr(View, "print_login_failure", lambda *args, **kwargs: None)
        monkeypatch.setattr(Controller, "return_to_menu", lambda *args, **kwargs: None)

        # run paths
        Controller.run()

        # check if no user were connected
        all_collaborators = self.session.query(Collaborator).all()
        for collaborator in all_collaborators:
            assert collaborator.last_login is None

    def test_change_password(self, monkeypatch):
        self.clear_db()

        # setup user data
        user = self.create_collaborator("Gestion")
        user.set_password(self.CLEAR_PASSWORD)
        user.save(self.session)

        # building LoginForm to mock View.get_user_ids  and View.change_password
        input_data = {"email": self.CLEAR_EMAIL, "password": self.CLEAR_PASSWORD}
        form = LoginForm(MultiDict(input_data))

        input_data2 = {
            "password": "new_Password18*",
            "password_confirm": "new_Password18*",
        }
        form2 = PasswordForm(MultiDict(input_data2))

        # forbidden paths
        monkeypatch.setattr(
            Controller, "_create_gestion_account", self.mock_permission_denied
        )
        monkeypatch.setattr(View, "logout", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_first_login", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_create_password", self.mock_permission_denied)
        monkeypatch.setattr(View, "print_login_failure", self.mock_permission_denied)
        monkeypatch.setattr(View, "print_forms_errors", self.mock_permission_denied)

        # allowed path
        monkeypatch.setattr(Controller, "re_run", lambda *args, **kwargs: None)
        monkeypatch.setattr(Controller, "session", self.session)
        monkeypatch.setattr(View, "print_menu", lambda *args, **kwargs: None)
        monkeypatch.setattr(View, "get_user_choice", lambda *args, **kwargs: 2)
        monkeypatch.setattr(View, "get_user_ids", lambda *args, **kwargs: form)
        monkeypatch.setattr(View, "print_login_success", lambda *args, **kwargs: None)

        monkeypatch.setattr(View, "change_password", lambda *args, **kwargs: form2)
        monkeypatch.setattr(
            View, "print_password_update_success", lambda *args, **kwargs: None
        )

        monkeypatch.setattr(Controller, "return_to_menu", lambda *args, **kwargs: None)

        # run paths
        Controller.run()

        # check if the password changed
        user = self.session.get(Collaborator, 1)
        assert user
        assert Fernet.decrypt(user.email) == self.CLEAR_EMAIL
        assert Collaborator.check_password("new_Password18*", user.password)

    def test_first_connexion(self, monkeypatch):
        self.clear_db()

        # setup user data
        user = self.create_collaborator("Gestion")
        assert user.password is None
        assert user.last_login is None

        # building LoginForm to mock View.get_first_connexion_data and View.get_user_ids and View.create_password
        input_data = {
            "id": user.id,
            "email": self.CLEAR_EMAIL,
            "birthdate": user.prompt_birthdate,
        }
        form = FirstConnexionForm(MultiDict(input_data))

        input_data2 = {
            "password": "new_Password77*",
            "password_confirm": "new_Password77*",
        }
        form2 = PasswordForm(MultiDict(input_data2))

        # forbidden paths
        monkeypatch.setattr(
            Controller, "_create_gestion_account", self.mock_permission_denied
        )
        monkeypatch.setattr(View, "logout", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_login", self.mock_permission_denied)
        monkeypatch.setattr(
            Controller, "_redirect_to_home", self.mock_permission_denied
        )
        monkeypatch.setattr(Controller, "_change_password", self.mock_permission_denied)
        monkeypatch.setattr(View, "print_login_failure", self.mock_permission_denied)
        monkeypatch.setattr(View, "print_forms_errors", self.mock_permission_denied)

        # allowed path
        monkeypatch.setattr(Controller, "re_run", lambda *args, **kwargs: None)
        monkeypatch.setattr(Controller, "session", self.session)
        monkeypatch.setattr(View, "print_menu", lambda *args, **kwargs: None)
        monkeypatch.setattr(View, "get_user_choice", lambda *args, **kwargs: 3)
        monkeypatch.setattr(
            View, "get_first_connexion_data", lambda *args, **kwargs: form
        )
        monkeypatch.setattr(View, "print_valid_forms", lambda *args, **kwargs: None)

        monkeypatch.setattr(View, "create_password", lambda *args, **kwargs: form2)
        monkeypatch.setattr(
            View, "print_password_update_success", lambda *args, **kwargs: None
        )

        monkeypatch.setattr(Controller, "return_to_menu", lambda *args, **kwargs: None)

        # run paths
        Controller.run()

        # check if the password changed
        user = self.session.get(Collaborator, 1)
        assert user
        assert user.password is not None
        assert Fernet.decrypt(user.email) == self.CLEAR_EMAIL
        assert Collaborator.check_password("new_Password77*", user.password)

    def test_first_connexion_failure_with_wrong_id(self, monkeypatch):
        self.clear_db()

        # setup user data
        user = self.create_collaborator("Gestion")
        assert user.password is None

        # building LoginForm to mock View.get_first_connexion_data and View.get_user_ids and View.create_password
        input_data = {
            "id": 15,
            "email": self.CLEAR_EMAIL,
            "birthdate": user.prompt_birthdate,
        }
        form = FirstConnexionForm(MultiDict(input_data))

        # forbidden paths
        monkeypatch.setattr(
            Controller, "_create_gestion_account", self.mock_permission_denied
        )
        monkeypatch.setattr(View, "logout", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_login", self.mock_permission_denied)
        monkeypatch.setattr(
            Controller, "_redirect_to_home", self.mock_permission_denied
        )
        monkeypatch.setattr(Controller, "_change_password", self.mock_permission_denied)
        monkeypatch.setattr(View, "print_valid_forms", self.mock_permission_denied)
        monkeypatch.setattr(
            View, "print_password_update_success", self.mock_permission_denied
        )

        # allowed path
        monkeypatch.setattr(Controller, "re_run", lambda *args, **kwargs: None)
        monkeypatch.setattr(Controller, "session", self.session)
        monkeypatch.setattr(View, "print_menu", lambda *args, **kwargs: None)
        monkeypatch.setattr(View, "get_user_choice", lambda *args, **kwargs: 3)
        monkeypatch.setattr(
            View, "get_first_connexion_data", lambda *args, **kwargs: form
        )

        monkeypatch.setattr(Controller, "return_to_menu", lambda *args, **kwargs: None)

        # run paths
        Controller.run()

        # check if the password changed
        user = self.session.get(Collaborator, 1)
        assert user.password is None
        self.clear_db()

    @pytest.mark.parametrize(
        "attempts, user_ids",
        [
            # invalid user ids for 1,2,3
            (1, {"email": "unknown@mail.com", "password": "unknown"}),
            (2, {"email": "unknown@mail.com", "password": "unknown"}),
            (3, {"email": "unknown@mail.com", "password": "unknown"}),
            # valid user ids for 4,5
            (4, {"email": "john@gmail.com", "password": "00000000pW-"}),
            (5, {"email": "john@gmail.com", "password": "00000000pW-"}),
        ],
    )
    def test_brute_force_attack(self, monkeypatch, capsys, attempts, user_ids):
        # setup user data
        user = self.create_collaborator("Gestion")
        user.set_password(self.CLEAR_PASSWORD)
        user.save(self.session)

        # building LoginForm to mock View.get_user_ids()
        form = LoginForm(MultiDict(user_ids))

        # forbidden paths
        monkeypatch.setattr(
            Controller, "_create_gestion_account", self.mock_permission_denied
        )
        monkeypatch.setattr(View, "logout", self.mock_permission_denied)
        monkeypatch.setattr(HomeMenu, "run", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_change_password", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_first_login", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_create_password", self.mock_permission_denied)
        monkeypatch.setattr(View, "print_login_success", self.mock_permission_denied)

        # allowed path
        monkeypatch.setattr(Controller, "re_run", lambda *args, **kwargs: None)
        monkeypatch.setattr(Controller, "session", self.session)
        monkeypatch.setattr(View, "get_user_choice", lambda *args, **kwargs: 1)
        monkeypatch.setattr(View, "get_user_ids", lambda *args, **kwargs: form)
        monkeypatch.setattr(Controller, "return_to_menu", lambda *args, **kwargs: None)

        # run paths
        Controller.run()
        captured = capsys.readouterr()
        if attempts in [1, 2, 3]:
            assert "Saisissez des données d'authentification valides." in captured.out

        if attempts in [4, 5]:
            assert (
                "Le service est momentanément indisponible, veuillez réessayer plus tard."
                in captured.out
            )

            user = self.session.get(Collaborator, 1)
            assert user
            # check that user ids are valid
            assert Fernet.decrypt(user.email) == user_ids["email"]
            assert Collaborator.check_password(user_ids["password"], user.password)
            # check that user has never been connected
            assert user.last_login is None
