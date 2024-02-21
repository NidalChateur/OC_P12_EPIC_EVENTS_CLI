from rich.console import Console
from rich.prompt import Prompt
from werkzeug.datastructures import MultiDict

from ..forms.collaborator import (
    CollaboratorForm,
    FirstConnexionForm,
    LoginForm,
    PasswordForm,
)
from ..models.collaborator import Collaborator
from .mixin import MixinView

console = Console()


class View(MixinView):
    @classmethod
    def print_menu(self):
        console.print("\nConnexion à Epic Events", style="bold", justify="center")
        console.print("_______________________", justify="center")

        console.print("\n0. Quitter", style="bold", justify="center")
        console.print("\n1. Se connecter", style="bold", justify="center")
        console.print("\n2. Modifier mot de passe", style="bold", justify="center")
        console.print("\n3. Première connexion", style="bold", justify="center")

    @classmethod
    def create_password(self) -> PasswordForm:
        console.print(
            "\nCréer maintenant votre mot de passe\n",
            style="bold",
            end="",
        )

        input_data = {
            "password": Prompt.ask("\nNouveau mot de passe", password=True),
            "password_confirm": Prompt.ask(
                "\nConfirmation mot de passe", password=True
            ),
        }

        return PasswordForm(MultiDict(input_data))

    @classmethod
    def get_gestion_data(self) -> CollaboratorForm:
        """used if db is empty"""

        message = "Renseigner le formulaire de création de compte Gestion"
        console.print(f"\n\n{message}\n\n", style="bold", end="")

        input_data = {
            "first_name": Prompt.ask("Prénom"),
            "last_name": Prompt.ask("\nNom"),
            "birthdate": Prompt.ask("\nDate de naissance (yyyy-mm-dd)"),
            "email": Prompt.ask("\nEmail"),
            "phone": Prompt.ask("\nTéléphone"),
        }

        return CollaboratorForm(MultiDict(input_data))

    @classmethod
    def get_user_ids(self) -> LoginForm:
        console.print("\nEntrez vos identifiants\n", style="bold", end="")

        input_data = {
            "email": Prompt.ask("\nEmail"),
            "password": Prompt.ask("\nMot de passe ", password=True),
        }

        return LoginForm(MultiDict(input_data))

    @classmethod
    def change_password(self) -> PasswordForm:
        console.print(
            "\nModifiez maintenant votre mot de passe\n",
            style="bold",
            end="",
        )

        input_data = {
            "password": Prompt.ask("\nNouveau mot de passe", password=True),
            "password_confirm": Prompt.ask(
                "\nConfirmation mot de passe", password=True
            ),
        }

        return PasswordForm(MultiDict(input_data))

    @classmethod
    def print_login_failure(self):
        console.print(
            "\nSaisissez des données d'authentification valides.\n", style="bold red"
        )

    @classmethod
    def print_login_success(self, user: Collaborator):
        console.print("\nConnexion réussie\n", style="bold green")
        console.print(f"\nBienvenue {user.title}\n", style="bold green")

    @classmethod
    def print_password_update_success(self):
        console.print(
            "\nVotre mot de passe a été mis à jour avec succès !\n",
            style="bold green",
            end="",
        )
        console.print(
            "\nConnectez vous avec vos identifiants.\n",
            style="bold blue",
            end="",
        )

    @classmethod
    def print_create_gestion_account_success(self):
        console.print(
            "\nVotre compte Gestion a été créé succès !\n",
            style="bold green",
            end="",
        )
        console.print(
            "\nConnectez vous avec vos identifiants.\n",
            style="bold blue",
            end="",
        )

    @classmethod
    def get_first_connexion_data(self) -> FirstConnexionForm:
        console.print(
            "\nIdentifiez vous avec vos informations personnelles\n",
            style="bold",
            end="",
        )

        input_data = {
            "id": Prompt.ask("\nIdentifiant"),
            "email": Prompt.ask("\nEmail"),
            "birthdate": Prompt.ask("\nDate de naissance (yyyy-mm-dd)"),
        }

        return FirstConnexionForm(MultiDict(input_data))

    @classmethod
    def print_brute_force_attack_message(self):
        message = "\nLe service est momentanément indisponible, veuillez réessayer plus tard.\n"
        console.print(message, style="bold red")
