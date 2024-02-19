import os


def clear_shell():
    if os.name == "posix":  # Unix/Linux
        os.system("clear")
    if os.name == "nt":  # Windows
        os.system("cls")
