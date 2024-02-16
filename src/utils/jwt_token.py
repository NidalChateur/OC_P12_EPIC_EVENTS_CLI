from datetime import datetime, timedelta

import jwt

from ..models.collaborator import Collaborator
from ..settings.settings import ENCRYPTION_KEY, PUBLIC_KEY


class JwtToken:
    @staticmethod
    def generate(collaborator, session) -> str:
        payload = {
            "id": collaborator.id,
            "role": collaborator.role(session),
            "exp": datetime.utcnow() + timedelta(days=1),
        }
        jwt_token = jwt.encode(payload, ENCRYPTION_KEY, algorithm="HS256")

        return jwt_token

    @staticmethod
    def check(jwt_token, session) -> Collaborator:
        """check if the jwt token is valid:
        return the collaborator instance if the token is valid
        return False if the token is invalid"""

        try:
            payload = jwt.decode(jwt_token, PUBLIC_KEY, algorithms=["HS256"])
            collaborator = session.get(Collaborator, payload.get("id"))

            return collaborator

        except jwt.ExpiredSignatureError:
            return False

        except jwt.InvalidTokenError:
            return False
