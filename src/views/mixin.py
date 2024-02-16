import sys

from rich.console import Console

console = Console()


class MixinView:
    name = ""

    @classmethod
    def print_create_success(self, obj):
        if obj and obj.id:
            self.print_valid_forms()
            success_msg = f"{self.name.title()} n°{obj.id} créé avec succès !\n"

            console.print(success_msg, style="bold green")

    @classmethod
    def print_update_success(self, obj):
        if obj and obj.id:
            self.print_valid_forms()
            success_msg = f"{self.name.title()} n°{obj.id} modifié avec succès !\n"

            console.print(success_msg, style="bold green")

    @classmethod
    def print_delete_success(self, obj_id: int):
        success_msg = f"\n\n{self.name.title()} n°{obj_id} supprimé avec succès !\n\n"
        console.print(success_msg, style="bold green")

    @classmethod
    def print_signature_success(self, session, obj):
        if obj and obj.is_ready_for_event(session):
            success_msg1 = (
                f"Félicitation pour la signature du {self.name} n°{obj.id} !\n"
            )

            console.print(success_msg1, style="bold green")

            success_msg2 = f"Vous pouvez maintenant créer un événement pour le {self.name} n°{obj.id}\n"

            console.print(success_msg2, style="bold blue")

    @classmethod
    def print_delete_confirm(self, obj):
        console.print(
            f"\nÊtes vous sur de vouloir supprimer {self.name} n°{obj.id} (o/n) ?",
            style="bold red",
        )
        return input()

    @classmethod
    def print_valid_forms(self):
        console.print("\n\nFormulaire valide !\n\n", style="bold green", end="")

    @classmethod
    def print_forms_errors(self, form1, form2=None):
        console.print(f"\nErreurs dans le formulaire {self.name}:", style="bold red")
        if not form1.validate():
            for field, errors in form1.errors.items():
                label = getattr(form1, field).label.text
                console.print(f"  - {label} : {', '.join(errors)}")

        if form2 and not form2.validate():
            for field, errors in form2.errors.items():
                label = getattr(form2, field).label.text
                console.print(f"  - {label} : {', '.join(errors)}")

    @classmethod
    def print_permission_denied(self):
        console.print("\nPermission refusée !", style="bold red")

    @classmethod
    def print_email_is_not_unique(self):
        console.print(f"\nErreurs dans le formulaire {self.name}:", style="bold red")
        console.print("  - email : Adresse email déjà utilisé par un utilisateur.")

    @classmethod
    def get_user_choice(self) -> int:
        console.print("\n\nEntrez votre choix (ex : 1) : ", style="bold", end="")

        choice = input()

        if choice.isdigit():
            return int(choice)

    @classmethod
    def get_id(self, obj_name: str) -> int:
        console.print(
            f"\n\nEntrez l'ID d'un {obj_name} (ex : 1) : ", style="bold", end=""
        )

        choice = input()

        if choice.isdigit():
            return int(choice)
        else:
            return 0

    @classmethod
    def get_searched_value(self) -> str:
        console.print(
            f"\n\nRechercher {self.name} (ex : Jean Dupont) : ", style="bold", end=""
        )

        return input()

    @classmethod
    def logout(self) -> str:
        console.print("\nVous êtes déconnecté.\n", style="bold blue")
        sys.exit()
