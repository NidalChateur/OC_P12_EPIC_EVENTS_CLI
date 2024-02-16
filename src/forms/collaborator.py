from datetime import date

from wtforms import DateField, Form, IntegerField, StringField, ValidationError
from wtforms.validators import Email, EqualTo, InputRequired, Length

from .customer import CustomerForm
from .str_template import (
    INVALID_EMAIL_MESSAGE,
    MAX_LENGTH,
    REQUIRED_MESSAGE,
    UNEQUAL_PASSWORD_MESSAGE,
)


class PasswordForm(Form):
    """used to change or create password"""

    SPECIAL_CHARACTERS = '!@#$%^&*(),.;?":{}|<>_=/+-*µ£€§¤çàùéè°'

    password = StringField(
        validators=[
            InputRequired(REQUIRED_MESSAGE),
            Length(max=255, message=MAX_LENGTH),
        ],
        label="Nouveau mot de passe",
    )

    password_confirm = StringField(
        validators=[
            InputRequired(REQUIRED_MESSAGE),
            EqualTo("password", UNEQUAL_PASSWORD_MESSAGE),
        ],
        label="Confirmation mot de passe",
    )

    # def validate_password(self, field):
    #     if len(field.data) < 8:
    #         raise ValidationError(
    #             "Votre mot de passe doit contenir au minimum 8 caractères."
    #         )
    #     if field.data.isdigit():
    #         raise ValidationError(
    #             "Votre mot de passe ne peut pas être entièrement numérique."
    #         )
    #     if field.data.isalpha():
    #         raise ValidationError(
    #             "Votre mot de passe doit contenir au moins un chiffre."
    #         )

    #     if not re.search(r"[A-Z]", field.data):
    #         raise ValidationError(
    #             "Votre mot de passe doit contenir au moins une lettre majuscule."
    #         )
    #     if not re.search(r"[a-z]", field.data):
    #         raise ValidationError(
    #             "Votre mot de passe doit contenir au moins une lettre minuscule."
    #         )

    #     if all([character in field.data for character in self.SPECIAL_CHARACTERS]):
    #         raise ValidationError(
    #             "Votre mot de passe doit contenir au moins un caractère spécial."
    #         )


class LoginForm(Form):
    email = StringField(
        validators=[InputRequired(REQUIRED_MESSAGE), Email(INVALID_EMAIL_MESSAGE)]
    )

    password = StringField(validators=[InputRequired(REQUIRED_MESSAGE)])


class FirstConnexionForm(Form):
    id = IntegerField(validators=[InputRequired(REQUIRED_MESSAGE)])

    email = StringField(
        validators=[InputRequired(REQUIRED_MESSAGE), Email(INVALID_EMAIL_MESSAGE)]
    )

    birthdate = DateField(validators=[InputRequired(REQUIRED_MESSAGE)])


class CollaboratorForm(CustomerForm):
    """Used by a Manager to CRUD Collaborator()"""

    birthdate = DateField(
        validators=[InputRequired(REQUIRED_MESSAGE)], label="Date de naissance"
    )

    def _is_minor(self, birthdate: date) -> bool:
        AGE_LIMIT = 18
        today = date.today()
        age = (
            today.year
            - birthdate.year
            - ((today.month, today.day) < (birthdate.month, birthdate.day))
        )

        return age < AGE_LIMIT

    def validate_birthdate(self, field):
        if field.data and self._is_minor(birthdate=field.data):
            raise ValidationError("Le collaborateur doit avoir au moins 18 ans.")
