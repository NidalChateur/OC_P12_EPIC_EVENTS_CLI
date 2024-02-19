"""Script implementing the MVC pattern using SQLAlchemy ORM and WTForms

To activate Sentry :
1. Create a new Sentry project at https://sentry.io/ and get your 'dsn_key'
2. in the .env file, set SENTRY_DSN='dsn_key' without any quotes

"""
from src.controllers.login import Controller
from src.utils.shell import clear_shell

if __name__ == "__main__":
    clear_shell()
    Controller.run()
