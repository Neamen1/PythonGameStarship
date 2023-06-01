import math
import os
import random
import time
import tkinter as tk
from PIL import Image, ImageTk  # Pillow library
from global_constans import *
import global_vars as glv
# import classes
from Dead_Piece_class import Dead_Piece
from Player_class import Player
from Enemies_health_bar_classes import Enemies
from Classes_bonuses import Bullet_bonus, Enemy_wipe_bonus

choose_difficulty = tk.IntVar()     # in-game difficulty 
BUTTONS = {}        # all buttons are stored in dictionary

warning_text = None

# writing images pathes
ENEMY_TEXTURE_LIGHT = tk.PhotoImage(file=os.path.join(IMAGES_DIR, ENEMY_IMAGE_LIGHT))
ENEMY_TEXTURE_MEDIUM = tk.PhotoImage(file=os.path.join(IMAGES_DIR, ENEMY_IMAGE_MEDIUM))
ENEMY_TEXTURE_HEAVY = tk.PhotoImage(file=os.path.join(IMAGES_DIR, ENEMY_IMAGE_HEAVY))
ENEMY_TEXTURE_BOSS = tk.PhotoImage(file=os.path.join(IMAGES_DIR, ENEMY_IMAGE_BOSS))

PLAYER1_IMG_FILE = os.path.join(IMAGES_DIR, PLAYER1_IMAGE)      # player image path
PLAYER1_IMAGE = Image.open(PLAYER1_IMG_FILE).resize((PLAYER_WIDTH, PLAYER_HEIGHT))
# Image.open(file) loads image and creates image object, which ahs resize method
# resize(size) creates an image copy with new size
PLAYER1_TEXTURE = ImageTk.PhotoImage(image=PLAYER1_IMAGE) # for tkinter we need to conver image to ImageTk type instead Image type

PLAYER2_IMG_FILE = os.path.join(IMAGES_DIR, PLAYER2_IMAGE)
PLAYER2_IMAGE = Image.open(PLAYER2_IMG_FILE).resize((PLAYER_WIDTH, PLAYER_HEIGHT))
PLAYER2_TEXTURE = ImageTk.PhotoImage(image=PLAYER2_IMAGE)

def main():
    glv.CANVAS.delete(tk.ALL)
    BUTTONS["retry"].place_forget()
    BUTTONS["continue"].place_forget()
    BUTTONS["damage_upgrade_level"].place_forget()
    BUTTONS["player_speed"].place_forget()
    BUTTONS["bullet_quantity_upgrade_level"].place_forget()
    BUTTONS["speed_of_bullet_upgrade_level"].place_forget()
    BUTTONS["go_main_menu"].place_forget()
    
    BUTTONS["quit"].place(x=FIELD_WIDTH - 180, y=FIELD_HEIGHT - 100, width=80, height=40)
    
    # (re)drawing coins amount
    pos_1 = FIELD_WIDTH // 1.4 
    pos_2 = FIELD_HEIGHT // 2.5 
    COINS = glv.CANVAS.find_overlapping(pos_1 - 10, pos_2 - 10, pos_1 + 10, pos_2 + 10)     
    if COINS and glv.CANVAS.type(COINS) == 'text':
        glv.CANVAS.delete(COINS)
    glv.CANVAS.create_text(pos_1, pos_2, text=f'coins: {glv.coins}', fill="white")  # creating new text
    
    BUTTONS["go_main_menu"].configure(command=main)
    # placing main manu buttons
    BUTTONS["top_score"] = tk.Button(glv.ROOT, text="Top score", command=scores_func, fg="white", name="score_menu",background="#C88539")
    BUTTONS["top_score"].place(x=(FIELD_WIDTH - 80) // 3.75, y=(FIELD_HEIGHT - 65) / 2, width=80, height=65)
    
    BUTTONS["run"].place(x=(FIELD_WIDTH - 100) / 2, y=(FIELD_HEIGHT - 100) / 2, width=100, height=90)
    BUTTONS["upgrades_menu"].place(x=(FIELD_WIDTH - 80)//1.35, y=(FIELD_HEIGHT - 65) / 2, width=80, height=65)

    choose_difficulty.set(0)
    

    BUTTONS["easyHardness"].place(x=(FIELD_WIDTH - 100) / 2, y=(FIELD_HEIGHT - 100) / 2 + 160, height=20)
    BUTTONS["midHardness"].place(x=(FIELD_WIDTH - 100) / 2, y=(FIELD_HEIGHT - 100) / 2 + 180, height=20)
    BUTTONS["highHardness"].place(x=(FIELD_WIDTH - 100) / 2, y=(FIELD_HEIGHT - 100) / 2 + 200, height=20)
    glv.ROOT.mainloop()


def write_to_file():        # write updated data to data file
        game_money = open(DATA_DIR_NAME, 'w')
        game_money.write("money:"+str(glv.coins)+"\n"+
                        "damage_upgrade_level:" + str(glv.damage_upgrade_level)+ "\n"+
                        "player_speed:" + str(glv.player_speed)+"\n"+
                        "bullet_upgrade_level:" + str(glv.bullet_quantity_upgrade_level)+"\n"+
                        "speed_of_bullet_upgrade_level:" + str(glv.speed_of_bullet_upgrade_level)+"\n")

        game_money.close()

# upgrades menu
def upgrades():
    # cleaning all active objects
    glv.CANVAS.delete(tk.ALL)   

    BUTTONS["run"].place_forget()
    BUTTONS["retry"].place_forget()
    BUTTONS["quit"].place_forget()
    BUTTONS["easyHardness"].place_forget()
    BUTTONS["midHardness"].place_forget()
    BUTTONS["highHardness"].place_forget()
    BUTTONS["top_score"].place_forget()
    BUTTONS["upgrades_menu"].place_forget()
    
    # placing new buttons and text
    BUTTONS["damage_upgrade_level"].place(x=20, y=(FIELD_HEIGHT - 65) / 2.6, width=200, height=65)
    BUTTONS["player_speed"].place(x=20, y=(FIELD_HEIGHT - 65) / 2.6 + 65*1+10, width=200, height=65)
    BUTTONS["bullet_quantity_upgrade_level"].place(x=20, y=(FIELD_HEIGHT - 65) / 2.6 + (65+10)*2, width=200, height=65)
    BUTTONS["speed_of_bullet_upgrade_level"].place(x=20, y=(FIELD_HEIGHT - 65) / 2.6 + (65+10)*3, width=200, height=65)
    
    glv.CANVAS.create_text(FIELD_WIDTH / 2, 50, font=("ARIAL", 10), text=f'coins: {glv.coins}', fill="white")
    
    
    def redraw_coins_text():
        coins_text = glv.CANVAS.find_overlapping(FIELD_WIDTH / 2 - 10, 50 - 10, FIELD_WIDTH / 2 + 10, 50 + 10)
        for elem in coins_text:
            if glv.CANVAS.type(elem) == 'text':
                glv.CANVAS.delete(elem)
            glv.CANVAS.create_text(FIELD_WIDTH / 2, 50, font=("ARIAL", 10), text=f'coins: {glv.coins}', fill="white")
    damage_upgrade_needed_coins = 200 * (glv.damage_upgrade_level)
    #
    def buy_damage_upgrade():
        
        damage_upgrade_needed_coins = 200 * (glv.damage_upgrade_level)
        if glv.damage_upgrade_level >= 20:
            BUTTONS["damage_upgrade_level"].configure(command=None, text="Max damage upgrade!")
        elif glv.coins>=damage_upgrade_needed_coins:              # if enough money - buys upgrade
            pos_x = FIELD_WIDTH / 2
            pos_y = 20
            not_en_coins_text = glv.CANVAS.find_overlapping(pos_x - 10, pos_y - 10, pos_x + 10, pos_y + 10)
            glv.CANVAS.delete(not_en_coins_text)
            glv.coins -= damage_upgrade_needed_coins
            glv.damage_upgrade_level+=1
            damage_upgrade_needed_coins = 200 * (glv.damage_upgrade_level)
            write_to_file()
            redraw_coins_text()
            BUTTONS["damage_upgrade_level"].configure(text=f"Damage upgrade level: {glv.damage_upgrade_level} \n needed coins: {damage_upgrade_needed_coins}")
        else:
            glv.CANVAS.create_text(FIELD_WIDTH / 2, 20, font=("ARIAL", 20, "bold"), text='Not enough coins!', fill="red")
    #
    player_speed_needed_coins = 250 * int((glv.player_speed+0.1) * 10)
    def buy_player_speed():
        player_speed_needed_coins = 250 * int((glv.player_speed+0.1) * 10)
        if glv.player_speed >= 2:
            BUTTONS["player_speed"].configure(command=None, text="Max player speed upgrade!")
        elif glv.coins>=player_speed_needed_coins:
            pos_x = FIELD_WIDTH / 2
            pos_y = 20
            not_en_coins_text = glv.CANVAS.find_overlapping(pos_x - 10, pos_y - 10, pos_x + 10, pos_y + 10)
            glv.CANVAS.delete(not_en_coins_text)
            glv.coins -= player_speed_needed_coins
            glv.player_speed=round(glv.player_speed+0.1, 1)
            player_speed_needed_coins = 250 * int((glv.player_speed+0.1) * 10)
            write_to_file()
            redraw_coins_text()
            BUTTONS["player_speed"].configure(text=f"Player speed upgrade: {glv.player_speed} \n needed coins: {player_speed_needed_coins}")
        else: 
            glv.CANVAS.create_text(FIELD_WIDTH / 2, 20, font=("ARIAL", 20, "bold"), text='Not enough coins!', fill="red")
    #
    bullet_upgrade_level_needed_coins = 1500*(glv.bullet_quantity_upgrade_level+1)
    def bullet_quantity_upgrade():
        bullet_upgrade_level_needed_coins = 1500 * (glv.bullet_quantity_upgrade_level+1)
        if glv.bullet_quantity_upgrade_level >= 3:
            BUTTONS["bullet_quantity_upgrade_level"].configure(command=None, text="Max bullet quantity upgrade!")
        elif glv.coins>=bullet_upgrade_level_needed_coins:
            pos_x = FIELD_WIDTH / 2
            pos_y = 20
            not_en_coins_text = glv.CANVAS.find_overlapping(pos_x - 10, pos_y - 10, pos_x + 10, pos_y + 10)
            glv.CANVAS.delete(not_en_coins_text)
            glv.coins -= bullet_upgrade_level_needed_coins
            glv.bullet_quantity_upgrade_level+=1
            bullet_upgrade_level_needed_coins = 1500 * (glv.bullet_quantity_upgrade_level+1)
            write_to_file()
            redraw_coins_text()
            BUTTONS["bullet_quantity_upgrade_level"].configure(text=f"Bullet quantity upgrade level: {glv.bullet_quantity_upgrade_level} \n needed coins: {bullet_upgrade_level_needed_coins}")
        else: 
            glv.CANVAS.create_text(FIELD_WIDTH / 2, 20, font=("ARIAL", 20, "bold"), text='Not enough coins!', fill="red")
    #   
    speed_of_bullet_needed_coins = 300 * (glv.speed_of_bullet_upgrade_level+1)
    def speed_of_bullet_upgrade():
        speed_of_bullet_needed_coins = 300 * (glv.speed_of_bullet_upgrade_level+1)
        if glv.speed_of_bullet_upgrade_level >= 10:
            BUTTONS["speed_of_bullet_upgrade_level"].configure(command=None, text="Max speed of bullet upgrade!")
        elif glv.coins>=speed_of_bullet_needed_coins:
            pos_x = FIELD_WIDTH / 2
            pos_y = 20
            not_en_coins_text = glv.CANVAS.find_overlapping(pos_x - 10, pos_y - 10, pos_x + 10, pos_y + 10)
            glv.CANVAS.delete(not_en_coins_text)
            glv.coins -= speed_of_bullet_needed_coins
            glv.speed_of_bullet_upgrade_level+=1
            speed_of_bullet_needed_coins = 300 * (glv.speed_of_bullet_upgrade_level+1)
            write_to_file()
            redraw_coins_text()
            BUTTONS["speed_of_bullet_upgrade_level"].configure(text=f"Speed of bullet upgrade level: {glv.speed_of_bullet_upgrade_level} \n needed coins: {speed_of_bullet_needed_coins}")
        else: 
            glv.CANVAS.create_text(FIELD_WIDTH / 2, 20, font=("ARIAL", 20, "bold"), text='Not enough coins!', fill="red")
   
   
    BUTTONS["damage_upgrade_level"].configure(command=buy_damage_upgrade, text=f"Damage upgrade level: {glv.damage_upgrade_level} \n needed coins: {damage_upgrade_needed_coins}")
    BUTTONS["player_speed"].configure(command=buy_player_speed, text=f"Player speed upgrade: {glv.player_speed} \n needed coins: {player_speed_needed_coins}")
    BUTTONS["bullet_quantity_upgrade_level"].configure(command=bullet_quantity_upgrade, text=f"Bullet quantity upgrade level: {glv.bullet_quantity_upgrade_level} \n needed coins: {bullet_upgrade_level_needed_coins}")
    BUTTONS["speed_of_bullet_upgrade_level"].configure(command=speed_of_bullet_upgrade, text=f"Speed of bullet upgrade level: {glv.speed_of_bullet_upgrade_level} \n needed coins: {speed_of_bullet_needed_coins}")
    BUTTONS["go_main_menu"].place(x=(FIELD_WIDTH-160)/2, y=FIELD_HEIGHT - 100, width=160, height=50)  


def scores_func():        # scores menu - shows top 10 scores written in mtopscores.txt
    glv.CANVAS.delete(tk.ALL)

    BUTTONS["run"].place_forget()
    BUTTONS["retry"].place_forget()
    BUTTONS["quit"].place_forget()
    BUTTONS["easyHardness"].place_forget()
    BUTTONS["midHardness"].place_forget()
    BUTTONS["highHardness"].place_forget()
    BUTTONS["top_score"].place_forget()
    BUTTONS["upgrades_menu"].place_forget()

    text = "Top scores: \n"
    for score in glv.top10_scores:
        text+=str(score) + "\n"
    glv.CANVAS.create_text(FIELD_WIDTH / 2, FIELD_HEIGHT / 2 + 30, text=f"{text}", fill="#C88539", font=("Times New Roman", 14, "bold"), justify="center")

    BUTTONS["go_main_menu"].place(x=(FIELD_WIDTH-160)/2, y=FIELD_HEIGHT - 100, width=160, height=50)  

def rungame():      # main game start function
    # removing previous elements
    glv.CANVAS.delete(tk.ALL)
    
    BUTTONS["run"].place_forget()
    BUTTONS["retry"].place_forget()
    BUTTONS["quit"].place_forget()
    BUTTONS["easyHardness"].place_forget()
    BUTTONS["midHardness"].place_forget()
    BUTTONS["highHardness"].place_forget()
    BUTTONS["top_score"].place_forget()
    BUTTONS["go_main_menu"].place_forget()
    BUTTONS["upgrades_menu"].place_forget()

    game = {  # Game state variable are stored in "game" dictionary
        "players": [],  # they will store number - ids of elements in window
        "bullets": [],
        "enemies": [],
        "is_over": False,
        "score": 0,
        "hardness": choose_difficulty.get(),  # difficulty - increases every time winning by 1, can be chosen on the start manu
        "level": 1,
        "start_time" : time.time(),
        "num_of_enemies" : None,        # num of enemies per level
        "ammo": tk.IntVar(value=20 + choose_difficulty.get() * 2), # initial number of ammo, depends on the difficulty
        "bonuses":[],
        "dead_pieces":[]  # for effects after enemy killed
    }
    
    game["ammo"].trace_add('write', lambda *args: redraw_ammo(game))     

    runlevel(game)


def runlevel(game):         # level parameters
    glv.CANVAS.delete(tk.ALL)
    BUTTONS["go_main_menu"].place_forget()
    redraw_ammo(game)
    # num of level
    pos_x = FIELD_WIDTH - (0.1 * FIELD_WIDTH)
    pos_y = .05 * FIELD_HEIGHT
    level_text = glv.CANVAS.find_overlapping(pos_x - 30, pos_y + 10, pos_x, pos_y + 10)
    if level_text and glv.CANVAS.type(level_text) == 'text':
        glv.CANVAS.delete(level_text)
    
    glv.CANVAS.create_text(pos_x, pos_y, text=f'Level: {game["level"]}', fill="white")
    
    
    def do_game_over_on_button_press():
        game["is_over"]=True
        do_game_over(game)
        
    glv.CANVAS.bind_all('<KeyPress-r>', lambda e: do_game_over_on_button_press())

    game["start_time"] = time.time()
    
    if game["level"]%3==0:      # every 3rd level is boss level
        global warning_text
        warning_text = glv.CANVAS.create_text(FIELD_WIDTH/2, FIELD_HEIGHT/2, font=("ARIAL", 20, "bold"),text="Warning! Boss level!", fill="red")        
        glv.CANVAS.after(int((1.5-(game["hardness"]*0.03))*1000) , lambda: glv.CANVAS.delete(warning_text))     # after some time delete warning text
    
    game["num_of_enemies"] = DEFAULT_ENEMIES_NUMBER + game["hardness"]
    

    # (re)drawing money text
    pos_1 = FIELD_WIDTH / 1.5 
    pos_2 = 30
    COINS = glv.CANVAS.find_overlapping(pos_1 - 10, pos_2 - 10, pos_1 + 10, pos_2 + 10)
    if COINS and glv.CANVAS.type(COINS) == 'text':
        glv.CANVAS.delete(COINS)
    glv.CANVAS.create_text(pos_1, pos_2, text=f'coins: {glv.coins}', fill="white")

    redraw_score(game)

    class Playfield:
        def __init__(self):
            self.pressed = {}
            self._set_bindings()
            self.tickCounter=0
            # creating players
            bul_color1 = "red"  # bullet color for player 1
            self.player1 = Player(PLAYER1_TEXTURE, bul_color1)
            self.player1.move(40)
            game["players"].append(self.player1)

            bul_color2 = "purple"  # bullet color for player 2
            self.player2 = Player(PLAYER2_TEXTURE, bul_color2)
            self.player2.move(-40)
            game["players"].append(self.player2)
            game["is_over"] = False
            self.nextstep()

        def nextstep(self):  # game main loop
            update_game(game)

            if self.tickCounter%6==5:
                
                if self.pressed["a"]: self.player2.move(-10)
                elif self.pressed["d"]: self.player2.move(10)
                
                if self.pressed["j"]: self.player1.move(-10)
                elif self.pressed["l"]: self.player1.move(10)

                if self.tickCounter% 10 == 9:
                    if self.pressed["w"]: self.player2.shoot(game)
                    if self.pressed["i"]: self.player1.shoot(game)
                    self.tickCounter=-1
                
            self.tickCounter+=1

            is_won = not game["enemies"] and not game["dead_pieces"] and game["num_of_enemies"]<1
            if game["is_over"]:
                is_won = False
            
            if not is_won and not game["is_over"]:
                glv.CANVAS.after(TICK, self.nextstep)  # invoking loop again every tick, between invoking buttons input can be read
            elif is_won:
                write_to_file()
                do_game_win(game)
            else:
                write_to_file()
                do_game_over(game)

        def _set_bindings(self):
            for char in ["a","d","w", "j", "l", "i"]:
                glv.ROOT.bind("<KeyPress-%s>" % char, self._pressed)
                glv.ROOT.bind("<KeyRelease-%s>" % char, self._released)
                self.pressed[char] = False

        def _pressed(self, event):
            self.pressed[event.char] = True

        def _released(self, event):
            self.pressed[event.char] = False
    
    p = Playfield()
    p.nextstep()

def update_game_score(game,killed_enemy_health):        # score per enemy changes on different difficulties
    if game["hardness"] < 7:
        game["score"] += 1 *killed_enemy_health
    elif game["hardness"] < 14:
        game["score"] += 2*killed_enemy_health
    else:
        game["score"] += 4*killed_enemy_health
    

def update_game(game):
    current_time = (time.time() - game["start_time"])>=(1.5-(game["hardness"]*0.03))        #(1.5-(game["hardness"]*0.1)) - period of time when new enemy is created (in seconds)
    if current_time and game["num_of_enemies"] >=1:   
        enemy = None
        if game["level"] %3==0 and game["num_of_enemies"]%8==0:     # create boss when minimum 8 enemies units are left to spawn on level
            enemy = Enemies(shifty=0.1 + game["hardness"] * 0.1, enemy_heaviness="boss", enemy_texture=ENEMY_TEXTURE_BOSS)
            game["num_of_enemies"] -=6
        elif game["num_of_enemies"] % 6 == 0:       # create heavy enemy when minimum 6 enemies units aENEMY_TEXTURE_n on level
            enemy = Enemies(shifty=0.3 + game["hardness"] * 0.1, enemy_heaviness="heavy", enemy_texture=ENEMY_TEXTURE_HEAVY)
            game["num_of_enemies"] -=1
        elif game["num_of_enemies"] % 3 == 0:
            enemy = Enemies(shifty=0.3 + game["hardness"] * 0.1, enemy_heaviness="medium",enemy_texture=ENEMY_TEXTURE_MEDIUM)       
            game["num_of_enemies"] -=1
        else:
            enemy = Enemies(shifty=0.3 + game["hardness"] * 0.1, enemy_heaviness="light", enemy_texture=ENEMY_TEXTURE_LIGHT)       
            game["num_of_enemies"] -=1
        game["enemies"].append(enemy)
        game["start_time"] = time.time()
    for bullet in game["bullets"]:
        bullet.move()
        killed_enemy = get_killed(bullet, game["enemies"])
        destroy_bonus = get_killed(bullet, game["bonuses"])
        if destroy_bonus:       # when destoying bonus boxes
            explode_from_all_sides(game, destroy_bonus)
            destroy_bonus.clear()
            game["bonuses"].remove(destroy_bonus)
            if isinstance(destroy_bonus, Bullet_bonus):
                game["ammo"].set(game["ammo"].get() + 10 + (game["num_of_enemies"]*2 ))
            elif isinstance(destroy_bonus, Enemy_wipe_bonus):
                for enemy in game["enemies"]:
                    glv.coins+=2
                    explode_enemy_randomly(game, enemy)
                    update_game_score(game, enemy.max_health)
                    enemy.clear()
                game["enemies"].clear()

        
        if killed_enemy:
            chance = random.randint(1, 100)
            
            if chance <10:  # for every enemy hit with some chance spawn bullets bonus
                game["bonuses"].append(Bullet_bonus())
            killed_enemy.hb.health -= glv.damage_upgrade_level     # Decreasing enemy HP on hit
            if killed_enemy.hb.health > 0:
                killed_enemy.hb.redraw_health(killed_enemy.canvid)  # redraw health for living enemies
            else:
                # for dead enemies:
                if chance <5:   # for every enemy kill with some chance spawn enemy wipe bonus
                    game["bonuses"].append(Enemy_wipe_bonus())
                glv.coins+=1*(killed_enemy.max_health //2)
                

                pos_1 = FIELD_WIDTH / 1.5
                pos_2 = 30
                COINS = glv.CANVAS.find_overlapping(pos_1 - 10, pos_2 - 10, pos_1 + 10, pos_2 + 10)
                for elem in COINS:
                    if glv.CANVAS.type(elem) == 'text':
                        glv.CANVAS.delete(elem)
                glv.CANVAS.create_text(pos_1, pos_2, text=f'coins: {glv.coins}', fill="white")

                explode_enemy_randomly(game, killed_enemy)
                update_game_score(game, killed_enemy.max_health)
                killed_enemy.clear()
                game["enemies"].remove(killed_enemy)
                
                
        if killed_enemy or is_outside_borders(bullet) or destroy_bonus:
            bullet.clear()
            game["bullets"].remove(bullet)
    redraw_score(game)   
    
    for enemy in game["enemies"]:
        enemy.move()  # enemies are faster on higher difficulty
        if is_outside_borders(enemy):  # game over on enemies touch bottom borders
            game["is_over"] = True
    
    for bonus in game["bonuses"]: 
        bonus.move()
        if is_outside_borders(bonus):
            bonus.clear()
            game["bonuses"].remove(bonus) 
    
    for piece in game["dead_pieces"]:
        if piece.frames <0:
            glv.CANVAS.delete(piece.canvid)
            game["dead_pieces"].remove(piece)
        else:
            piece.move()
    



def redraw_ammo(game):
    pos_x = FIELD_WIDTH / 2
    pos_y = 20
    if game["ammo"].get() > 0:
        AMMO = glv.CANVAS.find_overlapping(pos_x - 10, pos_y - 10, pos_x + 10, pos_y + 10)
        for elem in AMMO:
            if glv.CANVAS.type(elem) == 'text':
                glv.CANVAS.delete(elem)
        glv.CANVAS.create_text(pos_x, pos_y, text=f'Ammo: {game["ammo"].get()}', fill="white")        
    else:
        AMMO = glv.CANVAS.find_overlapping(pos_x - 10, pos_y - 10, pos_x + 10, pos_y + 10)
        for elem in AMMO:
            if glv.CANVAS.type(elem) == 'text':
                glv.CANVAS.delete(elem)
        glv.CANVAS.create_text(pos_x, pos_y, text='Ammo: No Ammo', fill="red")

def explode_enemy_randomly(game, enemy):  # Function for drawing explosion when enemy destroyed
    enemy_pos = glv.CANVAS.coords(enemy.canvid)
    start_x, start_y = enemy_pos[0], enemy_pos[1]

    pieces_number = random.randint(6, 8)
    for _ in range(pieces_number):
        dx = random.randint(-3, 3)   # moving piece every tick
        dy = random.randint(-4, 4)   # horizontal displacements is random, vertical displacements - down (and up) at different speeds

        x = start_x + 5 * dx
        y = start_y + 5 * dy

        piece = Dead_Piece(x, y, dx, dy)
        game["dead_pieces"].append(piece)


def explode_from_all_sides(game, bonus):  # One more function for drawing explosion when enemy destroyed with different effect (in circle)
    bonus_pos = glv.CANVAS.coords(bonus.canvid)
    start_x, start_y = bonus_pos[0], bonus_pos[1]
    pieces_number = random.randint(10, 15)
    delta_radius = 12 / pieces_number
    for i in range(pieces_number):
        angle = math.radians(i * (360 / pieces_number))
        dx = delta_radius * math.cos(angle)
        dy = delta_radius * math.sin(angle)
        x = start_x + 5 * dx
        y = start_y + 5 * dy
        piece = Dead_Piece(x, y, dx, dy)
        game["dead_pieces"].append(piece)




def do_game_over(game):
    reset_game(game)  # removing the keypress handlers
    if not glv.top10_scores:
        top_scores = open(SCORES_DIR_NAME,"w")
        top_scores.write(str(game["score"]) + "\n")
        top_scores.close()
        glv.top10_scores.append(game["score"])
    else: 
        glv.top10_scores.append(game["score"])
        glv.top10_scores = sorted(glv.top10_scores, reverse=True)
        glv.top10_scores = glv.top10_scores[:10]

        top_scores = open(SCORES_DIR_NAME,"w")
        for i in glv.top10_scores:
            top_scores.write(str(i)+"\n")
        top_scores.close()


    glv.CANVAS.create_text(FIELD_WIDTH / 2, FIELD_HEIGHT / 2 - 30, font=("BRUSH SCRIPT MT", 50, "bold"),
                       text="Game Over...", fill="#D20606")
    glv.CANVAS.create_text(FIELD_WIDTH / 2, FIELD_HEIGHT / 2 + 30, font=("BRUSH SCRIPT MT", 30, "bold"),
                       text=f'Score: {game["score"]}', fill="#D20606")

    BUTTONS["retry"].place(x=100, y=FIELD_HEIGHT - 100, width=80, height=40)  # top-left corner

    BUTTONS["quit"].place(x=FIELD_WIDTH - 180, y=FIELD_HEIGHT - 100, width=80, height=40)  
    BUTTONS["go_main_menu"].place(x=(FIELD_WIDTH-160)/2, y=FIELD_HEIGHT - 100, width=160, height=50)
    


def do_game_win(game):      # when player passed a level 
    reset_game(game)    # removing the keypress handlers
    game["hardness"] += 1
        
    glv.current_score=game["score"]
    glv.CANVAS.create_text(FIELD_WIDTH/2, 60, font=("ARIAL", 10), text="TIP: If you want to save your score - press 'go main menu' or 'quit' \n Don't close the game with alt+f4 or cross in the corner",
                       fill="yellow")

    glv.CANVAS.create_text(FIELD_WIDTH / 2, FIELD_HEIGHT / 2 - 30, font=("BRUSH SCRIPT MT", 50, "bold"), text="You Win!",
                       fill="#69BC4A")
    glv.CANVAS.create_text(FIELD_WIDTH / 2, FIELD_HEIGHT / 2 + 30, font=("BRUSH SCRIPT MT", 30, "bold"),
                       text=f'Score: {game["score"]}', fill="#69BC4A")

    BUTTONS["continue"].place(x=100, y=(FIELD_HEIGHT - 100), width=80, height=40)  # top-left corner
    BUTTONS["quit"].place(x=FIELD_WIDTH - 180, y=FIELD_HEIGHT - 100, width=80, height=40)  # top-left corner
    BUTTONS["go_main_menu"].place(x=(FIELD_WIDTH-160)/2, y=FIELD_HEIGHT - 100, width=160, height=50)
    
    def save_and_quit():
        glv.top10_scores.append(glv.current_score)
        glv.top10_scores = sorted(glv.top10_scores, reverse=True)
        glv.top10_scores = glv.top10_scores[:10]

        top_scores = open(SCORES_DIR_NAME,"w")
        for i in glv.top10_scores:
            top_scores.write(str(i)+"\n")
        top_scores.close()
        quit()
    
    def save_and_go_main_menu():
        glv.top10_scores.append(glv.current_score)
        glv.top10_scores = sorted(glv.top10_scores, reverse=True)
        glv.top10_scores = glv.top10_scores[:10]
        
        top_scores = open(SCORES_DIR_NAME,"w")
        for i in glv.top10_scores:
            top_scores.write(str(i)+"\n")
        top_scores.close()
        main()
    
    def level_continue():
        game["level"] += 1
        BUTTONS["continue"].place_forget()
        BUTTONS["quit"].place_forget()
        runlevel(game)

    BUTTONS["go_main_menu"].configure(command=save_and_go_main_menu)
    BUTTONS["quit"].configure(command=save_and_quit)
    BUTTONS["continue"].configure(command=level_continue)  # click handler can be changed if needed


def reset_game(game):
    glv.CANVAS.delete(tk.ALL)

    game["enemies"].clear()
    game["bullets"].clear()
    game["players"].clear()
    game["dead_pieces"].clear()
    game["bonuses"].clear()


    # unbinding keyPress handlers from deleted players
    for char in ["a","d","w", "j", "l", "i", "r"]:
        glv.ROOT.unbind_all("<KeyPress-%s>" % char)
        glv.ROOT.unbind_all("<KeyRelease-%s>" % char)








def get_killed(bullet, items):
    bullet_pos = glv.CANVAS.bbox(bullet.canvid)
    for item in items:
        item_pos = glv.CANVAS.bbox(item.canvid)
        if (item_pos[0] <= bullet_pos[0] <= item_pos[2] and item_pos[1] <= bullet_pos[1] <= item_pos[3]
                or item_pos[0] <= bullet_pos[2] <= item_pos[2] and item_pos[1] <= bullet_pos[3] - 30 <= item_pos[3]):
            return item
    return None


def redraw_score(game):
    pos_x = 0.1 * FIELD_WIDTH
    pos_y = 0.05 * FIELD_HEIGHT

    # Find an already drawn score in the corner of the screen and delete it before drawing a new one
    score = glv.CANVAS.find_overlapping(pos_x - 10, pos_y - 10, pos_x + 10, pos_y + 10)
    for elem in score:
        if elem and glv.CANVAS.type(elem) == 'text':
            glv.CANVAS.delete(elem)
    glv.CANVAS.create_text(pos_x, pos_y, text=f'Score: {game["score"]}', fill="white")


def is_outside_borders(item):
    # This function checks if the window element is within the window borders.
    item_pos = glv.CANVAS.bbox(item.canvid)
    left_top_x, left_top_y = item_pos[0], item_pos[1]
    right_bottom_x, right_bottom_y = item_pos[2], item_pos[3]
    return (left_top_x < 0
            or left_top_y < 0
            or right_bottom_x > FIELD_WIDTH
            or right_bottom_y > FIELD_HEIGHT - PLAYER_HEIGHT - FLOOR_SIZE)


if __name__ == '__main__':
    # Create all needed buttons on the start, then just draw/hide them when needed 
    BUTTONS["run"] = tk.Button(glv.ROOT, text="start", fg="white", command=rungame, name="button1", background="green")
    BUTTONS["continue"] = tk.Button(glv.ROOT, text="continue", fg="white", name="continueButton", background="#C88539")
    BUTTONS["retry"] = tk.Button(glv.ROOT, text="retry", command=rungame, fg="white", name="retryButton",background="#C88539")
    BUTTONS["quit"] = tk.Button(glv.ROOT, text="quit", fg="white", command=quit, name="quitButton", background="#C88539")
    BUTTONS["go_main_menu"] = tk.Button(glv.ROOT, text="Go to main menu", command=main, fg="white", name="go_main_menu",background="#C88539")
    BUTTONS["upgrades_menu"] = tk.Button(glv.ROOT, text="Upgrades", command=upgrades, fg="white", name="upgrades_menu",background="#C88539")
    BUTTONS["damage_upgrade_level"] = tk.Button(glv.ROOT, text=f"Damage upgrade level: {glv.damage_upgrade_level} ", fg="white", name="damage_upgrade_level",background="#45AC4A")
    BUTTONS["player_speed"] = tk.Button(glv.ROOT, text=f"Player speed upgrade: {glv.player_speed} ", fg="white", name="player_speed_upgrade", background="#45AC4A")
    BUTTONS["bullet_quantity_upgrade_level"] = tk.Button(glv.ROOT, text=f"Bullet quantity upgrade level: {glv.bullet_quantity_upgrade_level} ", fg="white", name="bullet_quantity_upgrade_level",background="#45AC4A")
    BUTTONS["speed_of_bullet_upgrade_level"] = tk.Button(glv.ROOT, text=f"Speed of bullet upgrade: {glv.speed_of_bullet_upgrade_level} ", fg="white", name="speed_of_bullet_upgrade_level",background="#45AC4A")
    
    BUTTONS["easyHardness"] = tk.Radiobutton(text="Easy", variable=choose_difficulty, value=0, bg="black", fg="white")
    BUTTONS["midHardness"] = tk.Radiobutton(text="Medium", variable=choose_difficulty, value=7, bg="black", fg="white")
    BUTTONS["highHardness"] = tk.Radiobutton(text="Hard", variable=choose_difficulty, value=14, bg="black", fg="white")
    main()
