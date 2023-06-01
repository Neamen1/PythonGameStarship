import global_vars as glv

class Dead_Piece:
    piece_size = 5          
    color = "#EE5F10"
    def __init__(self, x, y, shift_x, shift_y):
        self.canvid = glv.CANVAS.create_rectangle(
            x, y, x + Dead_Piece.piece_size, y + Dead_Piece.piece_size, fill=Dead_Piece.color)
        self.frames = 40
        self.shiftx = shift_x
        self.shifty = shift_y

    def move(self):
        glv.CANVAS.move(self.canvid, self.shiftx, self.shifty)
        self.frames-=1
