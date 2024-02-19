# pylint: disable=no-member
from ..models.collaborator import Collaborator
from ..models.contract_event import Contract, Event
from ..models.location import Location
from ..utils.session import session_is_expired
from ..utils.slugify import slugify
from ..views.event import View

model1 = Event
model2 = Location


class Controller:
    @classmethod
    def run(self, session, user):
        self._menu(session, user)

    @classmethod
    def return_to_menu(self, session, user):
        self._menu(session, user)

    @classmethod
    def _menu(self, session, user) -> bool:
        if session_is_expired(user):
            View.logout()

            return None

        if user.role == "Gestion":
            View.print_gestion_menu()

        if user.role == "Commercial":
            View.print_commercial_menu()

        if user.role == "Support":
            View.print_support_menu()

        choice = View.get_user_choice()

        if choice == 0:
            back_to_home_menu = True

            return back_to_home_menu

        if choice == 1:
            self._list(session)

        if choice == 2:
            self._search(session)

        if choice == 3:
            self._detail(session)

        if choice == 4 and user.role == "Support":
            self._support_events(session, user)

        if choice == 4 and user.role == "Gestion":
            self._events_without_support(session)

        if choice == 4 and user.role == "Commercial":
            self._create(session, user)

        if choice == 5 and user.role in ["Support", "Commercial"]:
            self._update(session, user)

        if choice == 5 and user.role == "Gestion":
            self._change_support(session)

        if choice == 6 and user.role == "Commercial":
            self._delete(session, user)

        self.return_to_menu(session, user)

    @classmethod
    def _list(self, session):
        qs = session.query(Event).order_by(Event.edition_time.desc()).all()
        list_name = f"Tous les {View.name}s"
        View.print_list(qs, list_name)

    @classmethod
    def _search(self, session):
        search = View.get_searched_value()

        qs = (
            session.query(Event)
            .filter(Event.slug.like(f"%{slugify(search)}%"))
            .order_by(Event.edition_time.desc())
            .all()
        )

        list_name = f"Résultat recherche {View.name}"
        View.print_list(qs, list_name)

    @classmethod
    def _get_event(self, session) -> Event:
        obj_id = View.get_id(View.name)
        if obj_id != 0 and session.get(Event, obj_id):
            return session.get(Event, obj_id)

    @classmethod
    def _detail(self, session):
        obj = self._get_event(session)
        if obj:
            View.print_detail(obj)

    @classmethod
    def _support_events(self, session, user):
        qs = (
            session.query(Event)
            .filter(Event.support == user)
            .order_by(Event.edition_time.desc())
            .all()
        )
        list_name = f"Mes {View.name}s"
        View.print_list(qs, list_name)

    @classmethod
    def _events_without_support(self, session):
        qs = (
            session.query(Event)
            .filter(Event.support == None)  # noqa: E711
            .order_by(Event.edition_time.desc())
            .all()
        )
        list_name = f"Les {View.name}s sans support"
        View.print_list(qs, list_name)

    @classmethod
    def _get_contract(self, session) -> Contract:
        obj_id = View.get_id(Contract.FRENCH_NAME)
        if obj_id != 0:
            obj = session.get(Contract, obj_id)

            return obj

    @classmethod
    def _check_contract(self, session, user, contract: Contract) -> bool:
        if not contract:
            View.print_permission_denied()

            return False

        if not contract.is_ready_for_event(session):
            View.print_permission_denied()

            return False

        if contract.customer.commercial != user:
            View.print_permission_denied()

            return False

        return View.print_create_confirm(contract)

    @classmethod
    def _create_event(self, session, contract, form) -> Event:
        event = Event(
            contract=contract,
            start_date=form.start.data,
            end_date=form.end.data,
            attendees=form.attendees.data,
            note=form.note.data,
        )
        event.create(session)
        event.save(session)

        return event

    @classmethod
    def _create_location(self, session, form) -> Location:
        location = Location(
            name=form.name.data,
            number=form.number.data,
            street_type=form.street_type.data,
            street_name=form.street_name.data,
            zip_code=form.zip_code.data,
            city=form.city.data,
        )
        location.create(session)
        location.save(session)

        return location

    @classmethod
    def _save_location(self, session, event, form) -> Event:
        """get or create the location then save event.location"""

        # check if the location exists
        slug_form = form.slug_form.data
        obj = (
            session.query(Location).filter(Location.slug.like(f"%{slug_form}%")).first()
        )

        if obj:
            # get the existant location
            event.location = obj
            event.save(session)

            return event

        if not obj:
            # create location
            location = self._create_location(session, form)

            event.location = location
            event.save(session)

            return event

    @classmethod
    def _create(self, session, user):
        """only possible for the customer commercial
        the contract must be signed and no created event associated with the contract"""

        contract = self._get_contract(session)

        check_contract = self._check_contract(session, user, contract)
        if check_contract is False:
            return None

        form1 = View.get_event_data_to_create()
        form2 = View.get_location_data_to_create()

        if all([form1.validate(), form2.validate()]):
            event = self._create_event(session, contract, form1)
            event = self._save_location(session, event, form2)
            View.print_create_success(event)

        else:
            View.print_forms_errors(form1, form2)

    @classmethod
    def _update_event(self, session, obj: Event, form) -> Event:
        obj.start_date = form.start.data
        obj.end_date = form.end.data
        obj.attendees = form.attendees.data
        obj.note = form.note.data

        obj.save(session)

        return obj

    @classmethod
    def _update(self, session, user):
        obj = self._get_event(session)

        if not obj:
            View.print_permission_denied()

            return None

        if user.role == "Commercial" and obj.contract.customer.commercial != user:
            View.print_permission_denied()

            return None

        if user.role == "Support" and obj.support != user:
            View.print_permission_denied()

            return None

        View.print_detail(obj)

        form1 = View.get_event_data_to_update(obj)
        form2 = View.get_location_data_to_update(obj)
        if all([form1.validate(), form2.validate()]):
            obj = self._update_event(session, obj, form1)
            obj = self._save_location(session, obj, form2)
            View.print_update_success(obj)

        else:
            View.print_forms_errors(form1, form2)

    @classmethod
    def _get_support(self, session) -> Collaborator:
        obj_id = View.get_id("support")
        if obj_id != 0:
            obj = session.get(Collaborator, obj_id)

            return obj

    @classmethod
    def _change_support(self, session):
        event = self._get_event(session)
        if not event:
            View.print_permission_denied()

            return None

        support = self._get_support(session)
        if not support or support.role != "Support":
            View.print_permission_denied()

            return None

        event.support = support
        event.save(session)
        View.print_update_success(event)

    @classmethod
    def _delete(self, session, user):
        obj_id = View.get_id(View.name)

        if obj_id == 0:
            return None

        obj = session.get(Event, obj_id)

        if not obj or obj.contract.customer.commercial != user:
            View.print_permission_denied()

            return None

        View.print_detail(obj)
        choice = View.print_delete_confirm(obj)
        if choice == "o":
            obj.delete(session)
            View.print_delete_success(obj_id)
