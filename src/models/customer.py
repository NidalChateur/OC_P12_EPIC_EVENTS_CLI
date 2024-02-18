from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .abstract import AbstractUser, slugify
from .company import Company
from .contract_event import Contract
from .str_template import unfilled


class Customer(AbstractUser):
    __tablename__ = "customer"

    FRENCH_NAME = "client"

    company_id = Column(Integer, ForeignKey("company.id"))
    company = relationship(Company, back_populates="customers")

    commercial_id = Column(
        Integer, ForeignKey("collaborator.id", ondelete="SET NULL", onupdate="CASCADE")
    )
    commercial = relationship("Collaborator", back_populates="customers")

    # child relation
    contracts = relationship(
        Contract, back_populates="customer", cascade="all, delete-orphan"
    )

    @property
    def prompt_company_name(self) -> str:
        if self.company:
            return str(self.company)

        return ""

    @property
    def company_name(self) -> str:
        if self.company:
            return str(self.company)

        return unfilled

    @property
    def commercial_name(self) -> str:
        if self.commercial:
            return self.commercial.name

        return unfilled

    @property
    def slug_commercial_name(self) -> str:
        if self.commercial:
            return slugify(self.commercial.name)

        return ""

    def save(self, session):
        """save slug"""

        slug_company = slugify(self.prompt_company_name)
        slug_commercial = self.slug_commercial_name
        self.slug = f"{self.id}-{self.slug_first_name}-{self.slug_last_name}-{slug_company}-{slug_commercial}"

        session.commit()
