import builtins

from rich.prompt import Prompt

from src.utils.fernet import Fernet
from src.views.collaborator import Collaborator, CollaboratorForm, DepartmentForm, View
from tests import MixinSetup


class TestView(MixinSetup):
    def test_print_menu(self, capsys):
        View.print_menu()

        captured = capsys.readouterr()

        assert "Menu Collaborateur" in captured.out
        assert "__________________" in captured.out

        assert "0. Retour" in captured.out
        assert "1. Lister" in captured.out
        assert "2. Rechercher" in captured.out
        assert "3. Détail" in captured.out
        assert "4. Créer" in captured.out
        assert "5. Modifier" in captured.out
        assert "6. Supprimer" in captured.out

    def test_print_list(self, capsys, monkeypatch):
        """the paginator displays 5 instances per pages"""

        # 0. test to print an empty qs
        list_name = f"Tous les {View.name}s"
        View.print_list([], list_name)
        captured = capsys.readouterr()
        assert f"Aucun {View.name} trouvé." in captured.out

        # 1. check to see all pages of the paginator
        self.clear_db()
        monkeypatch.setattr(builtins, "input", self.mock_prompt_ask)
        qs = self.create_collaborator_qs()
        assert len(qs) > 5

        View.print_list(qs, list_name)

        captured = capsys.readouterr()
        for collaborator in qs:
            assert "ID" and str(collaborator.id) in captured.out
            assert "Nom" and collaborator.name in captured.out
            assert "Département" and collaborator.role in captured.out

        # 2. check to see only the page 1 of the paginator
        monkeypatch.setattr(builtins, "input", lambda *args, **kwargs: "n")

        View.print_list(qs, list_name)

        captured = capsys.readouterr()

        for collaborator in qs[:5]:
            assert "ID" and str(collaborator.id) in captured.out
            assert "Nom" and collaborator.name in captured.out
            assert "Département" and collaborator.role in captured.out

        for collaborator in qs[5:]:
            assert str(collaborator.id) not in captured.out
            assert collaborator.name not in captured.out

    def test_print_detail(self, capsys):
        collaborator = self.session.get(Collaborator, 1)

        View.print_detail(collaborator)

        captured = capsys.readouterr()

        assert f"Fiche {View.name} n°{collaborator.id}" in captured.out
        assert "Information" in captured.out
        assert "Valeur" in captured.out

        assert "Nom complet" and collaborator.name in captured.out
        assert "Date de naissance" and collaborator.formatted_birthdate in captured.out
        assert "Email" and Fernet.decrypt(collaborator.email) in captured.out
        assert "Téléphone" and collaborator.formatted_phone in captured.out
        assert "Département" and collaborator.role in captured.out
        assert (
            "Date de création" and collaborator.formatted_creation_time in captured.out
        )
        assert (
            "Dernière mise à jour"
            and collaborator.formatted_edition_time in captured.out
        )

        View.print_detail(None)

        captured = capsys.readouterr()
        assert f"Aucun {View.name} trouvé." in captured.out

    def test_get_collaborator_data_to_create(self, capsys, monkeypatch):
        monkeypatch.setattr(Prompt, "ask", self.mock_prompt_ask)

        form = View.get_collaborator_data_to_create()

        captured = capsys.readouterr()

        assert f"Renseigner le formulaire {View.name}" in captured.out
        assert isinstance(form, CollaboratorForm)

    def test_get_department_data_to_create(self, monkeypatch):
        monkeypatch.setattr(Prompt, "ask", self.mock_prompt_ask)

        form = View.get_department_data_to_create()

        assert isinstance(form, DepartmentForm)

    def test_get_collaborator_data_to_update(self, capsys, monkeypatch):
        # 1. test to change email
        monkeypatch.setattr(Prompt, "ask", self.mock_prompt_ask)
        obj = self.session.get(Collaborator, 1)

        form, email_is_unchanged = View.get_collaborator_data_to_update(obj)

        captured = capsys.readouterr()

        assert f"Renseigner le formulaire {View.name}" in captured.out
        assert isinstance(form, CollaboratorForm)
        assert isinstance(email_is_unchanged, bool)
        assert email_is_unchanged is False

        # 2. test to not change email
        monkeypatch.setattr(
            Prompt, "ask", lambda *args, **kwargs: Fernet.decrypt(obj.email)
        )

        form, email_is_unchanged = View.get_collaborator_data_to_update(obj)

        captured = capsys.readouterr()

        assert f"Renseigner le formulaire {View.name}" in captured.out
        assert isinstance(form, CollaboratorForm)
        assert isinstance(email_is_unchanged, bool)
        assert email_is_unchanged is True

    def test_get_department_data_to_update(self, monkeypatch):
        monkeypatch.setattr(Prompt, "ask", self.mock_prompt_ask)
        obj = self.session.get(Collaborator, 1)

        form = View.get_department_data_to_update(obj)

        assert isinstance(form, DepartmentForm)
