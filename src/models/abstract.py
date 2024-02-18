from sqlalchemy import Column, DateTime, Integer, String, func

from ..utils.slugify import slugify
from . import Base
from .str_template import unfilled


class AbstractTimeField(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    creation_time = Column(DateTime, default=func.now())
    edition_time = Column(DateTime, default=func.now(), onupdate=func.now())
    slug = Column(String(255))

    @property
    def formatted_creation_time(self) -> str:
        return self.creation_time.strftime("%d/%m/%Y")

    @property
    def formatted_edition_time(self) -> str:
        return self.edition_time.strftime("%d/%m/%Y")

    def create(self, session):
        """after create, use the save method"""

        session.add(self)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()


class AbstractNameField(AbstractTimeField):
    __abstract__ = True

    name = Column(String(255), nullable=False)
    slug_name = Column(String(255))

    def __str__(self) -> str:
        return self.name.capitalize()

    def __repr__(self) -> str:
        return str(self)

    def save(self, session):
        """save slug"""

        self.slug_name = slugify(self.name)
        self.slug = f"{self.id}-{self.slug_name}"
        session.commit()


class AbstractUser(AbstractTimeField):
    __abstract__ = True

    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20))

    def __str__(self) -> str:
        first_name = self.first_name.capitalize()

        last_name = self.last_name.capitalize()

        return f"{first_name} {last_name}"

    def __repr__(self) -> str:
        return str(self)

    @property
    def name(self) -> str:
        return str(self)

    @property
    def formatted_phone(self) -> str:
        if self.phone:
            return " ".join(
                [self.phone[i : i + 2] for i in range(0, len(self.phone), 2)]
            )

        return unfilled

    @property
    def prompt_phone(self) -> str:
        if self.phone:
            return self.phone

        return ""

    @property
    def slug_first_name(self) -> str:
        return slugify(self.first_name)

    @property
    def slug_last_name(self) -> str:
        return slugify(self.last_name)

    @property
    def slug_email(self) -> str:
        return slugify(self.email)
