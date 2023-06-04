import random
from GUInterface import Graphic
from Tile import Tile


class PlayKonane:

    def __init__(self, init_board, game_manager ,agent1, agent2 = None):
        self.init_board = init_board
        self.game_manager = game_manager
        self.agent1 = agent1
        self.agent2 = agent2
        self.play(init_board)
        
    def play(self, init_board):
        """
        Resets the starting board state.
        """
        self.computing = False
        self.selected_tile = None
        self.current_player = Tile.P_Black
        self.valid_moves = []
   
        self.board = init_board
        self.c_player=Tile.P_White
        self.board_view = Graphic(self.board.game_board)
        self.game_finished = False

        if self.agent2 is None:
            self.board_view.add_click_handler(self.tile_clicked)
        else:
            self.run_bot_vs_bot()

        self.board_view.draw_tiles(board = self.board.game_board)
        self.board_view.mainloop()


    def run_bot_vs_bot(self):

        self.execute_computer_move(self.agent1)
        if not self.game_finished:
            self.execute_computer_move(self.agent2)
        if not self.game_finished:
            self.run_bot_vs_bot()


    def tile_clicked(self, row, col):
  
        if self.computing:  # Block clicks while computing
            return
        new_tile = self.board.game_board[row][col]
        # If we are selecting a friendly piece

        if self.board.is_opening_move():
            self.selected_tile = new_tile
            self.valid_moves = self.game_manager.get_moves_at_tile(self.board, new_tile, self.current_player)
            for tile in  self.valid_moves:
                if self.selected_tile == tile:
                    self.outline_tiles(None)  # Reset outlines
                    self.do_move(self.current_player, [self.selected_tile.row, self.selected_tile.col, new_tile.row, new_tile.col])

                    # Update status and reset tracking variables
                    self.selected_tile = None
                    self.valid_moves = []
                    self.toggle_current_player()
                    if self.c_player is not None:
                        self.execute_computer_move(self.agent1)


        elif new_tile.piece == self.current_player:
            
            self.outline_tiles(None)  # Reset outlines
            
            # Outline the new and valid move tiles
            new_tile.outline = Tile.O_MOVED
            self.valid_moves = self.game_manager.get_moves_at_tile(self.board, new_tile, self.current_player)
            
            # Update status and save the new tile
            self.outline_tiles(self.valid_moves)
            self.board_view.set_status("Tile `" + str(new_tile.row) + "," + str(new_tile.col) +"` selected")
            self.selected_tile = new_tile

            self.board_view.draw_tiles(board = self.board.game_board)  # Refresh the board

        # If we already had a piece selected and we are moving a piece
        elif self.selected_tile and new_tile in self.valid_moves:
            self.outline_tiles(None)  # Reset outlines
            self.do_move(self.current_player, [self.selected_tile.row, self.selected_tile.col, new_tile.row, new_tile.col])

            # Update status and reset tracking variables
            self.selected_tile = None
            self.valid_moves = []
            self.toggle_current_player()
         
            # If there is a winner to the game
            winner = self.game_manager.find_winner(self.board, self.current_player)
            if winner:
                self.board_view.set_status("The " + ("white"
                    if winner == Tile.P_White else "black") + " player has won!")
                self.current_player = None
                self.print_winner(winner)
                print(self.boardToStr(self.board))
            
            elif self.c_player is not None:
                self.execute_computer_move(self.agent1)
            
        else:
            self.board_view.set_status("Invalid move attempted")    



    def do_move(self, player, move):
        """
        Updates the current board with the next board created by the given
        move.
        """
        self.computing = True
        self.board = self.board.next_board(player, move)
        self.board_view.draw_tiles(board = self.board.game_board)
        self.computing = False
        print("player: " + str(player))
        print(self.boardToStr(self.board))
        print("---------------------------")


    def outline_tiles(self, tiles=[], outline_type=Tile.O_SELECT):

        if tiles is None:
            tiles = [j for i in self.board.game_board for j in i]
            outline_type = Tile.O_NONE

        for tile in tiles:
            tile.outline = outline_type   



    def execute_computer_move(self, agent):

        self.computing = True
        self.board_view.update()
        max_depth = 3

        move = agent.do_min_max(self.board)

        self.outline_tiles(None)  # Reset outlines

        self.do_move(self.current_player, move)

        self.toggle_current_player()
        winner = self.game_manager.find_winner(self.board, self.current_player)
        if winner:
            self.board_view.set_status("The " + ("white"
                if winner == Tile.P_White else "black") + " player has won!")
            self.board_view.set_status_color("#212121")
            self.current_player = None
            self.print_winner(winner)
            self.game_finished = True

        self.computing = False
        
        print()

    def print_winner(self, winner):
        print()
        print("Final Stats")
        print("===========")
        print("Final winner:", "white"
            if winner == Tile.P_White else "black")


    def toggle_current_player(self):
        self.current_player = (Tile.P_Black
                if self.current_player == Tile.P_White else Tile.P_White)


    def boardToStr(self, board):
            """
            Returns a string representation of the konane board.
            """
            result = "  "
            for i in range(board.size):
                result += str(i) + " "
            result += "\n"
            for i in range(board.size):
                result += str(i) + " "
                for j in range(board.size):
                    result += str(board.game_board[i][j].piece) + " "
                result += "\n"
            return result