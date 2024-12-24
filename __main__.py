import builtins
import os
from typing import Optional
from tabulate import tabulate


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def input(prompt = ''):
    return builtins.input(prompt).strip()



class CommandException(Exception):
    """Class for exceptions raised by commands"""


class NotFoundErr(Exception):
    """Class for exceptions raised by search"""


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
        self.chrono = dict()
        self.show_chrono = False

        self.play()

    def play(self):
        players = self.get_players_number()
        print()

        players_names = self.get_players_names(players)
        players_list = Player.from_names(players_names)
        self.chrono = {player.name: [] for player in players_list}

        while True:
            self.sign_points(players_list)

    def get_players_number(self) -> int:
        while True:
            self.clear()
            players = input('Inserire il numero di giocatori: ')
            self.check_exit(players)
            players = self.validate_int(players)

            if players is not None and players > 1:
                return players
            elif players is not None:
                print(f"\tDevono esserci almeno 2 giocatori\n")
            else:
                print(f"\tL'input non è corretto\n")
            input()

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
                        input()
                    print()
            confirm_names = self.confirm(f'I nomi dei giocatori sono {", ".join(player_list)}, va bene così?')

        return player_list

    def sign_points(self, players: list[Player]):
        self.clear()
        if self.show_chrono:
            self.print_chrono()

        print('Punti')
        Player.print(players)

        command = input('> ')

        self.check_exit(command)

        if self.toggle(command):
            return

        addiction = self.validate_addiction(command)

        if addiction:
            name, number = addiction

            try:
                player = Player.search(name, players)
                self.update_chrono(player, number)
            except NotFoundErr as e:
                print(e)
                input()
                return

            player.add(number)
        else:
            print(f'\t"{command}" non è un comando valido')
            input()

    def print_chrono(self):
        print("\nCronologia Punti")
        max_turns = max(len(points) for points in self.chrono.values())
        rows = [[self.chrono[player][i] if i < len(self.chrono[player]) else '' for player in self.chrono] for i in range(max_turns)]
        table = [[i+1] + row for i, row in enumerate(rows)]
        print(tabulate(table, headers=["Turni"] + list(self.chrono.keys()), tablefmt="fancy_grid"))
        print()


    def update_chrono(self, player: Player, number: int):
        if number > 0:
            self.chrono[player.name].append(number)
        elif number < 0:
            self.chrono[player.name][-1] += number

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
            cmd, prop = command.split(' ', 1)

            if cmd in self.toggle_words:
                if prop in self.chrono_words:
                    self.show_chrono = cmd == self.toggle_words[0]  # True se "mostra", False se "nascondi"
                    print(f"\t{'Attivo' if self.show_chrono else 'Disattivo'} la cronologia...", end=' ')
                    input()
                    return True
                else:
                    raise CommandException(f'"{prop}" non è un comando valido')
            return False
        except ValueError:
            return False
        except CommandException as e:
            print(f"\t{e}")
            input()
            return True


if __name__ == '__main__':
    try:
        Game()
    except KeyboardInterrupt:
        print('\nEsecuzione Terminata\n')
