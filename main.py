"""Script implementing the MVC pattern using SQLAlchemy ORM and WTForms

To activate Sentry :
1. Create a new Sentry project at https://sentry.io/ and get your dsn_key
2. in the .env file, replace 'DEBUG=True' by 'SENTRY=dsn_key'

"""

from src.controllers.login import Controller

if __name__ == "__main__":
    Controller.clear_shell()
    Controller.run()
