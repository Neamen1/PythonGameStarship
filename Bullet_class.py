import global_vars as glv


class Bullet:
    def __init__(self, player_x, player_y, bul_color, diagonal_shift_x=0):
        self.diag_shift_x = diagonal_shift_x
        # self.canvid = glv.CANVAS.create_rectangle(         # rectangle bullets
        #     (player_x-4), player_y-65,
        #     (player_x + 4), player_y-5,
        #     fill=bul_color, tag="bullet")
        self.canvid = glv.CANVAS.create_oval(            # oval bullets
            (player_x-5), player_y-5-30,
            (player_x + 5), player_y-5,
            fill=bul_color, tag="bullet")
            
        
    def move(self):
        glv.CANVAS.move(self.canvid, self.diag_shift_x, -20 - (glv.speed_of_bullet_upgrade_level))

    def clear(self):
        glv.CANVAS.delete(self.canvid)