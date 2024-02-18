import logging

from ..settings.settings import fernet


class Fernet:
    """encrypt and decrypt data with Fernet"""

    @staticmethod
    def encrypt(value: str) -> str:
        try:
            return fernet.encrypt(value.encode()).decode()
        except Exception as e:
            error_msg = f"encrypt error : {e}"
            print(error_msg)
            logging.exception(error_msg)

    @staticmethod
    def decrypt(value: str) -> str:
        try:
            return fernet.decrypt(value.encode()).decode()
        except Exception as e:
            error_msg = f"decrypt error : {e}"
            print(error_msg)
            logging.exception(error_msg)
