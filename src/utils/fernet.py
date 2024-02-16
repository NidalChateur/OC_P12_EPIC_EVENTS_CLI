from ..settings.settings import fernet


class Fernet:
    """encrypt and decrypt data with Fernet"""

    @staticmethod
    def encrypt(value: str) -> str:
        try:
            return fernet.encrypt(value.encode()).decode()
        except Exception as e:
            print(f"encrypt error : {e}")

    @staticmethod
    def decrypt(value: str) -> str:
        try:
            return fernet.decrypt(value.encode()).decode()
        except Exception as e:
            print(f"decrypt error : {e}")
