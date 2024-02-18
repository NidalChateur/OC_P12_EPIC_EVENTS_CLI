import os
from pathlib import Path

from cryptography.fernet import Fernet
from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..models import Base

env_vars = dotenv_values(".env")

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def create_fernet() -> Fernet:
    if not os.path.exists(".env") or not env_vars.get("ENCRYPTION_KEY"):
        ENCRYPTION_KEY = Fernet.generate_key().decode()

        with open(".env", "w") as f:
            f.write(f"ENCRYPTION_KEY={ENCRYPTION_KEY}\nSENTRY_DSN=")

        return Fernet(ENCRYPTION_KEY.encode())

    else:
        ENCRYPTION_KEY = env_vars.get("ENCRYPTION_KEY").encode()

        return Fernet(ENCRYPTION_KEY)


fernet = create_fernet()

PUBLIC_KEY = "public_key"


def init_db(Base=Base):
    engine = create_engine("sqlite:///" + str(BASE_DIR / "db.sqlite3"))
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session


def init_test_db(Base=Base, db_name="db_test.sqlite3"):
    if os.path.exists(db_name):
        os.remove(db_name)

    engine = create_engine("sqlite:///" + str(BASE_DIR / db_name))
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session
