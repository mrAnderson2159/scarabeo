from os import system


def clear():
    system('clear')


class Player:
    def __init__(self, name):
        self.name = name
        self.point = 0

    def __repr__(self):
        return f'Player<{self.name}>'

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
        names = cls.names(players)
        maxln = max([len(name) for name in names]) + 1
        print(''.join([f'%-{maxln}s' % name for name in names]))
        print(''.join([f'%-{maxln}s' % player.point for player in players]))
        print()

    @classmethod
    def search(cls, name, players: list['Player']):
        names = cls.names(players)
        for i in range(len(names)):
            if names[i].lower().startswith(name):
                return players[i]
        return None


class Game:
    def __init__(self):
        while True:  # Inserimento numero giocatori
            self.clear()
            players = input('Inserire il numero di giocatori: ')
            players = self.validate_int(players)
            if players:
                break
            print(f"\tL'input non Ã¨ corretto\n")
        print()

        confirm_names = False  # Inserimento nomi giocatori

        while not confirm_names:
            self.clear()
            player_list = []
            for i in range(players):
                player_list.append(
                    input(f"Inserisci il nome del giocatore {i + 1}: ").capitalize()
                )
                print()
            confirm_names = self.confirm(f'I nomi dei giocatori sono {", ".join(player_list)}, va bene cosÃ¬?')

        player_list = list(map(lambda p: Player(p), player_list))

        while True:
            self.sign_points(player_list)

    def sign_points(self, players):
        self.clear()
        Player.print(players)
        command = self.validate_command(input('> '))

        if command:
            name, number = command

            try:
                player = Player.search(name, players)
            except:
                print(f'"{name}" non corrisponde alle iniziali di nessun giocatore')
                return

            player.add(number)
        else:
            print(f'"{command}" non Ã¨ un comando valido')

    def validate_int(self, value):
        try:
            return int(value)
        except:
            return None

    def confirm(self, prompt):
        return input(prompt + ' (Y/n): ').lower() == 'y'

    def clear(self):
        clear()  # Titolo
        print('SCARABEO\n')

    def validate_command(self, command):
        try:
            sw, number = command.split(' ')
            return sw, int(number)
        except:
            return None


if __name__ == '__main__':
    try:
        Game()
    except KeyboardInterrupt:
        print('\nEsecuzione Terminata\n')
