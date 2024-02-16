from wtforms import BooleanField, Form, IntegerField
from wtforms.validators import InputRequired

from .str_template import (
    REQUIRED_MESSAGE,
)


class ContractForm(Form):
    """user by Gestion or customer Commercial"""

    total_amount = IntegerField(
        validators=[InputRequired(REQUIRED_MESSAGE)], label="Montant total"
    )

    paid_amount = IntegerField(
        validators=[InputRequired(REQUIRED_MESSAGE)], label="Montant payé"
    )

    is_signed = BooleanField(label="Signature")

    def validate(self) -> bool:
        """multi field validator : check if total_amount > paid_amount"""

        initial_validation = super(ContractForm, self).validate()
        if not initial_validation:
            return False

        if self.total_amount.data < self.paid_amount.data:
            self.paid_amount.errors.append(
                "Le montant payé par le client ne peut pas excéder le montant total."
            )

            return False

        return True
