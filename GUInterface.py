import tkinter as tk

class Graphic(tk.Tk):

    def __init__(self, init_board, *args, **kwargs):

        # Initialize parent tk class
        tk.Tk.__init__(self, *args, **kwargs)

        # Save metadata
        self.title("Konane | Bash Games")
        #self.wm_iconbitmap("deep_red.ico")
        self.wm_iconbitmap("Doc/BashGames.ico")
        self.resizable(False, False)
        self.configure(bg="#fff")

        # Save tracking variables
        self.tiles = {}
        self.board = init_board
        self.b_size = len(init_board)

        self.init_click_handler()
        
        # Create column/row labels
        label_font = "Helvetica 16"
        label_bg = "#fff"
        label_fg = "#333"
        for i in range(self.b_size):

            row_label1 = tk.Label(self, text=i , font=label_font,
                bg=label_bg, fg=label_fg)
            row_label1.grid(row=i + 1, column=0)


            col_label1 = tk.Label(self, text=i , font=label_font,
                bg=label_bg, fg=label_fg)
            col_label1.grid(row=0, column=i + 1)

   

        # Create grid canvas
        self.canvas = tk.Canvas(self, width=550, height=550, bg="#fff",
            highlightthickness=0)
        self.canvas.grid(row=1, column=1,
            columnspan=self.b_size, rowspan=self.b_size)

        # Create status label
        self.status = tk.Label(self, anchor="c", font=(None, 16),
            bg="#212121", fg="#fff", text="White player's turn")
        self.status.grid(row=self.b_size + 3, column=0,
            columnspan=self.b_size + 3, sticky="ewns")

        # Bind the drawing function and configure grid sizes
        self.canvas.bind("<Configure>", self.draw_tiles)
        self.columnconfigure(0, minsize=48)
        self.rowconfigure(0, minsize=48)
        self.columnconfigure(self.b_size + 2, minsize=48)
        self.rowconfigure(self.b_size + 2, minsize=48)
        self.rowconfigure(self.b_size + 3, minsize=48)

    # Public Methods #

    def add_click_handler(self, func):
        self.click_handler = func

    def init_click_handler(self):
        self.click_handler = False

    def set_status(self, text):
        self.status.configure(text=text)

    def set_status_color(self, color):
        self.status.configure(bg=color)

    def draw_tiles(self, event=None, board=None):

        if board is not None:
            self.board = board
        else:
            print("board is not set")
            
        # Delete old rectangles and save properties
        self.canvas.delete("tile")
        cell_width = int(self.canvas.winfo_width() / self.b_size)
        cell_height = int(self.canvas.winfo_height() / self.b_size)
        border_size = 5

        # Recreate each rectangle
        for col in range(self.b_size):
            for row in range(self.b_size):

                board_tile = self.board[row][col]
                tile_color, outline_color = board_tile.get_tile_colors()

                # Calculate pixel positions
                x1 = col * cell_width + border_size / 2
                y1 = row * cell_height + border_size / 2
                x2 = (col + 1) * cell_width - border_size / 2
                y2 = (row + 1) * cell_height - border_size / 2

                # Render tile
                tile = self.canvas.create_rectangle(x1, y1, x2, y2,
                    tags="tile", width=border_size, fill=tile_color,
                    outline=outline_color)
                self.tiles[row, col] = tile
                if self.click_handler:
                    self.canvas.tag_bind(tile, "<1>", lambda event, row=row,
                        col=col: self.click_handler(row, col))

        self.draw_pieces()

    def draw_pieces(self, board=None):

        if board is not None:
            self.board = board

        self.canvas.delete("piece")
        cell_width = int(self.canvas.winfo_width() / self.b_size)
        cell_height = int(self.canvas.winfo_height() / self.b_size)
        border_size = 20

        for col in range(self.b_size):
            for row in range(self.b_size):

                # Calculate pixel positions
                x1 = col * cell_width + border_size / 2
                y1 = row * cell_height + border_size / 2
                x2 = (col + 1) * cell_width - border_size / 2
                y2 = (row + 1) * cell_height - border_size / 2

                if self.board[row][col].piece == 2:
                    piece = self.canvas.create_oval(x1, y1, x2, y2,
                        tags="piece", width=0, fill="#302424")
                elif self.board[row][col].piece == 1:
                    piece = self.canvas.create_oval(x1, y1, x2, y2,
                        tags="piece", width=0, fill="#ded5d5")
                else:
                    continue
                

                if self.click_handler:
                    self.canvas.tag_bind(piece, "<1>", lambda event, row=row,
                        col=col: self.click_handler(row, col))

        self.update()
