from global_constans import FIELD_WIDTH, FIELD_HEIGHT, FLOOR_SIZE, PLAYER_WIDTH, PLAYER_HEIGHT
import global_vars as glv
from Bullet_class import Bullet


class Player:
    
    def __init__(self, player_texture, bul_color, player_width = PLAYER_WIDTH, player_height=PLAYER_HEIGHT):
        self.id = glv.CANVAS.create_image(  # drawing image on coordinates
        (FIELD_WIDTH - player_width) / 2,
        FIELD_HEIGHT - player_height - FLOOR_SIZE,
        image=player_texture)
        self.bul_color = bul_color

    def move(self, step):
        step*=glv.player_speed
        player_pos = glv.CANVAS.bbox(self.id)
        if not player_pos:
            return
        if not (player_pos[0] + step < FIELD_WIDTH * 0.1 or player_pos[2]+step > FIELD_WIDTH * 0.9):
            glv.CANVAS.move(self.id, step, 0)

    def shoot(self, game):
        ammo = game["ammo"].get()
        if ammo > 0:
            player_pos = glv.CANVAS.bbox(self.id)
            if not player_pos:
                return
            player_x = (player_pos[0]+player_pos[2])//2
            player_y = player_pos[1]
            bullet_shift = 15
            diagonal_shift_x = 2            # shift for additional bullets, which will go to the sides also, not just straight
            for i in range(glv.bullet_quantity_upgrade_level):      # spawn as many bullets as the upgrade level
                shift_x=((0-glv.bullet_quantity_upgrade_level /2)+i)*bullet_shift+bullet_shift/2
                if glv.bullet_quantity_upgrade_level==1:
                    bullet = Bullet(player_x = player_x, player_y=player_y, bul_color = self.bul_color,diagonal_shift_x = 0)  
                elif glv.bullet_quantity_upgrade_level==2 and i==0:
                    bullet = Bullet(player_x = player_x + shift_x, player_y=player_y, bul_color = self.bul_color,diagonal_shift_x = 0-diagonal_shift_x)
                elif glv.bullet_quantity_upgrade_level == 2 and i==1:
                    bullet = Bullet(player_x = player_x + shift_x, player_y=player_y, bul_color = self.bul_color,diagonal_shift_x = diagonal_shift_x)
                else:
                    bullet = Bullet(player_x = player_x + shift_x, player_y=player_y, bul_color = self.bul_color,diagonal_shift_x = diagonal_shift_x*(i-1))   
                game["bullets"].append(bullet)
            game["ammo"].set(ammo-1)