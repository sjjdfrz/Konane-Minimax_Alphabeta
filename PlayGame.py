from PlayKonane import PlayKonane
from Tile import Tile
from Agent import Agent
from Board import Board
from KonaneGame import KonaneGame as konanegame1
from KonaneGame2 import KonaneGame as konanegame2


class PlayGame:

    def __init__(self):
        NotImplemented

    def play(self):
        size = 6
        game1 = konanegame1()
        game2 = konanegame2()
        initial_board = Board(size, game1.initialize_board(size))
        agent1 = Agent(game1, color=Tile.P_Black, max_depth=4)
        agent2 = Agent(game2, color=Tile.P_White, max_depth=4)
        # bot vs bot
        play = PlayKonane(initial_board, game1, agent1=agent1, agent2=agent2)

        # player vs bot
        #play = PlayKonane(initial_board, game1, agent1=agent1)
    



if __name__ == '__main__':
    PlayGame().play()