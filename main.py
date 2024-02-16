"""Script implementing the MVC pattern using SQL_Alchemy ORM and Django Forms"""

from src.controllers.login import Controller

if __name__ == "__main__":
    Controller.clear_shell()
    Controller.run()
