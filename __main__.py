import os
from typing import Optional
from xml.dom import NotFoundErr
from tabulate import tabulate


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


class CommandException(Exception):
    """Class for exceptions raised by commands"""


class Player:
    def __init__(self, name):
        self.name = name
        self.point = 0

    def __repr__(self):
        return f'Player<{self.name}>'

    @classmethod
    def from_names(cls, names: list[str]) -> list['Player']:
        return [cls(name) for name in names]

    def add(self, amount):
        if self.point + amount >= 0:
            self.point += amount
        else:
            self.point = 0

    @classmethod
    def names(cls, players: list['Player']):
        return [player.name for player in players]

    @classmethod
    def print(cls, players: list['Player']):
        # names = cls.names(players)
        # maxln = max([len(name) for name in names]) + 1
        # print(''.join([f'%-{maxln}s' % name for name in names]))
        # print(''.join([f'%-{maxln}s' % player.point for player in players]))
        table = [[player.name, player.point] for player in players]
        print(tabulate(table, headers=["Giocatore", "Punti"], tablefmt="fancy_grid"))
        print()

    @classmethod
    def search(cls, name, players: list['Player']) -> 'Player':
        names = cls.names(players)
        for i in range(len(names)):
            if names[i].lower().startswith(name):
                return players[i]

        raise NotFoundErr(f'"{name}" non corrisponde alle iniziali di nessun giocatore')


class Game:
    exit_words = ['exit', 'quit', 'esci']
    toggle_words = ['mostra', 'nascondi']
    chrono_words = ['crono', 'cronologia']

    @classmethod
    def get_reserved_words(cls):
        lists = [cls.exit_words, cls.toggle_words, cls.chrono_words]
        return [word for sublist in lists for word in sublist]

    def __init__(self):
        self.show_chrono = False

        self.play()

    def play(self):
        players = self.get_players_number()
        print()

        players_names = self.get_players_names(players)
        players_list = Player.from_names(players_names)

        while True:
            self.sign_points(players_list)

    def get_players_number(self) -> int:
        while True:
            self.clear()
            players = input('Inserire il numero di giocatori: ')
            self.check_exit(players)
            players = self.validate_int(players)
            if players:
                return players
            print(f"\tL'input non è corretto\n")

    def get_players_names(self, players: int) -> list[str]:
        confirm_names = False  # Inserimento nomi giocatori
        player_list = []

        while not confirm_names:
            self.clear()
            player_list = []
            for i in range(players):
                while True:
                    try:
                        name = input(f"Inserisci il nome del giocatore {i + 1}: ")
                        self.check_exit(name)
                        player_list.append(self.validate_name(name).capitalize())
                        break
                    except Exception as e:
                        print(f"\t{e}")
                    print()
            confirm_names = self.confirm(f'I nomi dei giocatori sono {", ".join(player_list)}, va bene così?')

        return player_list

    def sign_points(self, players: list[Player]):
        self.clear()
        Player.print(players)

        command = input('> ')

        self.check_exit(command)

        if self.toggle(command, players):
            return

        addiction = self.validate_addiction(command)

        if command:
            name, number = addiction

            try:
                player = Player.search(name, players)
            except NotFoundErr as e:
                print(e)
                return

            player.add(number)
        else:
            print(f'"{command}" non Ã¨ un comando valido')

    @staticmethod
    def validate_int(value) -> Optional[int]:
        try:
            return int(value)
        except:
            return None

    @classmethod
    def validate_name(cls, name) -> Optional[str]:
        if name in cls.get_reserved_words():
            raise ValueError(f'"{name}" è una parola riservata')
        elif not name.isalpha():
            raise ValueError(f'"{name}" non è un nome valido')

        return name

    @staticmethod
    def confirm(prompt):
        return input(prompt + ' (Y/n): ').lower() == 'y'

    @staticmethod
    def clear():
        clear()  # Titolo
        print('SCARABEO\n')

    @classmethod
    def validate_addiction(cls, command):
        try:
            sw, number = command.split(' ')
            return sw, int(number)
        except:
            return None

    @classmethod
    def check_exit(cls, command):
        if command in cls.exit_words:
            raise KeyboardInterrupt

    def toggle(self, command: str) -> bool:
        try:
            command, prop = command.split(' ')

            if command in self.toggle_words:
                if prop in self.chrono_words:
                    self.show_chrono = command == self.toggle_words[0]
                else:
                    raise CommandException(f'"{prop}" non è un comando valido')
                return True
            return False

        except ValueError:
            return False


if __name__ == '__main__':
    try:
        Game()
    except KeyboardInterrupt:
        print('\nEsecuzione Terminata\n')
