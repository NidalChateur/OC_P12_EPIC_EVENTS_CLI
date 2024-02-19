import math
from datetime import datetime

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from werkzeug.datastructures import MultiDict

from ..forms.event import EventForm
from ..forms.location import LocationForm
from ..models.collaborator import Collaborator
from ..models.contract_event import Contract, Event
from .collaborator import View as CollaboratorView
from .contract import View as ContractView
from .mixin import MixinView

console = Console()

model = Event


class View(MixinView):
    name = Event.FRENCH_NAME

    @classmethod
    def print_commercial_menu(self):
        self._print_menu()
        self.print_edit_menu()

    @classmethod
    def print_gestion_menu(self):
        self._print_menu()
        console.print("\n4. Sans support", style="bold", justify="center")
        console.print("\n5. Assigner support", style="bold", justify="center")

    @classmethod
    def print_support_menu(self):
        self._print_menu()
        console.print("\n4. Mes événements", style="bold", justify="center")
        console.print("\n5. Modifier", style="bold", justify="center")

    @classmethod
    def _print_menu(self):
        console.print(f"\nMenu {self.name.title()}", style="bold", justify="center")
        console.print("______________", justify="center")

        self.print_read_only_menu()

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
            table.add_column("Contrat ID", style="bold")
            table.add_column("Client", style="bold")
            table.add_column("Commercial", style="bold")
            table.add_column("Support", style="bold")

            end_index = min(current_index + page_size, len(qs))

            for event in qs[current_index:end_index]:
                table.add_row(
                    str(event.id),
                    str(event.contract.id),
                    event.customer_name,
                    event.commercial_name,
                    event.support_name,
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
    def print_detail(self, obj: Event):
        if obj:
            table = Table(title=f"\n\nFiche {self.name} n°{obj.id}")

            table.add_column("Information", style="bold")
            table.add_column("Valeur", style="bold")

            table.add_row("Contrat ID", str(obj.contract.id))
            table.add_row("", "")
            table.add_row("Nom client", obj.customer_name)
            table.add_row("Email client", obj.customer_email)
            table.add_row("Tel client", obj.customer_phone)
            table.add_row("", "")
            table.add_row("Nom support", obj.support_name)
            table.add_row("Email support", obj.support_email)
            table.add_row("Tel support", obj.support_phone)
            table.add_row("", "")
            table.add_row("Date de début", obj.formatted_start_date)
            table.add_row("Date de fin", obj.formatted_end_date)
            table.add_row("Participants", str(obj.attendees))
            table.add_row("Lieu", obj.address)
            table.add_row("Note", obj.note)
            table.add_row("", "")
            table.add_row("Date de création", obj.formatted_creation_time)
            table.add_row("Dernière mise à jour", obj.formatted_edition_time)

            console.print(table)
        else:
            console.print(f"\n\nAucun {self.name} trouvé.", style="italic", end="")

    @classmethod
    def print_create_confirm(self, contract: Contract) -> bool:
        ContractView.print_detail(contract)

        console.print(
            f"\n\nSouhaitez vous créer un {self.name} pour le contrat n°{contract.id} (o/n) ?\n\n",
            style="bold",
            end="",
        )
        return input() == "o"

    @classmethod
    def get_event_data_to_create(self) -> EventForm:
        console.print(
            f"\n\nRenseigner le formulaire de l'{self.name}\n\n", style="bold", end=""
        )

        today = datetime.today().strftime("%Y-%m-%d")

        input_data = {
            "start_date": Prompt.ask("\nDate de début", default=today),
            "start_time": Prompt.ask("\nHeure de début", default="00:00"),
            "end_date": Prompt.ask("\nDate de fin", default=today),
            "end_time": Prompt.ask("\nHeure de fin", default="23:59"),
            "attendees": Prompt.ask("\nNombre de participant"),
            "note": Prompt.ask("\nNote"),
        }

        return EventForm(MultiDict(input_data))

    @classmethod
    def get_location_data_to_create(self) -> LocationForm:
        input_data = {
            "name": Prompt.ask("\nNom du lieu"),
            "number": Prompt.ask("\nNuméro"),
            "street_type": Prompt.ask(
                "\nType de voie",
                choices=[
                    "",
                    "rue",
                    "impasse",
                    "avenue",
                    "boulevard",
                    "allée",
                    "chemin",
                ],
            ),
            "street_name": Prompt.ask("\nNom voie"),
            "zip_code": Prompt.ask("\nCode postal (ex : 75000)"),
            "city": Prompt.ask("\nVille"),
        }

        return LocationForm(MultiDict(input_data))

    @classmethod
    def get_event_data_to_update(self, obj: Event) -> EventForm:
        console.print(
            f"\n\nRenseigner le formulaire de l'{self.name}\n\n", style="bold", end=""
        )

        input_data = {
            "start_date": Prompt.ask("\nDate de début", default=obj.prompt_start_date),
            "start_time": Prompt.ask("\nHeure de début", default=obj.prompt_start_time),
            "end_date": Prompt.ask("\nDate de fin", default=obj.prompt_end_date),
            "end_time": Prompt.ask("\nHeure de fin", default=obj.prompt_end_time),
            "attendees": Prompt.ask(
                "\nNombre de participant", default=str(obj.attendees)
            ),
            "note": Prompt.ask("\nNote", default=obj.note),
        }

        return EventForm(MultiDict(input_data))

    @classmethod
    def get_location_data_to_update(self, obj: Event) -> LocationForm:
        input_data = {
            "name": Prompt.ask("\nNom du lieu", default=obj.location.name),
            "number": Prompt.ask("\nNuméro", default=obj.location.number),
            "street_type": Prompt.ask(
                "\nType de voie",
                choices=[
                    "",
                    "rue",
                    "impasse",
                    "avenue",
                    "boulevard",
                    "allée",
                    "chemin",
                ],
                default=obj.location.street_type,
            ),
            "street_name": Prompt.ask("\nNom voie", default=obj.location.street_name),
            "zip_code": Prompt.ask("\nCode postal", default=obj.location.zip_code),
            "city": Prompt.ask("\nVille", default=obj.location.city),
        }

        return LocationForm(MultiDict(input_data))

    @classmethod
    def print_support_confirm(self, user: Collaborator, event: Event) -> bool:
        CollaboratorView.print_detail(user)

        console.print(
            f"\n\nSouhaitez vous assigner le support {user.name} à l'évènement n°{event.id} (o/n) ?\n\n",
            style="bold",
            end="",
        )
        return input() == "o"
