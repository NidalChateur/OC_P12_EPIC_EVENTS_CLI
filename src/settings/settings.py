from pathlib import Path

from cryptography.fernet import Fernet
from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..models import Base

env_vars = dotenv_values(".env")

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# If the db is empty, an user Gestion is created
ADMIN_EMAIL = env_vars.get("ADMIN_EMAIL")
ADMIN_PASSWORD = env_vars.get("ADMIN_PASSWORD")

# Fernet.generate_key() to generate an ENCRYPTION_KEY

# ENCRYPTION_KEY = b"cU6la5-GP1WV59YRt9rrId9hEVmE7rWIhdJcPf_Ee3s="
ENCRYPTION_KEY = env_vars.get("ENCRYPTION_KEY").encode()
fernet = Fernet(ENCRYPTION_KEY)

PUBLIC_KEY = "public_key"


def init_db(Base=Base):
    engine = create_engine("sqlite:///" + str(BASE_DIR / "db.sqlite3"))
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session
