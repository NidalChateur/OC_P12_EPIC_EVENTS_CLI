from wtforms import Form, StringField
from wtforms.validators import InputRequired, Length

from ..utils.slugify import slugify
from .str_template import MAX_LENGTH, REQUIRED_MESSAGE


class LocationForm(Form):
    """Used by a Commercial to CRUD Event()"""

    name = StringField(
        validators=[Length(max=255, message=MAX_LENGTH)], label="Nom du lieu"
    )

    number = StringField(
        validators=[Length(max=255, message=MAX_LENGTH)], label="Numéro"
    )

    street_type = StringField(
        validators=[Length(max=255, message=MAX_LENGTH)], label="Type de voie"
    )

    street_name = StringField(
        validators=[Length(max=255, message=MAX_LENGTH)], label="Nom de voie"
    )

    zip_code = StringField(
        validators=[
            Length(max=5, message="Ce champ ne peut pas dépasser 5 caractères."),
            InputRequired(REQUIRED_MESSAGE),
        ],
        label="Code postal",
    )

    city = StringField(
        validators=[
            Length(max=255, message=MAX_LENGTH),
            InputRequired(REQUIRED_MESSAGE),
        ],
        label="Ville",
    )

    slug_form = StringField(validators=[Length(max=255, message=MAX_LENGTH)])

    def validate(self) -> bool:
        initial_validation = super(LocationForm, self).validate()
        if not initial_validation:
            return False

        if self.zip_code.data and not self.zip_code.data.isdigit():
            self.zip_code.errors.append(
                "Le code postal doit être composé de 5 chiffres."
            )

            return False

        if self.name.data:
            name = self.name.data
        else:
            name = ""

        if self.number.data:
            number = self.number.data
        else:
            number = ""

        if self.street_type.data:
            street_type = self.street_type.data
        else:
            street_type = ""

        if self.street_name.data:
            street_name = self.street_name.data
        else:
            street_name = ""

        city = self.city.data

        zip_code = self.zip_code.data

        self.slug_form.data = slugify(
            f"{name} {number} {street_type} {street_name} {zip_code} {city}".strip()
        )

        return True
