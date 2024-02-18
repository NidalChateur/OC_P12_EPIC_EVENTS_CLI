from rich.prompt import Prompt

from src.views.login import (
    CollaboratorForm,
    FirstConnexionForm,
    LoginForm,
    PasswordForm,
    View,
)
from tests import MixinSetup


class TestView(MixinSetup):
    def test_print_menu(self, capsys):
        View.print_menu()
        captured = capsys.readouterr()

        assert "Connexion à Epic Events" in captured.out
        assert "_______________________" in captured.out
        assert "0. Quitter" in captured.out
        assert "1. Se connecter" in captured.out
        assert "2. Modifier mot de passe" in captured.out
        assert "3. Première connexion" in captured.out

    def test_create_password(self, capsys, monkeypatch):
        monkeypatch.setattr(Prompt, "ask", self.mock_prompt_ask)

        form = View.create_password()

        captured = capsys.readouterr()

        assert "Créer maintenant votre mot de passe" in captured.out
        assert isinstance(form, PasswordForm)

    def test_get_gestion_data(self, capsys, monkeypatch):
        monkeypatch.setattr(Prompt, "ask", self.mock_prompt_ask)

        form = View.get_gestion_data()

        captured = capsys.readouterr()

        assert "Renseigner le formulaire de création de compte Gestion" in captured.out
        assert isinstance(form, CollaboratorForm)

    def test_get_user_ids(self, capsys, monkeypatch):
        monkeypatch.setattr(Prompt, "ask", self.mock_prompt_ask)

        form = View.get_user_ids()

        captured = capsys.readouterr()

        assert "Entrez vos identifiants" in captured.out
        assert isinstance(form, LoginForm)

    def test_change_password(self, capsys, monkeypatch):
        monkeypatch.setattr(Prompt, "ask", self.mock_prompt_ask)

        form = View.change_password()

        captured = capsys.readouterr()

        assert "Modifiez maintenant votre mot de passe" in captured.out
        assert isinstance(form, PasswordForm)

    def test_print_login_failure(self, capsys):
        View.print_login_failure()

        captured = capsys.readouterr()

        assert "Saisissez des données d'authentification valides." in captured.out

    def test_print_login_success(self, capsys):
        self.clear_db()
        collaborator = self.create_collaborator("Gestion")

        View.print_login_success(collaborator)

        captured = capsys.readouterr()

        assert "Connexion réussie" in captured.out
        assert f"Bienvenue {collaborator.title}" in captured.out

    def test_print_password_update_success(self, capsys):
        View.print_password_update_success()

        captured = capsys.readouterr()

        assert "Votre mot de passe a été mis à jour avec succès !" in captured.out
        assert "Connectez vous avec vos identifiants." in captured.out

    def test_print_create_gestion_account_success(self, capsys):
        View.print_create_gestion_account_success()

        captured = capsys.readouterr()

        assert "Votre compte Gestion a été créé succès !" in captured.out
        assert "Connectez vous avec vos identifiants." in captured.out

    def test_get_first_connexion_data(self, capsys, monkeypatch):
        monkeypatch.setattr(Prompt, "ask", self.mock_prompt_ask)

        form = View.get_first_connexion_data()

        captured = capsys.readouterr()

        assert "Identifiez vous avec vos informations personnelles" in captured.out
        assert isinstance(form, FirstConnexionForm)
