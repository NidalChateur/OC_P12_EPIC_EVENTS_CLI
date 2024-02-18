from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from ..utils.fernet import Fernet
from .abstract import AbstractTimeField, slugify
from .location import Location
from .str_template import no, unfilled, yes


class Contract(AbstractTimeField):
    __tablename__ = "contract"

    FRENCH_NAME = "contrat"

    customer_id = Column(
        Integer, ForeignKey("customer.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    customer = relationship("Customer", back_populates="contracts")

    total_amount = Column(Integer, default=0, nullable=False)
    paid_amount = Column(Integer, default=0, nullable=False)
    is_signed = Column(Boolean, default=False, nullable=False)

    # child relation
    events = relationship(
        "Event", back_populates="contract", cascade="all, delete-orphan"
    )

    @property
    def prompt_is_signed(self) -> str:
        if self.is_signed:
            return "oui"

        return "non"

    @property
    def formatted_is_signed(self) -> str:
        if self.is_signed:
            return yes

        return no

    @property
    def is_paid(self) -> bool:
        return self.total_amount - self.paid_amount == 0

    @property
    def formatted_is_paid(self) -> str:
        if self.is_paid:
            return yes

        return no

    @property
    def remaining_amount(self) -> float:
        return self.total_amount - self.paid_amount

    @property
    def formatted_paid_amount(self) -> str:
        return "{:,}".format(self.paid_amount).replace(",", " ")

    @property
    def formatted_total_amount(self) -> str:
        return "{:,}".format(self.total_amount).replace(",", " ")

    @property
    def formatted_remaining_amount(self) -> str:
        return "{:,}".format(self.remaining_amount).replace(",", " ")

    @property
    def customer_name(self) -> str:
        if self.customer:
            return self.customer.name

        return unfilled

    @property
    def customer_email(self) -> str:
        if self.customer:
            return self.customer.email

        return unfilled

    @property
    def customer_phone(self) -> str:
        if self.customer:
            return self.customer.formatted_phone

        return unfilled

    @property
    def commercial_name(self) -> str:
        if self.customer.commercial:
            return self.customer.commercial.name

        return unfilled

    @property
    def commercial_email(self) -> str:
        if self.customer.commercial:
            return Fernet.decrypt(self.customer.commercial.email)

        return unfilled

    @property
    def commercial_phone(self) -> str:
        if self.customer.commercial:
            return self.customer.commercial.formatted_phone

        return unfilled

    def is_ready_for_event(self, session) -> bool:
        """check if the contract is signed and if there is no event for this contract"""

        event = session.query(Event).filter_by(contract=self).first()
        if self.is_signed and not event:
            return True

        return False

    def save(self, session):
        """save slug"""

        if self.customer:
            slug_customer = slugify(self.customer_name)
        else:
            slug_customer = ""

        if self.customer and self.customer.commercial:
            slug_commercial = slugify(self.commercial_name)
        else:
            slug_commercial = ""

        self.slug = slugify(
            f"{self.id} {slug_customer} {slug_commercial} {self.total_amount}"
        )
        session.commit()


class Event(AbstractTimeField):
    __tablename__ = "event"

    FRENCH_NAME = "événement"

    contract_id = Column(
        Integer, ForeignKey("contract.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    contract = relationship(Contract, back_populates="events")

    location_id = Column(Integer, ForeignKey("location.id"))
    location = relationship(Location, back_populates="events")

    support_id = Column(Integer, ForeignKey("collaborator.id"))
    support = relationship("Collaborator", back_populates="events")

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    attendees = Column(Integer, default=0, nullable=False)
    note = Column(Text)

    @property
    def formatted_start_date(self) -> str:
        return self.start_date.strftime("%d/%m/%Y à %H:%M")

    @property
    def prompt_start_date(self) -> str:
        return self.start_date.strftime("%Y-%m-%d")

    @property
    def prompt_start_time(self) -> str:
        return self.start_date.strftime("%H:%M")

    @property
    def formatted_end_date(self) -> str:
        return self.end_date.strftime("%d/%m/%Y à %H:%M")

    @property
    def prompt_end_date(self) -> str:
        return self.end_date.strftime("%Y-%m-%d")

    @property
    def prompt_end_time(self) -> str:
        return self.end_date.strftime("%H:%M")

    @property
    def address(self) -> str:
        if self.location:
            return str(self.location)

        return unfilled

    @property
    def customer_name(self) -> str:
        if self.contract:
            return self.contract.customer_name

        return unfilled

    @property
    def customer_email(self) -> str:
        if self.contract:
            return self.contract.customer_email

        return unfilled

    @property
    def customer_phone(self) -> str:
        if self.contract:
            return self.contract.customer_phone

        return unfilled

    @property
    def commercial_name(self):
        if self.contract:
            return self.contract.commercial_name

        return unfilled

    @property
    def commercial_email(self):
        if self.contract:
            return self.contract.commercial_email

        return unfilled

    @property
    def commercial_phone(self):
        if self.contract:
            return self.contract.commercial_phone

        return unfilled

    @property
    def support_name(self):
        if self.support:
            return self.support.name

        return unfilled

    @property
    def support_email(self):
        if self.support:
            return self.support.email

        return unfilled

    @property
    def support_phone(self):
        if self.support:
            return self.support.formatted_phone

        return unfilled

    def save(self, session):
        """save slug"""

        customer_name = slugify(self.customer_name)
        commercial_name = slugify(self.commercial_name)
        support_name = slugify(self.support_name)

        if self.contract:
            contract_id = self.contract.id
        else:
            contract_id = ""

        slug = slugify(
            f"{self.id} {contract_id} {customer_name} {commercial_name} {support_name}"
        )
        self.slug = slug

        session.commit()
