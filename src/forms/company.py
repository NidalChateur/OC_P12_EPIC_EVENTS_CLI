from wtforms import Form, StringField
from wtforms.validators import InputRequired, Length

from .str_template import MAX_LENGTH, REQUIRED_MESSAGE


class CompanyForm(Form):
    """Used by a Commercial to CRUD customer Company()"""

    name = StringField(
        validators=[
            InputRequired(REQUIRED_MESSAGE),
            Length(max=255, message=MAX_LENGTH),
        ],
        label="Nom de l'entreprise",
    )
