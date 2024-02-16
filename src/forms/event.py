from datetime import datetime

from wtforms import (
    DateField,
    DateTimeField,
    Form,
    IntegerField,
    TextAreaField,
    TimeField,
)
from wtforms.validators import InputRequired, Length

from .str_template import REQUIRED_MESSAGE


class EventForm(Form):
    """Used by a Commercial to CRUD Event()"""

    start_date = DateField(
        validators=[InputRequired(REQUIRED_MESSAGE)], label="Date de début"
    )
    start_time = TimeField(
        validators=[InputRequired(REQUIRED_MESSAGE)], label="Heure de début"
    )

    end_date = DateField(
        validators=[InputRequired(REQUIRED_MESSAGE)], label="Date de fin"
    )
    end_time = TimeField(
        validators=[InputRequired(REQUIRED_MESSAGE)], label="Heure de fin"
    )

    attendees = IntegerField(
        validators=[InputRequired(REQUIRED_MESSAGE)], label="Nombre de participant"
    )

    note = TextAreaField(
        validators=[
            Length(max=2000, message="Ce champ ne peut pas dépasser 2000 caractères.")
        ],
        label="Note",
    )

    # filled by the validator
    start = DateTimeField()
    end = DateTimeField()

    def validate(self) -> bool:
        initial_validation = super(EventForm, self).validate()
        if not initial_validation:
            return False

        start = datetime.combine(self.start_date.data, self.start_time.data)

        end = datetime.combine(self.end_date.data, self.end_time.data)

        if start >= end:
            error_message = "La date et l'heure de fin doivent avoir lieu après la date et l'heure de début."
            self.start_date.errors.append(error_message)
            self.start_time.errors.append(error_message)

            return False

        self.start.data = start
        self.end.data = end

        return True
