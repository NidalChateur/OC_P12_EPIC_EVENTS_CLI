from ..utils.session import session_is_expired
from ..views.home import View
from . import collaborator, contract, customer, event


class Controller:
    @classmethod
    def run(self, session, user):
        self._menu(session, user)

    @classmethod
    def return_to_menu(self, session, user):
        self._menu(session, user)

    @classmethod
    def _menu(self, session, user):
        if session_is_expired(user):
            View.logout()

            return None

        if user.role == "Gestion":
            View.print_gestion_menu()
        else:
            View.print_menu()

        choice = View.get_user_choice()

        if choice == 0:
            View.logout()

            return None

        if choice == 1:
            customer.Controller.run(session, user)

        if choice == 2:
            contract.Controller.run(session, user)

        if choice == 3:
            event.Controller.run(session, user)

        if choice == 4 and user.role == "Gestion":
            collaborator.Controller.run(session, user)

        self.return_to_menu(session, user)
