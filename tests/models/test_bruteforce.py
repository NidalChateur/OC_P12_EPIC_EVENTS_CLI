from datetime import datetime, timedelta

from src.models.bruteforce import BruteForce
from src.models.collaborator import Collaborator
from tests import MixinSetup


class TestBruteForce(MixinSetup):
    def test_create_save(self):
        self.clear_db()
        assert len(self.session.query(BruteForce).all()) == 0

        bruteforce = BruteForce()
        bruteforce.create(self.session)

        assert len(self.session.query(BruteForce).all()) == 1
        bruteforce = self.session.get(BruteForce, 1)
        assert bruteforce.attempts == 0
        assert bruteforce.timestamp < datetime.utcnow() + timedelta(minutes=1)

        bruteforce.attempts += 1
        bruteforce._save(self.session)
        assert self.session.get(BruteForce, 1).attempts == 1

    def test_save_anonymous_data(self):
        self.clear_db()
        BruteForce.save_data(self.session, user=None)

        # getting anonymous brute force data
        anonymous_bruteforce_data = (
            self.session.query(BruteForce).filter_by(user=None).first()
        )

        # test anonymous bruteforce data
        assert anonymous_bruteforce_data is not None
        assert anonymous_bruteforce_data.user is None
        assert anonymous_bruteforce_data.attempts == 1
        timestamp = anonymous_bruteforce_data.timestamp
        assert timestamp < datetime.utcnow() + timedelta(minutes=1)

    def test_save_user_data(self):
        user = self.create_collaborator("Gestion")
        BruteForce.save_data(self.session, user)

        # getting user brute force data
        user_bruteforce_data = (
            self.session.query(BruteForce).filter_by(user=user).first()
        )

        # test user bruteforce data
        assert user_bruteforce_data is not None
        assert user_bruteforce_data.user == user
        assert user_bruteforce_data.attempts == 1
        timestamp = user_bruteforce_data.timestamp
        assert timestamp < datetime.utcnow() + timedelta(minutes=1)

    def test_reset_data(self):
        # get and test that bruteforce.attempts != 0
        anonymous_bruteforce = (
            self.session.query(BruteForce).filter_by(user=None).first()
        )

        assert anonymous_bruteforce
        assert anonymous_bruteforce.attempts > 0

        user = self.session.get(Collaborator, 1)
        user_bruteforce = self.session.query(BruteForce).filter_by(user=user).first()

        assert user_bruteforce
        assert user_bruteforce.attempts > 0

        BruteForce.reset_data(self.session, user)

        # get and test that bruteforce.attempts == 0
        anonymous_bruteforce = (
            self.session.query(BruteForce).filter_by(user=None).first()
        )

        assert anonymous_bruteforce
        assert anonymous_bruteforce.attempts == 0

        user_bruteforce = self.session.query(BruteForce).filter_by(user=user).first()

        assert user_bruteforce
        assert user_bruteforce.attempts == 0

    def test_anonymous_attempts_bruteforce(self):
        """when an unknown email is entered"""

        self.clear_db()
        # test with no data, BruteForce.attack_is_detected must be False
        assert BruteForce.attack_is_detected(self.session, user=None) is False

        # setup bruteforce data, BruteForce.attack_is_detected must be True
        anonymous_bruteforce = (
            self.session.query(BruteForce).filter_by(user=None).first()
        )
        anonymous_bruteforce.attempts += 3
        anonymous_bruteforce.timestamp = datetime.utcnow()

        assert BruteForce.attack_is_detected(self.session, user=None) is True

    def test_user_attempts_bruteforce(self):
        """when a known email is entered"""

        self.clear_db()
        # test with no data, BruteForce.attack_is_detected must be False
        user = self.create_collaborator("Gestion")
        assert BruteForce.attack_is_detected(self.session, user=user) is False

        # setup bruteforce data, BruteForce.attack_is_detected must be True
        user_bruteforce = self.session.query(BruteForce).filter_by(user=user).first()
        user_bruteforce.attempts += 3
        user_bruteforce.timestamp = datetime.utcnow()

        assert BruteForce.attack_is_detected(self.session, user=user) is True
