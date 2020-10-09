import sys, random, argparse
from queue import Queue


class Players(object):
    #Game players track
    def __init__(self, players):
        self.__players = players
        self.__current_player = players.get()

    def get_current_player(self):
        return self.__current_player

    def get_next_player(self):
        self.__players.put(self.__current_player)
        self.__current_player = self.__players.get()
        return self.__current_player

    def get_players(self):
        self.__players.put(self.__current_player)
        return self.__players


class Player(object):
    #Players score, name and rolls
    def __init__(self, name):
        self.__name = name.strip()
        self.__score = 0
        self.__rolls = 0

    def get_name(self):
        return self.__name

    def get_score(self):
        return self.__score

    def get_rolls(self):
        return self.__rolls

    def commit_score(self, score, rolls):
        self.__score += score
        self.__rolls += rolls


class Die(object):
    #The Die
    def __init__(self):
        random.seed(0)

    def roll(self):
        return random.randint(1, 6)


class Game(object):
    #Game itself
    def __init__(self, players):
        self.__players = Players(players)
        self.__die = Die()

    def start(self):
        self.__turn()

    def __game_over(self):
        ranking = ((player.get_name(), player.get_score(), player.get_rolls())
                       for player in list(self.__players.get_players().queue))

        print("\nPig Results:\n")
        for player in sorted(ranking, key=lambda player: (player[1]),reverse=True):
            print("{} Scored {} points, rolled {} times".format(player[0], player[1], player[2]))


    def __turn(self, next_player=False):
        player = self.__players.get_current_player() if not next_player else self.__players.get_next_player()

        current_score = 0
        rolls = 0

        active_turn = True
        game_over = False

        print("\n{}'s turn. Current score is {}".format( player.get_name(), player.get_score()))

        while active_turn and not game_over:

            action = input( "Please enter 'r' to roll or 'h' to hold. Your Choice? ")
            # Rolling
            if action == "r":
                roll = self.__die.roll()
                rolls += 1

                if roll == 1:
                    current_score = 0
                    player.commit_score(current_score, rolls)
                    print("{} rolled a {}, lost all points of the turn. Turn score is 0. Total score: {}.".format(
                        player.get_name(), roll,  player.get_score()))
                    active_turn = False
                else:
                    current_score += roll
                    if (current_score + player.get_score()) >= 100:
                        player.commit_score(current_score, rolls)
                        print("\n{} rolled a {}. Total score is {}. Won the game!"
                              .format(player.get_name(), roll, player.get_score()))
                        game_over, active_turn = True, False
                    else:
                        print("{} rolled a {}. Turn score is {}. Total score is {}".format( player.get_name(),
                            roll,
                            current_score,
                            current_score + player.get_score() ) )
            elif action == "h":
                player.commit_score(current_score, rolls)
                print("{}, you held. Your score for this turn is {}. Total score: {}.".format(
                    player.get_name(), current_score, player.get_score()))
                active_turn = False
            else:
                print("Invalid option.")

        if not game_over:
            self.__turn(True)
        else:
            self.__game_over()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--numPlayers', type=int, help='Number of players',)
    args = parser.parse_args()

    
    if args.numPlayers is None: player_count = 2
    else: player_count = args.numPlayers
    
    if player_count < 2:
        print("There must be at least 2 players.")
        sys.exit()

    players = Queue()

    for i in range(0, player_count):
        player = Player(input("Player {}'s name? ".format(str(i+1))))
        players.put(player)

    Game(players).start()

    sys.exit()


if __name__ == '__main__':
    main()
