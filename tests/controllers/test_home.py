from datetime import datetime, timedelta

from src.controllers.collaborator import Controller as CollaboratorMenu
from src.controllers.contract import Controller as ContractMenu
from src.controllers.customer import Controller as CustomerMenu
from src.controllers.event import Controller as EventMenu
from src.controllers.home import Controller
from src.views.home import View
from tests import MixinSetup


class TestController(MixinSetup):
    def test_session_is_expired(self, monkeypatch):
        self.clear_db()

        # forbidden paths
        monkeypatch.setattr(View, "print_menu", self.mock_permission_denied)
        monkeypatch.setattr(View, "print_gestion_menu", self.mock_permission_denied)
        monkeypatch.setattr(View, "get_user_choice", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "return_to_menu", self.mock_permission_denied)

        # allowed path
        monkeypatch.setattr(View, "logout", lambda *args, **kwargs: None)

        # run paths
        user = self.create_collaborator("Gestion")
        user.last_login = datetime.utcnow() - timedelta(days=1)
        Controller.run(self.session, user)

    def test_run_and_logout(self, monkeypatch):
        self.clear_db()

        # forbidden paths
        monkeypatch.setattr(View, "print_gestion_menu", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "return_to_menu", self.mock_permission_denied)

        # allowed paths
        monkeypatch.setattr(View, "print_menu", lambda *args, **kwargs: None)
        monkeypatch.setattr(View, "get_user_choice", lambda *args, **kwargs: 0)
        monkeypatch.setattr(View, "logout", lambda *args, **kwargs: None)

        # run paths
        user = self.create_collaborator("Commercial")
        user.last_login = datetime.utcnow()
        Controller.run(self.session, user)

    def test_print_menu_collaborator_as_gestion(self, monkeypatch):
        self.clear_db()

        # forbidden paths
        monkeypatch.setattr(View, "print_menu", self.mock_permission_denied)

        # allowed paths
        monkeypatch.setattr(View, "print_gestion_menu", lambda *args, **kwargs: 0)
        monkeypatch.setattr(View, "get_user_choice", lambda *args, **kwargs: 4)
        monkeypatch.setattr(CollaboratorMenu, "run", lambda *args, **kwargs: 0)
        monkeypatch.setattr(Controller, "return_to_menu", lambda *args, **kwargs: 0)

        # run paths
        user = self.create_collaborator("Gestion")
        user.last_login = datetime.utcnow()
        Controller.run(self.session, user)

    def test_print_menu_collaborator_as_commercial(self, monkeypatch):
        self.clear_db()

        # forbidden paths
        monkeypatch.setattr(View, "print_gestion_menu", self.mock_permission_denied)
        monkeypatch.setattr(CollaboratorMenu, "run", self.mock_permission_denied)

        # allowed paths
        monkeypatch.setattr(View, "print_menu", lambda *args, **kwargs: 0)
        monkeypatch.setattr(View, "get_user_choice", lambda *args, **kwargs: 4)
        monkeypatch.setattr(Controller, "return_to_menu", lambda *args, **kwargs: 0)

        # run
        user = self.create_collaborator("Commercial")
        user.last_login = datetime.utcnow()
        Controller.run(self.session, user)

    def test_print_menu_customer(self, monkeypatch):
        self.clear_db()

        # forbidden paths
        monkeypatch.setattr(View, "print_gestion_menu", self.mock_permission_denied)
        monkeypatch.setattr(CollaboratorMenu, "run", self.mock_permission_denied)

        # allowed paths
        monkeypatch.setattr(View, "print_menu", lambda *args, **kwargs: 0)
        monkeypatch.setattr(View, "get_user_choice", lambda *args, **kwargs: 1)
        monkeypatch.setattr(CustomerMenu, "run", lambda *args, **kwargs: 0)
        monkeypatch.setattr(Controller, "return_to_menu", lambda *args, **kwargs: 0)

        # run paths
        user = self.create_collaborator("Commercial")
        user.last_login = datetime.utcnow()
        Controller.run(self.session, user)

    def test_print_menu_contract(self, monkeypatch):
        self.clear_db()

        # forbidden paths
        monkeypatch.setattr(View, "print_gestion_menu", self.mock_permission_denied)
        monkeypatch.setattr(CollaboratorMenu, "run", self.mock_permission_denied)

        # allowed paths
        monkeypatch.setattr(View, "print_menu", lambda *args, **kwargs: 0)
        monkeypatch.setattr(View, "get_user_choice", lambda *args, **kwargs: 2)
        monkeypatch.setattr(ContractMenu, "run", lambda *args, **kwargs: 0)
        monkeypatch.setattr(Controller, "return_to_menu", lambda *args, **kwargs: 0)

        # run
        user = self.create_collaborator("Commercial")
        user.last_login = datetime.utcnow()
        Controller.run(self.session, user)

    def test_print_menu_event(self, monkeypatch):
        self.clear_db()

        # forbidden paths
        monkeypatch.setattr(View, "print_gestion_menu", self.mock_permission_denied)
        monkeypatch.setattr(CollaboratorMenu, "run", self.mock_permission_denied)

        # allowed paths
        monkeypatch.setattr(View, "print_menu", lambda *args, **kwargs: 0)
        monkeypatch.setattr(View, "get_user_choice", lambda *args, **kwargs: 3)
        monkeypatch.setattr(EventMenu, "run", lambda *args, **kwargs: 0)
        monkeypatch.setattr(Controller, "return_to_menu", lambda *args, **kwargs: 0)

        # run
        user = self.create_collaborator("Commercial")
        user.last_login = datetime.utcnow()
        Controller.run(self.session, user)
