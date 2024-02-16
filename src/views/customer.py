import math

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from werkzeug.datastructures import MultiDict

from ..forms.company import CompanyForm
from ..forms.customer import CustomerForm
from ..models.customer import Customer
from .mixin import MixinView

console = Console()


class View(MixinView):
    name = Customer.FRENCH_NAME

    @classmethod
    def print_commercial_menu(self):
        self.print_menu()
        console.print("\n4. Créer", style="bold", justify="center")
        console.print("\n5. Modifier", style="bold", justify="center")
        console.print("\n6. Supprimer", style="bold", justify="center")

    @classmethod
    def print_menu(self):
        console.print("\nMenu Client", style="bold", justify="center")
        console.print("___________", justify="center")

        console.print("\n0. Retour", style="bold", justify="center")
        console.print("\n1. Lister", style="bold", justify="center")
        console.print("\n2. Rechercher", style="bold", justify="center")
        console.print("\n3. Détail", style="bold", justify="center")

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
            table.add_column("Commercial", style="bold")

            end_index = min(current_index + page_size, len(qs))

            for obj in qs[current_index:end_index]:
                table.add_row(str(obj.id), obj.name, obj.commercial_name)

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
    def print_detail(self, obj: Customer):
        if obj:
            table = Table(title=f"\n\nFiche {self.name} n°{obj.id}")
            table.add_column("Information", style="bold")
            table.add_column("Valeur", style="bold")

            table.add_row("Nom complet", obj.name)
            table.add_row("Email", obj.email)
            table.add_row("Téléphone", obj.formatted_phone)
            table.add_row("", "")
            table.add_row("Nom de l'entreprise", obj.company_name)
            table.add_row("", "")
            table.add_row("Commercial", obj.commercial_name)
            table.add_row("", "")
            table.add_row("Date de création", obj.formatted_creation_time)
            table.add_row("Dernière mise à jour", obj.formatted_edition_time)

            console.print(table)
        else:
            console.print(f"\n\nAucun {self.name} trouvé.", style="italic", end="")

    @classmethod
    def get_customer_data_to_create(self) -> CustomerForm:
        console.print(
            f"\n\nRenseigner le formulaire {self.name}\n\n", style="bold", end=""
        )

        input_data = {
            "first_name": Prompt.ask("Prénom"),
            "last_name": Prompt.ask("\nNom"),
            "email": Prompt.ask("\nEmail"),
            "phone": Prompt.ask("\nTéléphone"),
        }

        return CustomerForm(MultiDict(input_data))

    @classmethod
    def get_company_data_to_create(self) -> CompanyForm:
        input_data = {"name": Prompt.ask("\nNom de l'entreprise")}

        return CompanyForm(MultiDict(input_data))

    @classmethod
    def get_customer_data_to_update(self, obj: Customer) -> CustomerForm:
        console.print(
            f"\n\nRenseigner le formulaire {self.name}\n\n", style="bold", end=""
        )

        email_is_unchanged = False

        input_data = {
            "first_name": Prompt.ask("Prénom", default=obj.first_name),
            "last_name": Prompt.ask("\nNom", default=obj.last_name),
            "email": Prompt.ask("\nEmail", default=obj.email),
            "phone": Prompt.ask("\nTéléphone", default=obj.prompt_phone),
        }

        if input_data.get("email") == obj.email:
            email_is_unchanged = True

        return CustomerForm(MultiDict(input_data)), email_is_unchanged

    @classmethod
    def get_company_data_to_update(self, obj: Customer) -> CompanyForm:
        input_data = {
            "name": Prompt.ask(
                "\nNom de l'entreprise",
                default=obj.prompt_company_name,
            )
        }

        return CompanyForm(MultiDict(input_data))
