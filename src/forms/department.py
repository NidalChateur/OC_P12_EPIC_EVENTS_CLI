from wtforms import Form, StringField, ValidationError
from wtforms.validators import InputRequired, Length

from .str_template import MAX_LENGTH, REQUIRED_MESSAGE


class DepartmentForm(Form):
    """Used by a Manager to CRUD Department()"""

    name = StringField(
        validators=[
            InputRequired(REQUIRED_MESSAGE),
            Length(max=255, message=MAX_LENGTH),
        ],
        label="Nom du département",
    )

    def validate_name(self, field):
        name = field.data
        choices = ["Gestion", "Commercial", "Support"]
        if name not in choices:
            raise ValidationError(f"Le nom du département doit être : {choices} ")
