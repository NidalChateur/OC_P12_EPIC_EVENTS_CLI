import builtins

from rich.prompt import Prompt

from src.views.customer import CompanyForm, Customer, CustomerForm, View
from tests import MixinSetup


class TestView(MixinSetup):
    def test_print_menu(self, capsys):
        View.print_menu()

        captured = capsys.readouterr()

        assert "Menu Client" in captured.out
        assert "___________" in captured.out

        assert "0. Retour" in captured.out
        assert "1. Lister" in captured.out
        assert "2. Rechercher" in captured.out
        assert "3. Détail" in captured.out

    def test_print_commercial_menu(self, capsys):
        View.print_commercial_menu()

        captured = capsys.readouterr()

        assert "Menu Client" in captured.out
        assert "___________" in captured.out

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
        View.print_list([], "Tous les clients")
        captured = capsys.readouterr()
        assert f"Aucun {View.name} trouvé." in captured.out

        # 1. check to see all pages of the paginator
        self.clear_db()
        monkeypatch.setattr(builtins, "input", self.mock_prompt_ask)
        qs = self.create_customer_qs()
        assert len(qs) > 5

        View.print_list(qs, "Tous les clients")

        captured = capsys.readouterr()
        for customer in qs:
            assert "ID" and str(customer.id) in captured.out
            assert "Nom" and customer.name in captured.out
            assert "Commercial" and customer.commercial_name in captured.out

        # 2. check to see only the page 1 of the paginator
        monkeypatch.setattr(builtins, "input", lambda: "n")

        View.print_list(qs, "Tous les clients")

        captured = capsys.readouterr()
        for customer in qs[:5]:
            assert "ID" and str(customer.id) in captured.out
            assert "Nom" and customer.name in captured.out
            assert "Commercial" and customer.commercial_name in captured.out

        for customer in qs[5:]:
            assert str(customer.id) not in captured.out
            assert customer.name not in captured.out

    def test_print_detail(self, capsys):
        customer = self.session.get(Customer, 1)

        View.print_detail(customer)

        captured = capsys.readouterr()

        assert f"Fiche {View.name} n°{customer.id}" in captured.out
        assert "Information" in captured.out
        assert "Valeur" in captured.out

        assert "Nom complet" and customer.name in captured.out
        assert "Email" and customer.email in captured.out
        assert "Téléphone" and customer.formatted_phone in captured.out
        assert "Nom de l'entreprise" and customer.company_name in captured.out
        assert "Commercial" and customer.commercial_name in captured.out
        assert "Date de création" and customer.formatted_creation_time in captured.out
        assert (
            "Dernière mise à jour" and customer.formatted_edition_time in captured.out
        )

        View.print_detail(None)

        captured = capsys.readouterr()
        assert f"Aucun {View.name} trouvé." in captured.out

    def test_get_customer_data_to_create(self, capsys, monkeypatch):
        monkeypatch.setattr(Prompt, "ask", self.mock_prompt_ask)

        form = View.get_customer_data_to_create()

        captured = capsys.readouterr()

        assert f"Renseigner le formulaire {View.name}" in captured.out
        assert isinstance(form, CustomerForm)

    def test_get_company_data_to_create(self, monkeypatch):
        monkeypatch.setattr(Prompt, "ask", self.mock_prompt_ask)

        form = View.get_company_data_to_create()

        assert isinstance(form, CompanyForm)

    def test_get_customer_data_to_update(self, capsys, monkeypatch):
        # 1. test to change email
        monkeypatch.setattr(Prompt, "ask", self.mock_prompt_ask)
        customer = self.session.get(Customer, 1)

        form, email_is_unchanged = View.get_customer_data_to_update(customer)

        captured = capsys.readouterr()

        assert f"Renseigner le formulaire {View.name}" in captured.out
        assert isinstance(form, CustomerForm)
        assert isinstance(email_is_unchanged, bool)
        assert email_is_unchanged is False

        # 2. test to not change email
        monkeypatch.setattr(Prompt, "ask", lambda *args, **kwargs: customer.email)

        form, email_is_unchanged = View.get_customer_data_to_update(customer)

        captured = capsys.readouterr()

        assert f"Renseigner le formulaire {View.name}" in captured.out
        assert isinstance(form, CustomerForm)
        assert isinstance(email_is_unchanged, bool)
        assert email_is_unchanged is True

    def test_get_company_data_to_update(self, monkeypatch):
        monkeypatch.setattr(Prompt, "ask", self.mock_prompt_ask)
        customer = self.session.get(Customer, 1)

        form = View.get_company_data_to_update(customer)

        assert isinstance(form, CompanyForm)
