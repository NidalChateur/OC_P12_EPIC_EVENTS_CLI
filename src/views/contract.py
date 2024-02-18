import math

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from werkzeug.datastructures import MultiDict

from ..forms.contract import ContractForm
from ..models.contract_event import Contract
from ..models.customer import Customer
from .customer import View as CustomerView
from .mixin import MixinView

console = Console()

model = Contract


class View(MixinView):
    name = Contract.FRENCH_NAME

    @classmethod
    def print_gestion_menu(self):
        self.print_commercial_menu()
        console.print("\n7. Créer", style="bold", justify="center")
        console.print("\n8. Supprimer", style="bold", justify="center")

    @classmethod
    def print_commercial_menu(self):
        self.print_menu()
        console.print("\n4. Non signés", style="bold", justify="center")
        console.print("\n5. Non payés", style="bold", justify="center")
        console.print("\n6. Modifier", style="bold", justify="center")

    @classmethod
    def print_menu(self):
        console.print(f"\nMenu {self.name.title()}", style="bold", justify="center")
        console.print("____________", justify="center")

        console.print("\n0. Retour", style="bold", justify="center")
        console.print("\n1. Lister", style="bold", justify="center")
        console.print("\n2. Rechercher", style="bold", justify="center")
        console.print("\n3. Détail", style="bold", justify="center")

    @classmethod
    def print_list(self, qs: list[model], list_name: str, page_size=5):
        if len(qs) == 0:
            console.print(f"\n\nAucun {self.name} trouvé.", style="italic", end="")

        current_index = 0
        current_page = 1
        number_of_pages = math.ceil(len(qs) / page_size)

        while current_index < len(qs):
            table = Table(title="\n\n" + list_name)
            table.add_column("ID", style="bold")
            table.add_column("Client", style="bold")
            table.add_column("Commercial", style="bold")
            table.add_column("Signé", style="bold")
            table.add_column("Payé", style="bold")

            end_index = min(current_index + page_size, len(qs))

            for contract in qs[current_index:end_index]:
                table.add_row(
                    str(contract.id),
                    contract.customer_name,
                    contract.commercial_name,
                    contract.formatted_is_signed,
                    contract.formatted_is_paid,
                )

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
    def print_detail(self, obj: Contract):
        if obj:
            table = Table(title=f"\n\nFiche {self.name} n°{obj.id}")
            table.add_column("Information", style="bold")
            table.add_column("Valeur", style="bold")

            table.add_row("Nom client", obj.customer_name)
            table.add_row("Email client", obj.customer_email)
            table.add_row("Tel client", obj.customer_phone)
            table.add_row("", "")
            table.add_row("Nom commercial", obj.commercial_name)
            table.add_row("Email commercial", obj.commercial_email)
            table.add_row("Tel commercial", obj.commercial_phone)
            table.add_row("", "")
            table.add_row("Montant total", obj.formatted_total_amount)
            table.add_row("Montant payé", obj.formatted_paid_amount)
            table.add_row("Montant restant", obj.formatted_remaining_amount)
            table.add_row("Signé", obj.formatted_is_signed)
            table.add_row("Payé", obj.formatted_is_paid)
            table.add_row("", "")
            table.add_row("Date de création", obj.formatted_creation_time)
            table.add_row("Dernière mise à jour", obj.formatted_edition_time)

            console.print(table)
        else:
            console.print(f"\n\nAucun {self.name} trouvé.", style="italic", end="")

    @classmethod
    def print_create_confirm(self, customer: Customer) -> bool:
        CustomerView.print_detail(customer)

        console.print(
            f"\n\nSouhaitez vous créer un {self.name} pour le client {customer.name} (o/n) ?\n\n",
            style="bold",
            end="",
        )
        return input() == "o"

    @classmethod
    def get_contract_data_to_create(self) -> ContractForm:
        console.print(
            f"\n\nRenseigner le formulaire du {self.name}\n\n", style="bold", end=""
        )

        input_data = {
            "total_amount": Prompt.ask("Montant total", default=str(0)),
            "paid_amount": Prompt.ask("\nMontant payé", default=str(0)),
            "is_signed": Prompt.ask(
                "\nSignature", default="non", choices=["oui", "non"]
            ),
        }

        if input_data["is_signed"] == "oui":
            input_data["is_signed"] = True
        else:
            input_data["is_signed"] = False

        return ContractForm(MultiDict(input_data))

    @classmethod
    def get_contract_data_to_update(self, obj: Contract) -> ContractForm:
        console.print(
            f"\n\nRenseigner le formulaire du {self.name}\n\n", style="bold", end=""
        )

        if obj.is_signed:
            is_signed = "oui"
        else:
            is_signed = "non"

        input_data = {
            "total_amount": Prompt.ask("Montant total", default=str(obj.total_amount)),
            "paid_amount": Prompt.ask("\nMontant payé", default=str(obj.paid_amount)),
            "is_signed": Prompt.ask(
                "\nSignature", default=is_signed, choices=["oui", "non"]
            ),
        }

        if input_data["is_signed"] == "oui":
            input_data["is_signed"] = True
        else:
            input_data["is_signed"] = False

        return ContractForm(MultiDict(input_data))
