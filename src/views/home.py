from rich.console import Console

from .mixin import MixinView

console = Console()


class View(MixinView):
    @classmethod
    def print_gestion_menu(self) -> int:
        self.print_menu()
        console.print("\n4. Collaborateurs", style="bold", justify="center")

    @classmethod
    def print_menu(self) -> int:
        console.print("\nMenu Epic Events", style="bold", justify="center")
        console.print("________________", justify="center")

        console.print("\n0. Déconnexion", style="bold", justify="center")
        console.print("\n1. Clients", style="bold", justify="center")
        console.print("\n2. Contrats", style="bold", justify="center")
        console.print("\n3. Événements", style="bold", justify="center")
