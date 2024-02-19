from datetime import datetime, timedelta

from src.controllers.collaborator import Controller
from src.views.collaborator import View
from tests import MixinSetup


class TestController(MixinSetup):
    def test_session_is_expired(self, monkeypatch):
        self.clear_db()

        # forbidden paths
        monkeypatch.setattr(View, "print_menu", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "return_to_menu", self.mock_permission_denied)

        # allowed path
        monkeypatch.setattr(View, "logout", lambda *args, **kwargs: None)

        # run paths
        user = self.create_collaborator("Gestion")
        user.last_login = datetime.utcnow() - timedelta(days=1)
        Controller.run(self.session, user)

    def test_run_to_home_menu(self, monkeypatch):
        self.clear_db()

        # forbidden paths
        monkeypatch.setattr(Controller, "return_to_menu", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_list", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_search", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_detail", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_create", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_update", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_delete", self.mock_permission_denied)

        # allowed path
        monkeypatch.setattr(View, "print_menu", lambda *args, **kwargs: None)
        monkeypatch.setattr(View, "get_user_choice", lambda *args, **kwargs: 0)

        # run paths
        user = self.create_collaborator("Gestion")
        user.last_login = datetime.utcnow()
        Controller.run(self.session, user)

    def test_list(self, monkeypatch):
        self.clear_db()

        # forbidden paths

        monkeypatch.setattr(Controller, "_search", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_detail", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_create", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_update", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_delete", self.mock_permission_denied)

        # allowed path
        monkeypatch.setattr(View, "print_menu", lambda *args, **kwargs: None)
        monkeypatch.setattr(View, "get_user_choice", lambda *args, **kwargs: 1)
        monkeypatch.setattr(View, "print_list", lambda *args, **kwargs: None)
        monkeypatch.setattr(Controller, "return_to_menu", lambda *args, **kwargs: None)

        # run paths
        user = self.create_collaborator("Gestion")
        user.last_login = datetime.utcnow()
        Controller.run(self.session, user)

    def test_search(self, monkeypatch):
        self.clear_db()

        # forbidden paths
        monkeypatch.setattr(Controller, "_list", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_detail", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_create", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_update", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_delete", self.mock_permission_denied)

        # allowed path
        monkeypatch.setattr(View, "print_menu", lambda *args, **kwargs: None)
        monkeypatch.setattr(View, "get_user_choice", lambda *args, **kwargs: 2)
        monkeypatch.setattr(View, "get_searched_value", lambda *args, **kwargs: "2")
        monkeypatch.setattr(View, "print_list", lambda *args, **kwargs: None)
        monkeypatch.setattr(Controller, "return_to_menu", lambda *args, **kwargs: None)

        # run paths
        user = self.create_collaborator("Gestion")
        user.last_login = datetime.utcnow()
        Controller.run(self.session, user)

    def test_detail(self, monkeypatch):
        self.clear_db()

        # forbidden paths
        monkeypatch.setattr(Controller, "_list", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_search", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_create", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_update", self.mock_permission_denied)
        monkeypatch.setattr(Controller, "_delete", self.mock_permission_denied)

        # allowed path
        monkeypatch.setattr(View, "print_menu", lambda *args, **kwargs: None)
        monkeypatch.setattr(View, "get_user_choice", lambda *args, **kwargs: 3)
        monkeypatch.setattr(View, "get_id", lambda *args, **kwargs: "3")
        monkeypatch.setattr(View, "print_detail", lambda *args, **kwargs: None)
        monkeypatch.setattr(Controller, "return_to_menu", lambda *args, **kwargs: None)

        # run paths
        user = self.create_collaborator("Gestion")
        user.last_login = datetime.utcnow()
        Controller.run(self.session, user)
