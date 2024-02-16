from sqlalchemy.orm import relationship

from .abstract import AbstractNameField


class Company(AbstractNameField):
    __tablename__ = "company"

    FRENCH_NAME = "entreprise"

    # child relation
    customers = relationship("Customer", back_populates="company")
