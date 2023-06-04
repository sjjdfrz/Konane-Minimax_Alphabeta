from Tile import Tile


class Agent:
    MIN_VALUE = -1000000
    MAX_VALUE = 1000000

    def __init__(self, game, color, max_depth):
        self.game = game
        self.color = color
        self.max_depth = max_depth

    def do_min_max(self, current_board):
        alpha = self.MIN_VALUE
        betha = self.MAX_VALUE
        move, value = self.max(current_board, self.color, 0, alpha, betha)

        return move

    def max(self, current_board, current_color, depth, alpha, betha):

        if self.game.check_terminal(current_board, current_color):
            return None, self.game.evaluate(current_board, current_color, -1000)

        if depth == self.max_depth:
            return None, self.game.evaluate(current_board, current_color)

        possible_moves = self.game.generate_all_possible_moves(current_board, current_color)
        best_move = None
        best_move_value = self.MIN_VALUE

        for move in possible_moves:
            temp_move, value = self.min(current_board.next_board(current_color, move),
                                        self.game.opponent(current_color), depth + 1, alpha, betha)
            if value > best_move_value:
                best_move_value = value
                best_move = move

                if best_move_value >= betha:
                    return best_move, best_move_value
                alpha = max(alpha, best_move_value)

        return best_move, best_move_value

    def min(self, current_board, current_color, depth, alpha, betha):
        if self.game.check_terminal(current_board, current_color):
            return None, self.game.evaluate(current_board, current_color, 1000)

        if depth == self.max_depth:
            return None, self.game.evaluate(current_board, current_color)

        possible_moves = self.game.generate_all_possible_moves(current_board, current_color)
        best_move = None
        best_move_value = self.MAX_VALUE
        for move in possible_moves:
            temp_move, value = self.max(current_board.next_board(current_color, move),
                                        self.game.opponent(current_color), depth + 1, alpha, betha)
            if value < best_move_value:
                best_move_value = value
                best_move = move

                if best_move_value < alpha:
                    return best_move, best_move_value
                betha = min(betha, best_move_value)

        return best_move, best_move_value
