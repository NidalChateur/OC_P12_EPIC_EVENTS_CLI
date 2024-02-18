import builtins

from rich.prompt import Prompt

from src.views.contract import Contract, ContractForm, Customer, View
from tests import MixinSetup


class TestView(MixinSetup):
    def test_print_menu(self, capsys):
        View.print_menu()

        captured = capsys.readouterr()

        assert "Menu Contrat" in captured.out
        assert "____________" in captured.out

        assert "0. Retour" in captured.out
        assert "1. Lister" in captured.out
        assert "2. Rechercher" in captured.out
        assert "3. Détail" in captured.out

    def test_print_commercial_menu(self, capsys):
        View.print_commercial_menu()

        captured = capsys.readouterr()

        assert "Menu Contrat" in captured.out
        assert "____________" in captured.out

        assert "0. Retour" in captured.out
        assert "1. Lister" in captured.out
        assert "2. Rechercher" in captured.out
        assert "3. Détail" in captured.out
        assert "4. Non signés" in captured.out
        assert "5. Non payés" in captured.out
        assert "6. Modifier" in captured.out

    def test_print_gestion_menu(self, capsys):
        View.print_gestion_menu()

        captured = capsys.readouterr()

        assert "Menu Contrat" in captured.out
        assert "____________" in captured.out

        assert "0. Retour" in captured.out
        assert "1. Lister" in captured.out
        assert "2. Rechercher" in captured.out
        assert "3. Détail" in captured.out
        assert "4. Non signés" in captured.out
        assert "5. Non payés" in captured.out
        assert "6. Modifier" in captured.out
        assert "7. Créer" in captured.out
        assert "8. Supprimer" in captured.out

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
        qs = self.create_contract_qs()
        assert len(qs) > 5

        View.print_list(qs, list_name)

        captured = capsys.readouterr()
        for obj in qs:
            assert "ID" and str(obj.id) in captured.out
            assert "Client" and obj.customer_name in captured.out
            assert "Commercial" and obj.commercial_name in captured.out
            assert "Signé" and obj.commercial_name in captured.out
            assert "Payé" and obj.commercial_name in captured.out

        # 2. check to see only the page 1 of the paginator
        monkeypatch.setattr(builtins, "input", lambda *args, **kwargs: "n")

        View.print_list(qs, list_name)

        captured = capsys.readouterr()

        for obj in qs[:5]:
            assert "ID" and str(obj.id) in captured.out
            assert "Client" and obj.customer_name in captured.out
            assert "Commercial" and obj.commercial_name in captured.out
            assert "Signé" and obj.commercial_name in captured.out
            assert "Payé" and obj.commercial_name in captured.out

        for obj in qs[5:]:
            assert str(obj.id) not in captured.out

    def test_print_detail(self, capsys):
        obj = self.session.get(Contract, 1)

        View.print_detail(obj)

        captured = capsys.readouterr()

        assert f"Fiche {View.name} n°{obj.id}" in captured.out
        assert "Information" in captured.out
        assert "Valeur" in captured.out

        assert "Nom client" and obj.customer_name in captured.out
        assert "Email client" and obj.customer_email in captured.out
        assert "Tel client" and obj.customer_phone in captured.out

        assert "Nom commercial" and obj.commercial_name in captured.out
        assert "Email commercial" and obj.commercial_email in captured.out
        assert "Tel commercial" and obj.commercial_phone in captured.out

        assert "Montant total" and obj.formatted_total_amount in captured.out
        assert "Montant payé" and obj.formatted_paid_amount in captured.out
        assert "Montant restant" and obj.formatted_remaining_amount in captured.out
        assert "Signé" and obj.formatted_is_signed in captured.out
        assert "Payé" and obj.formatted_is_paid in captured.out

        assert "Date de création" and obj.formatted_creation_time in captured.out
        assert "Dernière mise à jour" and obj.formatted_edition_time in captured.out

        View.print_detail(None)

        captured = capsys.readouterr()
        assert f"Aucun {View.name} trouvé." in captured.out

    def test_print_create_confirm(self, capsys, monkeypatch):
        monkeypatch.setattr(builtins, "input", lambda: "o")
        obj = self.session.get(Customer, 1)

        response = View.print_create_confirm(obj)

        captured = capsys.readouterr()

        assert f"Fiche {Customer.FRENCH_NAME} n°{obj.id}" in captured.out
        assert "Information" in captured.out
        assert "Valeur" in captured.out

        assert "Nom complet" and obj.name in captured.out
        assert "Email" and obj.email in captured.out
        assert "Téléphone" and obj.formatted_phone in captured.out
        assert "Nom de l'entreprise" and obj.company_name in captured.out
        assert "Commercial" and obj.commercial_name in captured.out
        assert "Date de création" and obj.formatted_creation_time in captured.out
        assert "Dernière mise à jour" and obj.formatted_edition_time in captured.out

        assert (
            f"Souhaitez vous créer un {View.name} pour le client {obj.name} (o/n) ?"
            in captured.out
        )

        assert isinstance(response, bool)
        assert response is True

    def test_get_contract_data_to_create(self, capsys, monkeypatch):
        monkeypatch.setattr(Prompt, "ask", lambda *args, **kwargs: "oui")

        form = View.get_contract_data_to_create()

        captured = capsys.readouterr()

        assert f"Renseigner le formulaire du {View.name}" in captured.out
        assert isinstance(form, ContractForm)
        assert form.is_signed.data is True

        monkeypatch.setattr(Prompt, "ask", lambda *args, **kwargs: "non")

        form = View.get_contract_data_to_create()

        captured = capsys.readouterr()

        assert f"Renseigner le formulaire du {View.name}" in captured.out
        assert isinstance(form, ContractForm)
        assert form.is_signed.data is False

    def test_get_contract_data_to_update(self, capsys, monkeypatch):
        monkeypatch.setattr(Prompt, "ask", lambda *args, **kwargs: "oui")
        obj = self.session.get(Contract, 1)
        obj.is_signed = False

        form = View.get_contract_data_to_update(obj)

        captured = capsys.readouterr()

        assert f"Renseigner le formulaire du {View.name}" in captured.out
        assert isinstance(form, ContractForm)
        assert form.is_signed.data is True

        monkeypatch.setattr(Prompt, "ask", lambda *args, **kwargs: "non")

        obj.is_signed = True
        form = View.get_contract_data_to_update(obj)

        captured = capsys.readouterr()

        assert f"Renseigner le formulaire du {View.name}" in captured.out
        assert isinstance(form, ContractForm)
        assert form.is_signed.data is False
