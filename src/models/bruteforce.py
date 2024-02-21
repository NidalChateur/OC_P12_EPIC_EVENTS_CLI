from datetime import datetime, timedelta

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .abstract import AbstractTimeField


class BruteForce(AbstractTimeField):
    """allow to avoid brute forces attacks :

    An anonymous attempt occurs when an unknown email is entered in the login view.
    A user attempt occurs when a known email is entered in the login view."""

    __tablename__ = "bruteforce"

    user_id = Column(Integer, ForeignKey("collaborator.id"))
    user = relationship("Collaborator", back_populates="bruteforces")

    attempts = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow())

    # methods to get brute force data
    @classmethod
    def _get_or_create_user_data(self, session, user):
        """brute force data assigned to a user"""

        user_bruteforce = session.query(BruteForce).filter_by(user=user).first()
        if user_bruteforce:
            # get bruteforce data

            return user_bruteforce

        else:
            # create bruteforce data
            user_bruteforce = BruteForce(user=user)
            user_bruteforce.create(session)

            return user_bruteforce

    @classmethod
    def _get_or_create_anonymous_data(self, session):
        """brute force data not assigned to a user"""

        anonymous_bruteforce = session.query(BruteForce).filter_by(user=None).first()
        if anonymous_bruteforce:
            return anonymous_bruteforce

        else:
            anonymous_bruteforce = BruteForce()
            anonymous_bruteforce.create(session)

            return anonymous_bruteforce

    # methods to update brute force data
    @classmethod
    def reset_data(self, session, user):
        """used when a user is authenticated with success"""

        user_bruteforce = self._get_or_create_user_data(session, user)
        user_bruteforce.attempts = 0
        user_bruteforce._save(session)

        anonymous_bruteforce = self._get_or_create_anonymous_data(session)
        anonymous_bruteforce.attempts = 0
        anonymous_bruteforce._save(session)

    @classmethod
    def save_data(self, session, user):
        if user:
            # case where the user email exists
            bruteforce = self._get_or_create_user_data(session, user)

        else:
            # case where the user email does not exist
            bruteforce = self._get_or_create_anonymous_data(session)

        bruteforce.attempts += 1
        bruteforce.timestamp = datetime.utcnow()
        bruteforce._save(session)

    def _save(self, session):
        session.commit()

    # methods to detect brute force attacks
    @classmethod
    def _check_bruteforce_data(self, bruteforce, delta_in_mn: int) -> bool:
        """check the bruteforce attack conditions:
        - bruteforce.attempts must be >= 3
            and
        - now < bruteforce.timestamp + delta_in_mn

        return True if the data suggests a brute force attack
        return False if the data does not suggest a brute force attack
        """

        now = datetime.utcnow()
        time_condition = now < bruteforce.timestamp + timedelta(minutes=delta_in_mn)

        if bruteforce.attempts >= 3 and time_condition:
            return True
        else:
            False

    @classmethod
    def _anonymous_attempts_bruteforce(self, session, delta_in_mn=3) -> bool:
        """return True if the brute force data suggests an attack from an unknown user email
        else return False"""

        bruteforce = self._get_or_create_anonymous_data(session)

        return self._check_bruteforce_data(bruteforce, delta_in_mn=delta_in_mn)

    @classmethod
    def _user_attempts_bruteforce(self, session, user, delta_in_mn=3) -> bool:
        """return True if the brute force data suggests an attack from a known user email
        else return False"""

        bruteforce = self._get_or_create_user_data(session, user)

        return self._check_bruteforce_data(bruteforce, delta_in_mn=delta_in_mn)

    @classmethod
    def attack_is_detected(self, session, user) -> bool:
        """return True if brute force data suggests an attack"""

        if self._anonymous_attempts_bruteforce(session):
            return True

        if self._user_attempts_bruteforce(session, user):
            return True

        return False
