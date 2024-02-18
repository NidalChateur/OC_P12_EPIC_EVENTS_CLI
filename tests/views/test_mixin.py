import builtins
import sys

from werkzeug.datastructures import MultiDict

from src.forms.collaborator import CollaboratorForm
from src.forms.department import DepartmentForm
from src.models.collaborator import Collaborator
from src.models.contract_event import Contract
from src.views.mixin import MixinView
from tests import MixinSetup


class TestMixinView(MixinSetup):
    def test_print_create_success(self, capsys):
        self.clear_db()

        collaborator = self.create_collaborator("Gestion")

        MixinView.name = Collaborator.FRENCH_NAME
        MixinView.print_create_success(collaborator)

        captured = capsys.readouterr()

        assert (
            f"{MixinView.name.title()} n°{collaborator.id} créé avec succès !"
            in captured.out
        )

    def test_print_update_success(self, capsys):
        self.clear_db()

        collaborator = self.create_collaborator("Gestion")

        MixinView.name = Collaborator.FRENCH_NAME
        MixinView.print_update_success(collaborator)

        captured = capsys.readouterr()

        assert (
            f"{MixinView.name.title()} n°{collaborator.id} modifié avec succès !"
            in captured.out
        )

    def test_print_delete_success(self, capsys):
        obj_id = 1
        MixinView.name = Collaborator.FRENCH_NAME
        MixinView.print_delete_success(obj_id)

        captured = capsys.readouterr()

        assert (
            f"{MixinView.name.title()} n°{obj_id} supprimé avec succès !"
            in captured.out
        )

    def test_print_signature_success(self, capsys):
        self.clear_db()
        contract = self.create_contract()

        MixinView.name = Contract.FRENCH_NAME
        MixinView.print_signature_success(self.session, contract)

        captured = capsys.readouterr()

        assert (
            f"Félicitation pour la signature du {MixinView.name} n°{contract.id} !"
            in captured.out
        )
        assert (
            f"Vous pouvez maintenant créer un événement pour le {MixinView.name} n°{contract.id}."
            in captured.out
        )

    def test_print_delete_confirm(self, capsys, monkeypatch):
        monkeypatch.setattr(builtins, "input", self.mock_prompt_ask)
        self.clear_db()
        contract = self.create_contract()

        MixinView.name = Contract.FRENCH_NAME
        MixinView.print_delete_confirm(contract)

        captured = capsys.readouterr()

        assert (
            f"Êtes vous sur de vouloir supprimer {MixinView.name} n°{contract.id} (o/n) ?"
            in captured.out
        )

    def test_print_valid_forms(self, capsys):
        MixinView.print_valid_forms()

        captured = capsys.readouterr()

        assert "Formulaire valide !" in captured.out

    def test_print_forms_errors(self, capsys):
        MixinView.name = Collaborator.FRENCH_NAME
        form1 = DepartmentForm(MultiDict({"name": ""}))

        form2 = CollaboratorForm(
            MultiDict(
                {
                    "first_name": "alpha",
                    "last_name": "beta",
                    "email": "alpha@beta.com",
                    "birthdate": "",
                }
            )
        )

        MixinView.print_forms_errors(form1, form2)

        captured = capsys.readouterr()

        assert f"Erreurs dans le formulaire {MixinView.name}:" in captured.out
        assert "- Nom du département : Ce champ est requis." in captured.out
        assert "- Date de naissance : Ce champ est requis." in captured.out

    def test_print_permission_denied(self, capsys):
        MixinView.print_permission_denied()

        captured = capsys.readouterr()

        assert "Permission refusée !" in captured.out

    def test_print_email_is_not_unique(self, capsys):
        MixinView.name = Collaborator.FRENCH_NAME
        MixinView.print_email_is_not_unique()

        captured = capsys.readouterr()

        assert f"Erreurs dans le formulaire {MixinView.name}:" in captured.out
        assert (
            " - email : Adresse email déjà utilisé par un utilisateur." in captured.out
        )

    def test_get_user_choice(self, capsys, monkeypatch):
        monkeypatch.setattr(builtins, "input", lambda: "1")

        choice = MixinView.get_user_choice()

        captured = capsys.readouterr()

        assert "Entrez votre choix (ex : 1) : " in captured.out
        assert isinstance(choice, int)
        assert choice == 1

    def test_get_id(self, capsys, monkeypatch):
        monkeypatch.setattr(builtins, "input", self.mock_prompt_ask)

        obj_id = MixinView.get_id(Collaborator.FRENCH_NAME)

        captured = capsys.readouterr()

        assert (
            f"Entrez l'ID d'un {Collaborator.FRENCH_NAME} (ex : 1) : " in captured.out
        )

        assert isinstance(obj_id, int)
        assert obj_id == 0

        monkeypatch.setattr(builtins, "input", lambda: "1")

        obj_id = MixinView.get_id(Collaborator.FRENCH_NAME)

        captured = capsys.readouterr()

        assert (
            f"Entrez l'ID d'un {Collaborator.FRENCH_NAME} (ex : 1) : " in captured.out
        )

        assert isinstance(obj_id, int)
        assert obj_id == 1

    def test_get_searched_value(self, capsys, monkeypatch):
        monkeypatch.setattr(builtins, "input", self.mock_prompt_ask)

        MixinView.name = Collaborator.FRENCH_NAME
        MixinView.get_searched_value()

        captured = capsys.readouterr()

        assert f"Rechercher {MixinView.name} (ex : Jean Dupont) : " in captured.out

    def test_logout(self, capsys, monkeypatch):
        monkeypatch.setattr(sys, "exit", lambda: None)
        MixinView.logout()

        captured = capsys.readouterr()

        assert "Vous êtes déconnecté." in captured.out
