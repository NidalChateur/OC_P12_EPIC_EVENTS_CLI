from sqlalchemy.orm import relationship

from .abstract import AbstractNameField


class Department(AbstractNameField):
    __tablename__ = "department"

    FRENCH_NAME = "département"

    # child relation
    collaborators = relationship("Collaborator", back_populates="department")
