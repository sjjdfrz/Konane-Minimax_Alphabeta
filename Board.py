from Tile import Tile
import copy


class KonaneError(AttributeError):
    """
    This class is used to indicate a problem in the konane game.
    """


class Board:
    def __init__(self, size, init_board):
        self.size = size
        self.game_board = init_board

    def next_board(self, player, move):
        """
        Given a move for a particular player from (r1,c1) to (r2,c2) this
        executes the move on a copy of the current konane board.  It will
        raise a KonaneError if the move is invalid. It returns the copy of
        the board, and does not change the given board.
        """
        r1 = move[0]
        c1 = move[1]
        r2 = move[2]
        c2 = move[3]

        next = copy.deepcopy(self)
        if not (self.valid(r1, c1) and self.valid(r2, c2)):
            raise KonaneError

        if next.game_board[r1][c1].piece != player:
            raise KonaneError
        dist = self.distance(r1, c1, r2, c2)
        if dist == 0:
            if self.is_opening_move():
                next.game_board[r1][c1].piece = Tile.P_NONE
                return next
            raise KonaneError
        if next.game_board[r2][c2].piece != Tile.P_NONE:
            raise KonaneError
        jumps = dist / 2
        dr = int((r2 - r1) / dist)
        dc = int((c2 - c1) / dist)
        for i in range(int(jumps)):
            # test
            if next.game_board[r1 + dr][c1 + dc].piece != (3 - player):
                raise KonaneError
            next.game_board[r1][c1].piece = Tile.P_NONE
            next.game_board[r1 + dr][c1 + dc].piece = Tile.P_NONE
            r1 += 2 * dr
            c1 += 2 * dc
            next.game_board[r1][c1].piece = player
        return next

    def valid(self, row, col):
        """
        Returns true if the given row and col represent a valid location on
        the konane board.
        """
        return row >= 0 and col >= 0 and row < self.size and col < self.size

    def distance(self, r1, c1, r2, c2):
        """
        Returns the distance between two points in a vertical or
        horizontal line on the konane board. Diagonal jumps are NOT
        allowed.
        """
        return abs(r1 - r2 + c1 - c2)

    def is_opening_move(self):
        return self.count_symbol(Tile.P_NONE) <= 1

    def count_symbol(self, symbol):
        """
        Returns the number of instances of the symbol on the board.
        """
        count = 0
        for r in range(self.size):
            for c in range(self.size):
                if self.game_board[r][c].piece == symbol:
                    count += 1
        return count

    def contains(self, row, col, symbol):
        """
        Returns true if the given row and col represent a valid location on
        the konane board and that location contains the given symbol.
        """
        return self.valid(row, col) and self.game_board[row][col].piece == symbol
