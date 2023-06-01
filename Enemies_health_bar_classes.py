import random
import global_vars as glv
from global_constans import FIELD_WIDTH, FIELD_HEIGHT

class health_bar:
    def __init__(self, max_health, enemy_canvid):
        self.health = max_health
        self.max_health = max_health
        # create red bar
        pos = glv.CANVAS.bbox(enemy_canvid)
        height = 10
        width = (pos[2] - pos[0]) * (self.health / self.max_health)
        self.health_cid2 = glv.CANVAS.create_rectangle(     # red bar
            pos[0], pos[1] - height - 5,
            pos[0] + (pos[2] - pos[0]), pos[1] - 5,
            fill='red'
        )
        self.health_cid = glv.CANVAS.create_rectangle(      # green bar
            pos[0], pos[1] - height - 5,
            pos[0] + width, pos[1] - 5,
            fill='green'
        )

    def move(self, shiftx, shifty):
        glv.CANVAS.move(self.health_cid, shiftx, shifty)
        glv.CANVAS.move(self.health_cid2, shiftx, shifty)

    def redraw_health(self, enemy_canvid):  # redraw health
        if self.health_cid:
            glv.CANVAS.delete(self.health_cid)

        pos = glv.CANVAS.bbox(enemy_canvid)
        if not pos:
            return
        width = (pos[2] - pos[0]) * (self.health / self.max_health)
        height = 10
        self.health_cid = glv.CANVAS.create_rectangle(
            pos[0], pos[1] - height - 5,
            pos[0] + width, pos[1] - 5,
            fill='green'
        )
        
    
    def clear(self):
        glv.CANVAS.delete(self.health_cid)
        glv.CANVAS.delete(self.health_cid2)


class Enemies:
    max_health = 6  # basic max_health of enemy

    def __init__(self, enemy_texture, shiftx=0, shifty=0, enemy_heaviness = "light"):
        self.enemy_heaviness = enemy_heaviness
        self.shiftx = shiftx
        self.shifty = shifty
        # position of enemy
        x = random.randrange(int(FIELD_WIDTH * 0.2), int(FIELD_WIDTH * 0.8), 5)
        y = FIELD_HEIGHT * 0.1
        self.canvid = glv.CANVAS.create_image(x, y, image=enemy_texture, tag="Enemies")
        
        if enemy_heaviness == "light":
            self.max_health = self.max_health
        elif enemy_heaviness == "medium":
            self.max_health = self.max_health*3
        elif enemy_heaviness == "heavy":
            self.max_health = self.max_health*6
        elif enemy_heaviness == "boss":
            self.max_health = self.max_health*18

        self.hb = health_bar(self.max_health, self.canvid)      # class composition

    def move(self):
        glv.CANVAS.move(self.canvid, self.shiftx, self.shifty)
        self.hb.move(self.shiftx, self.shifty)

    def clear(self):
        glv.CANVAS.delete(self.canvid)
        self.hb.clear()
