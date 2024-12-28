import builtins
import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def input(prompt=''):
    return builtins.input(prompt).strip()
