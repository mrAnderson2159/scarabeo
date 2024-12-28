from src.game import Game

if __name__ == '__main__':
    try:
        Game()
    except KeyboardInterrupt:
        print('\nEsecuzione Terminata\n')
