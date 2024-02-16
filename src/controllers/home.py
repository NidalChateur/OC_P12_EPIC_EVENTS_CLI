from ..views.home import View
from . import collaborator, contract, customer, event


class Controller:
    @classmethod
    def run(self, session, user):
        self._menu(session, user)

    @classmethod
    def _menu(self, session, user):
        if user.role == "Gestion":
            View.print_gestion_menu()
        else:
            View.print_menu()

        choice = View.get_user_choice()

        if choice == 0:
            View.logout()

        if choice == 1:
            customer.Controller.run(session, user)

        if choice == 2:
            contract.Controller.run(session, user)

        if choice == 3:
            event.Controller.run(session, user)

        if choice == 4 and user.role == "Gestion":
            collaborator.Controller.run(session, user)

        self._menu(session, user)
