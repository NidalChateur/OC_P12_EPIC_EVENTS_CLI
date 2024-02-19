from datetime import datetime

import bcrypt
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.utils.fernet import Fernet

from .abstract import AbstractUser
from .contract_event import Event
from .customer import Customer
from .str_template import unfilled


class Collaborator(AbstractUser):
    __tablename__ = "collaborator"

    FRENCH_NAME = "collaborateur"

    department_id = Column(Integer, ForeignKey("department.id"))
    department = relationship("Department", back_populates="collaborators")

    birthdate = Column(Date, nullable=False)
    password = Column(String(255))
    last_login = Column(DateTime)

    # child relations
    customers = relationship(Customer, back_populates="commercial")
    events = relationship(Event, back_populates="support")

    @property
    def prompt_department(self) -> str:
        if self.department:
            return str(self.department)

        return ""

    @property
    def role(self) -> str:
        if self.department:
            return str(self.department)

        return unfilled

    @property
    def title(self) -> str:
        return f"{self.role} {self.first_name.capitalize()}"

    @property
    def formatted_birthdate(self) -> str:
        return self.birthdate.strftime("%d/%m/%Y")

    @property
    def prompt_birthdate(self) -> str:
        return self.birthdate.strftime("%Y-%m-%d")

    @property
    def _slug_role(self) -> str:
        if self.department:
            return self.department.slug_name

        return ""

    @classmethod
    def _hash_password(self, value_to_hash) -> bytes:
        salt = bcrypt.gensalt()

        return bcrypt.hashpw(value_to_hash.encode("utf-8"), salt)

    def set_password(self, password: str):
        self.password = self._hash_password(password)

    @classmethod
    def get_with_clear_email(self, session, email: str):
        collaborators = session.query(Collaborator).all()
        for collaborator in collaborators:
            collaborator_email = Fernet.decrypt(collaborator.email)
            if collaborator_email == email:
                return collaborator

    @classmethod
    def check_password(self, password: str, hashed_password: bytes) -> bool:
        if hashed_password and password:
            return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

        return False

    @classmethod
    def authenticate(self, session, email: str, password: str):
        collaborator = self.get_with_clear_email(session, email)
        if collaborator and self.check_password(password, collaborator.password):
            collaborator.last_login = datetime.utcnow()
            session.commit()

            return collaborator

    def create(self, session):
        """after create, use the save method to save slug"""

        session.add(self)
        session.commit()

    def save(self, session):
        """save slug"""

        slug_role = self._slug_role
        self.slug = (
            f"{self.id}-{self.slug_first_name}-{self.slug_last_name}-{slug_role}"
        )

        session.commit()
