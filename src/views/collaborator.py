import math

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from werkzeug.datastructures import MultiDict

from ..forms.collaborator import CollaboratorForm
from ..forms.department import DepartmentForm
from ..models.collaborator import Collaborator
from ..utils.fernet import Fernet
from .mixin import MixinView

console = Console()


class View(MixinView):
    name = Collaborator.FRENCH_NAME

    @classmethod
    def print_menu(self):
        console.print(f"\nMenu {self.name.title()}", style="bold", justify="center")
        console.print("__________________", justify="center")

        console.print("\n0. Retour", style="bold", justify="center")
        console.print("\n1. Lister", style="bold", justify="center")
        console.print("\n2. Rechercher", style="bold", justify="center")
        console.print("\n3. Détail", style="bold", justify="center")
        console.print("\n4. Créer", style="bold", justify="center")
        console.print("\n5. Modifier", style="bold", justify="center")
        console.print("\n6. Supprimer", style="bold", justify="center")

    @classmethod
    def print_list(self, qs: list, list_name: str, page_size=5):
        if len(qs) == 0:
            console.print(f"\n\nAucun {self.name} trouvé.", style="italic", end="")

        current_index = 0
        current_page = 1
        number_of_pages = math.ceil(len(qs) / page_size)

        while current_index < len(qs):
            table = Table(title="\n\n" + list_name)
            table.add_column("ID", style="bold")
            table.add_column("Nom", style="bold")
            table.add_column("Département", style="bold")

            end_index = min(current_index + page_size, len(qs))

            for obj in qs[current_index:end_index]:
                table.add_row(str(obj.id), obj.name, obj.role)

            console.print(table)

            console.print(
                f"\n\nPage {current_page} / {number_of_pages}", style="bold", end=""
            )
            if current_page < number_of_pages:
                console.print("\n\nPage suivante (o/n) : ", style="bold", end="")
                choice = input()
                if choice == "n":
                    break

            current_page += 1
            current_index += page_size

    @classmethod
    def print_detail(self, obj: Collaborator):
        if obj:
            table = Table(title=f"\n\nFiche {self.name} n°{obj.id}")
            table.add_column("Information", style="bold")
            table.add_column("Valeur", style="bold")

            table.add_row("Nom complet", obj.name)
            table.add_row("Date de naissance", obj.formatted_birthdate)
            table.add_row("Email", Fernet.decrypt(obj.email))
            table.add_row("Téléphone", obj.formatted_phone)
            table.add_row("", "")
            table.add_row("Département", obj.role)
            table.add_row("", "")
            table.add_row("Date de création", obj.formatted_creation_time)
            table.add_row("Dernière mise à jour", obj.formatted_edition_time)

            console.print(table)
        else:
            console.print(f"\n\nAucun {self.name} trouvé.", style="italic", end="")

    @classmethod
    def get_collaborator_data_to_create(self) -> CollaboratorForm:
        console.print(
            f"\n\nRenseigner le formulaire {self.name}\n\n", style="bold", end=""
        )

        input_data = {
            "first_name": Prompt.ask("Prénom"),
            "last_name": Prompt.ask("\nNom"),
            "birthdate": Prompt.ask("\nDate de naissance (yyyy-mm-dd)"),
            "email": Prompt.ask("\nEmail"),
            "phone": Prompt.ask("\nTéléphone"),
        }

        return CollaboratorForm(MultiDict(input_data))

    @classmethod
    def get_department_data_to_create(self) -> DepartmentForm:
        input_data = {
            "name": Prompt.ask(
                "\nNom du département", choices=["Gestion", "Commercial", "Support"]
            )
        }

        return DepartmentForm(MultiDict(input_data))

    @classmethod
    def get_collaborator_data_to_update(self, obj: Collaborator) -> CollaboratorForm:
        console.print(
            f"\n\nRenseigner le formulaire {self.name}\n\n", style="bold", end=""
        )

        email_is_unchanged = False
        clear_email = Fernet.decrypt(obj.email)

        input_data = {
            "first_name": Prompt.ask("Prénom", default=obj.first_name),
            "last_name": Prompt.ask("\nNom", default=obj.last_name),
            "birthdate": Prompt.ask(
                "\nDate de naissance", default=obj.prompt_birthdate
            ),
            "email": Prompt.ask("\nEmail", default=clear_email),
            "phone": Prompt.ask("\nTéléphone", default=obj.prompt_phone),
        }

        if input_data.get("email") == clear_email:
            email_is_unchanged = True

        return CollaboratorForm(MultiDict(input_data)), email_is_unchanged

    @classmethod
    def get_department_data_to_update(self, obj: Collaborator) -> DepartmentForm:
        input_data = {
            "name": Prompt.ask(
                "\nNom du département",
                choices=["Gestion", "Commercial", "Support"],
                default=obj.prompt_department,
            )
        }

        return DepartmentForm(MultiDict(input_data))
