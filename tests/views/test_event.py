import builtins

from rich.prompt import Prompt

from src.views.event import Collaborator, Contract, Event, EventForm, LocationForm, View
from tests import MixinSetup


class TestView(MixinSetup):
    def test_print_support_menu(self, capsys):
        View.print_support_menu()

        captured = capsys.readouterr()

        assert f"Menu {View.name.title()}" in captured.out
        assert "______________" in captured.out

        assert "0. Retour" in captured.out
        assert "1. Lister" in captured.out
        assert "2. Rechercher" in captured.out
        assert "3. Détail" in captured.out
        assert "4. Mes événements" in captured.out
        assert "5. Modifier" in captured.out

    def test_print_gestion_menu(self, capsys):
        View.print_gestion_menu()

        captured = capsys.readouterr()

        assert f"Menu {View.name.title()}" in captured.out
        assert "______________" in captured.out

        assert "0. Retour" in captured.out
        assert "1. Lister" in captured.out
        assert "2. Rechercher" in captured.out
        assert "3. Détail" in captured.out
        assert "4. Sans support" in captured.out
        assert "5. Assigner support" in captured.out

    def test_print_commercial_menu(self, capsys):
        View.print_commercial_menu()

        captured = capsys.readouterr()

        assert f"Menu {View.name.title()}" in captured.out
        assert "______________" in captured.out

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
        qs = self.create_event_qs()
        assert len(qs) > 5

        View.print_list(qs, list_name)

        captured = capsys.readouterr()
        for event in qs:
            assert "ID" and str(event.id) in captured.out
            assert "Contrat ID" and str(event.contract.id) in captured.out
            assert "Client" and event.customer_name in captured.out
            assert "Commercial" and event.commercial_name in captured.out
            assert "Support" and event.support_name in captured.out

        # 2. check to see only the page 1 of the paginator
        monkeypatch.setattr(builtins, "input", lambda *args, **kwargs: "n")

        View.print_list(qs, list_name)

        captured = capsys.readouterr()

        for event in qs[:5]:
            assert "ID" and str(event.id) in captured.out
            assert "Contrat ID" and str(event.contract.id) in captured.out
            assert "Client" and event.customer_name in captured.out
            assert "Commercial" and event.commercial_name in captured.out
            assert "Support" and event.support_name in captured.out

        for event in qs[5:]:
            assert str(event.id) not in captured.out

    def test_print_detail(self, capsys):
        obj: Event = self.session.get(Event, 1)

        View.print_detail(obj)

        captured = capsys.readouterr()

        assert f"Fiche {View.name} n°{obj.id}" in captured.out
        assert "Information" in captured.out
        assert "Valeur" in captured.out

        assert "Contrat ID" and str(obj.contract.id) in captured.out

        assert "Nom client" and obj.customer_name in captured.out
        assert "Email client" and obj.customer_email in captured.out
        assert "Tel client" and obj.customer_phone in captured.out

        assert "Nom support" and obj.support_name in captured.out
        assert "Email support" and obj.support_email in captured.out
        assert "Tel support" and obj.support_phone in captured.out

        assert "Date de début" and obj.formatted_start_date in captured.out
        assert "Date de fin" and obj.formatted_end_date in captured.out
        assert "Participants" and str(obj.attendees) in captured.out
        assert "Lieu" and obj.address in captured.out
        assert "Note" and obj.note in captured.out

        assert "Date de création" and obj.formatted_creation_time in captured.out
        assert "Dernière mise à jour" and obj.formatted_edition_time in captured.out

        View.print_detail(None)

        captured = capsys.readouterr()
        assert f"Aucun {View.name} trouvé." in captured.out

    def test_print_create_confirm(self, capsys, monkeypatch):
        monkeypatch.setattr(builtins, "input", lambda: "o")
        obj = self.session.get(Contract, 1)

        response = View.print_create_confirm(obj)

        captured = capsys.readouterr()

        assert f"Fiche {Contract.FRENCH_NAME} n°{obj.id}" in captured.out
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

        assert (
            f"Souhaitez vous créer un {View.name} pour le contrat n°{obj.id} (o/n) ?"
            in captured.out
        )

        assert isinstance(response, bool)
        assert response is True

    def test_get_event_data_to_create(self, capsys, monkeypatch):
        monkeypatch.setattr(Prompt, "ask", self.mock_prompt_ask)

        form = View.get_event_data_to_create()

        captured = capsys.readouterr()

        assert f"Renseigner le formulaire de l'{View.name}" in captured.out
        assert isinstance(form, EventForm)

    def test_get_location_data_to_create(self, monkeypatch):
        monkeypatch.setattr(Prompt, "ask", lambda *args, **kwargs: "rue")

        form = View.get_location_data_to_create()

        assert isinstance(form, LocationForm)

    def test_get_collaborator_data_to_update(self, capsys, monkeypatch):
        monkeypatch.setattr(Prompt, "ask", self.mock_prompt_ask)
        obj = self.session.get(Event, 1)

        form = View.get_event_data_to_update(obj)

        captured = capsys.readouterr()

        assert f"Renseigner le formulaire de l'{View.name}" in captured.out
        assert isinstance(form, EventForm)

    def test_get_location_data_to_update(self, monkeypatch):
        monkeypatch.setattr(Prompt, "ask", self.mock_prompt_ask)
        obj = self.session.get(Event, 1)

        form = View.get_location_data_to_update(obj)

        assert isinstance(form, LocationForm)

    def test_print_support_confirm(self, capsys, monkeypatch):
        monkeypatch.setattr(builtins, "input", lambda: "o")

        support = self.session.get(Collaborator, 1)
        event = self.session.get(Event, 1)

        response = View.print_support_confirm(support, event)

        captured = capsys.readouterr()

        assert (
            f"Souhaitez vous assigner le support {support.name} à l'évènement n°{event.id} (o/n) ?"
            in captured.out
        )

        assert isinstance(response, bool)
        assert response is True
