from tabulate import tabulate

from src.exceptions import NotFoundErr


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
