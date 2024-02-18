from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .abstract import AbstractTimeField, slugify
from .str_template import unfilled


class Location(AbstractTimeField):
    __tablename__ = "location"

    FRENCH_NAME = "lieu"

    events = relationship("Event", back_populates="location")

    name = Column(String(255))
    number = Column(String(255))
    street_type = Column(String(255))
    street_name = Column(String(255))
    zip_code = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)

    def __str__(self, name=True) -> str:
        if self.name and name:
            name = f"{self.name.title()}, "
        else:
            name = ""

        if self.number:
            number = f"{self.number.upper()} "
        else:
            number = ""

        if self.street_type:
            street_type = f"{self.street_type.capitalize()} "
        else:
            street_type = ""

        if self.street_name:
            street_name = f"{self.street_name.title()}, "
        else:
            street_name = ""

        zip_code = f"{self.zip_code} "

        city = f"{self.city.title()}"

        return f"{name}{number}{street_type}{street_name}{zip_code}{city}"

    @property
    def formatted_name(self) -> str:
        if self.name:
            return self.name.title()

        return unfilled

    @property
    def formatted_address(self) -> str:
        return self.__str__(name=False)

    def save(self, session):
        self.slug = f"{self.id}-{slugify(str(self))}"
        session.commit()
