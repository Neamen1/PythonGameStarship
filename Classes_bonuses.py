import random
import global_vars as glv
from global_constans import FIELD_WIDTH, FIELD_HEIGHT


class Bonus:
    def __init__(self, shiftx=0, shifty=0.5, x2=0, y2=0):
        self.shiftx = shiftx
        self.shifty = shifty
        
        self.canvid = None
    def move(self):
        glv.CANVAS.move(self.canvid, self.shiftx, self.shifty)
    def clear(self):
        glv.CANVAS.delete(self.canvid)

class Bullet_bonus(Bonus):
    def __init__(self):
        super(Bullet_bonus, self).__init__()
        x = random.randrange(int(FIELD_WIDTH * 0.2), int(FIELD_WIDTH * 0.8), 5)
        y = random.randrange(int(FIELD_HEIGHT * 0.1), int(FIELD_HEIGHT * 0.4), 5)
        self.canvid = glv.CANVAS.create_rectangle(x, y, x+30, y+30, fill="yellow", tag="Bonus")

class Enemy_wipe_bonus(Bonus):
    def __init__(self):
        super(Enemy_wipe_bonus, self).__init__()
        x = random.randrange(int(FIELD_WIDTH * 0.2), int(FIELD_WIDTH * 0.8), 5)
        y = random.randrange(int(FIELD_HEIGHT * 0.1), int(FIELD_HEIGHT * 0.4), 5)
        self.canvid = glv.CANVAS.create_rectangle(x, y, x+30, y+30, fill="pink", tag="Bonus")
