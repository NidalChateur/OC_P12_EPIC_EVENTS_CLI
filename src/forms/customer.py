from wtforms import Form, StringField, ValidationError
from wtforms.validators import Email, InputRequired, Length

from .str_template import INVALID_EMAIL_MESSAGE, MAX_LENGTH, REQUIRED_MESSAGE


class CustomerForm(Form):
    """Used by a Commercial to CRUD Customer()"""

    first_name = StringField(
        validators=[
            InputRequired(REQUIRED_MESSAGE),
            Length(max=255, message=MAX_LENGTH),
        ],
        label="Prénom",
    )

    last_name = StringField(
        validators=[
            InputRequired(REQUIRED_MESSAGE),
            Length(max=255, message=MAX_LENGTH),
        ],
        label="Nom",
    )

    email = StringField(
        validators=[
            InputRequired(REQUIRED_MESSAGE),
            Email(INVALID_EMAIL_MESSAGE),
            Length(max=255, message=MAX_LENGTH),
        ]
    )

    phone = StringField(
        validators=[
            Length(max=20, message="Ce champ ne peut pas dépasser 20 caractères.")
        ],
        label="Téléphone",
    )

    def validate_phone(self, field):
        if field.data and not field.data.isdigit():
            raise ValidationError(
                "Le numéro de téléphone doit être composé uniquement de chiffre."
            )

        if field.data and field.data[0] != "0":
            raise ValidationError("Le numéro de téléphone doit commencer par 0")

        if field.data and len(field.data) < 10:
            raise ValidationError(
                "Le numéro de téléphone doit comporter au moins 10 chiffres."
            )
