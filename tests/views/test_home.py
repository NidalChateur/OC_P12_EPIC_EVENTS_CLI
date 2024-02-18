from src.views.home import View
from tests import MixinSetup


class TestView(MixinSetup):
    def test_print_menu(self, capsys):
        View.print_menu()

        captured = capsys.readouterr()

        assert "Menu Epic Events" in captured.out
        assert "________________" in captured.out

        assert "0. Déconnexion" in captured.out
        assert "1. Clients" in captured.out
        assert "2. Contrats" in captured.out
        assert "3. Événements" in captured.out

    def test_print_gestion_menu(self, capsys):
        View.print_gestion_menu()

        captured = capsys.readouterr()

        assert "Menu Epic Events" in captured.out
        assert "________________" in captured.out

        assert "0. Déconnexion" in captured.out
        assert "1. Clients" in captured.out
        assert "2. Contrats" in captured.out
        assert "3. Événements" in captured.out
        assert "4. Collaborateurs" in captured.out
