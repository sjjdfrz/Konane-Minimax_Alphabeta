class Tile():
    # Piece constants
    P_NONE = 0
    P_White = 1
    P_Black = 2

    # Outline constants
    O_NONE = 0
    O_SELECT = 1
    O_MOVED = 2
    
    def __init__(self, piece= 0, outline=0, row=0, col=0):
        self.outline = outline
        self.piece = piece
        self.row = row
        self.col = col

    def get_tile_colors(self):

        # Find appropriate tile color
        tile_colors = [
            ("#8C6C50", "#DBBFA0")
        ]
        tile_color = tile_colors[0][0] if ((self.row + self.col) % 2) else tile_colors[0][1]

        # Find appropriate outline color
        outline_colors = [
            tile_color,
            "yellow",  # TODO: Change
            "#1100BB"
        ]
        outline_color = outline_colors[self.outline]

        return tile_color, outline_color

    def __str__(self):
        return chr(self.col + 97) + str(self.row + 1)

    def __repr__(self):
        return chr(self.col + 97) + str(self.row + 1)

    def update_color(self, tile_color):
        self.piece = tile_color
