from datetime import datetime, timedelta


def session_is_expired(user) -> bool:
    """used to disconnect the user after 12 hours"""

    if datetime.utcnow() > user.last_login + timedelta(hours=12):
        return True
