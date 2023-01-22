import math
import os
import random
import time
import tkinter as tk
from PIL import Image, ImageTk  # Pillow library


TICK = round(1000 / 60)  # Frame rate in milliseconds

FIELD_WIDTH = 600       # main window width and height
FIELD_HEIGHT = 700

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 30
FLOOR_SIZE = 10         # bottom zone size

DEFAULT_ENEMIES_NUMBER = 10

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
IMAGES_DIR = os.path.join(PROJECT_DIR, 'images')                # local path to images
SCORES_DIR_NAME = os.path.join(PROJECT_DIR ,"topscores.txt")    # path to scores file
MONEY_DIR_NAME = os.path.join(PROJECT_DIR, 'game_money.txt')    # path to data file


ENEMY_IMAGE_LIGHT = 'light_alien.png'       # setting images names
ENEMY_IMAGE_MEDIUM = 'medium_alien.png'
ENEMY_IMAGE_HEAVY = 'heavy_alien.png'
ENEMY_IMAGE_BOSS = 'boss.png'
PLAYER1_IMAGE = 'ship-red-39x30.png'
PLAYER2_IMAGE = 'ship-purple-39x30.png'

ROOT = tk.Tk()      # tkinter root variable 
CANVAS = tk.Canvas(ROOT, width=FIELD_WIDTH, height=FIELD_HEIGHT, bg="black", highlightthickness=0)      # setting window parameters
CANVAS.pack()


choose_difficulty = tk.IntVar()     # in-game difficulty 
BUTTONS = {}        # all buttons are stored in dictionary


top10_scores=[]
top10_scores_win=None
def read_score():           # loading scores
    if not os._exists(SCORES_DIR_NAME):
        top_scores = open(SCORES_DIR_NAME,"w")
        top_scores.close()
    top_scores = open(SCORES_DIR_NAME,'r')
    for top_line in top_scores:  
        if top_line == '\n':
            continue
        top10_scores.append(int(top_line))
    top_scores.close()


# global variables
coins = None
damage_upgrade_level = None
player_speed = None
bullet_quantity_upgrade_level = None
speed_of_bullet_upgrade_level = None
MONEY_DIR_NAME = os.path.join(PROJECT_DIR, 'game.txt')
def read_money():       # reading game data from data file
    game_money = open(MONEY_DIR_NAME, 'r')
    for mon in game_money:
        if mon.startswith("money:"):
            global coins
            coins = int(mon.replace("money:", ''))
        elif mon.startswith("damage_upgrade_level:"):
            global damage_upgrade_level
            damage_upgrade_level = int(mon.replace("damage_upgrade_level:", ''))
        elif mon.startswith("player_speed:"):
            global player_speed   
            player_speed = float(mon.replace("player_speed:", ''))
        elif mon.startswith("bullet_upgrade_level:"):
            global bullet_quantity_upgrade_level   
            bullet_quantity_upgrade_level = int(mon.replace("bullet_upgrade_level:", ''))
        elif mon.startswith("speed_of_bullet_upgrade_level:"):
            global speed_of_bullet_upgrade_level
            speed_of_bullet_upgrade_level = int(mon.replace("speed_of_bullet_upgrade_level:", ''))
    game_money.close()
warning_text = None

read_score()
read_money()

# writing images pathes
enemy_texture_LIGHT = tk.PhotoImage(file=os.path.join(IMAGES_DIR, ENEMY_IMAGE_LIGHT))
enemy_texture_MEDIUM = tk.PhotoImage(file=os.path.join(IMAGES_DIR, ENEMY_IMAGE_MEDIUM))
enemy_texture_HEAVY = tk.PhotoImage(file=os.path.join(IMAGES_DIR, ENEMY_IMAGE_HEAVY))
enemy_texture_BOSS = tk.PhotoImage(file=os.path.join(IMAGES_DIR, ENEMY_IMAGE_BOSS))
player1_img_file = os.path.join(IMAGES_DIR, PLAYER1_IMAGE)      # player image path
player1_image = Image.open(player1_img_file).resize((PLAYER_WIDTH, PLAYER_HEIGHT))
# Image.open(file) loads image and creates image object, which ahs resize method
# resize(size) creates an image copy with new size
player1_texture = ImageTk.PhotoImage(image=player1_image) # for tkinter we need to conver image to ImageTk type instead Image type

player2_img_file = os.path.join(IMAGES_DIR, PLAYER2_IMAGE)
player2_image = Image.open(player2_img_file).resize((PLAYER_WIDTH, PLAYER_HEIGHT))
player2_texture = ImageTk.PhotoImage(image=player2_image)


def main():
    CANVAS.delete(tk.ALL)
    # Create all needed buttons on the start, then just draw/hide them when needed 
    BUTTONS["run"] = tk.Button(ROOT, text="start", fg="white", command=rungame, name="button1", background="green")
    BUTTONS["continue"] = tk.Button(ROOT, text="continue", fg="white", name="continueButton", background="#C88539")
    BUTTONS["retry"] = tk.Button(ROOT, text="retry", command=rungame, fg="white", name="retryButton",background="#C88539")
    BUTTONS["quit"] = tk.Button(ROOT, text="quit", fg="white", command=quit, name="quitButton", background="#C88539")
    BUTTONS["go_main_menu"] = tk.Button(ROOT, text="Go to main menu", command=main, fg="white", name="go_main_menu",background="#C88539")
    BUTTONS["upgrades_menu"] = tk.Button(ROOT, text="Upgrades", command=upgrades, fg="white", name="upgrades_menu",background="#C88539")
    BUTTONS["damage_upgrade_level"] = tk.Button(ROOT, text=f"Damage upgrade level: {damage_upgrade_level} ", fg="white", name="damage_upgrade_level",background="#45AC4A")
    BUTTONS["player_speed"] = tk.Button(ROOT, text=f"Player speed upgrade: {player_speed} ", fg="white", name="player_speed_upgrade", background="#45AC4A")
    BUTTONS["bullet_quantity_upgrade_level"] = tk.Button(ROOT, text=f"Bullet quantity upgrade level: {bullet_quantity_upgrade_level} ", fg="white", name="bullet_quantity_upgrade_level",background="#45AC4A")
    BUTTONS["speed_of_bullet_upgrade_level"] = tk.Button(ROOT, text=f"Speed of bullet upgrade: {speed_of_bullet_upgrade_level} ", fg="white", name="speed_of_bullet_upgrade_level",background="#45AC4A")
    
    BUTTONS["quit"].place(x=FIELD_WIDTH - 180, y=FIELD_HEIGHT - 100, width=80, height=40)
    
    # (re)drawing coins amount
    global coins
    pos_1 = FIELD_WIDTH // 1.4 
    pos_2 = FIELD_HEIGHT // 2.5 
    COINS = CANVAS.find_overlapping(pos_1 - 10, pos_2 - 10, pos_1 + 10, pos_2 + 10)     
    if COINS and CANVAS.type(COINS) == 'text':
        CANVAS.delete(COINS)
    CANVAS.create_text(pos_1, pos_2, text=f'coins: {coins}', fill="white")  # creating new text

    # placing main manu buttons
    BUTTONS["top_score"] = tk.Button(ROOT, text="Top score", command=scores_func, fg="white", name="score_menu",background="#C88539")
    BUTTONS["top_score"].place(x=(FIELD_WIDTH - 80) // 3.75, y=(FIELD_HEIGHT - 65) / 2, width=80, height=65)
    
    BUTTONS["run"].place(x=(FIELD_WIDTH - 100) / 2, y=(FIELD_HEIGHT - 100) / 2, width=100, height=90)
    BUTTONS["upgrades_menu"].place(x=(FIELD_WIDTH - 80)//1.35, y=(FIELD_HEIGHT - 65) / 2, width=80, height=65)

    choose_difficulty.set(0)
    BUTTONS["easyHardness"] = tk.Radiobutton(text="Easy", variable=choose_difficulty, value=0, bg="black", fg="white")
    BUTTONS["midHardness"] = tk.Radiobutton(text="Medium", variable=choose_difficulty, value=7, bg="black", fg="white")
    BUTTONS["highHardness"] = tk.Radiobutton(text="Hard", variable=choose_difficulty, value=14, bg="black", fg="white")

    BUTTONS["easyHardness"].place(x=(FIELD_WIDTH - 100) / 2, y=(FIELD_HEIGHT - 100) / 2 + 160, height=20)
    BUTTONS["midHardness"].place(x=(FIELD_WIDTH - 100) / 2, y=(FIELD_HEIGHT - 100) / 2 + 180, height=20)
    BUTTONS["highHardness"].place(x=(FIELD_WIDTH - 100) / 2, y=(FIELD_HEIGHT - 100) / 2 + 200, height=20)
    ROOT.mainloop()

# upgrades menu
def upgrades():
    # cleaning all active objects
    CANVAS.delete(tk.ALL)   

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
    
    CANVAS.create_text(FIELD_WIDTH / 2, 50, font=("ARIAL", 10), text=f'coins: {coins}', fill="white")
    def write_to_file():        # write updated data to data file
        game_money = open(MONEY_DIR_NAME, 'w')
        game_money.write("money:"+str(coins)+"\n"+
                        "damage_upgrade_level:" + str(damage_upgrade_level)+ "\n"+
                        "player_speed:" + str(player_speed)+"\n"+
                        "bullet_upgrade_level:" + str(bullet_quantity_upgrade_level)+"\n"+
                        "speed_of_bullet_upgrade_level:" + str(speed_of_bullet_upgrade_level)+"\n")

        game_money.close()
    
    def redraw_coins_text():
        coins_text = CANVAS.find_overlapping(FIELD_WIDTH / 2 - 10, 50 - 10, FIELD_WIDTH / 2 + 10, 50 + 10)
        for elem in coins_text:
            if CANVAS.type(elem) == 'text':
                CANVAS.delete(elem)
            CANVAS.create_text(FIELD_WIDTH / 2, 50, font=("ARIAL", 10), text=f'coins: {coins}', fill="white")
    damage_upgrade_needed_coins = 200 * (damage_upgrade_level)
    #
    def buy_damage_upgrade():
        global damage_upgrade_level
        global coins
        
        damage_upgrade_needed_coins = 200 * (damage_upgrade_level)
        if damage_upgrade_level >= 20:
            BUTTONS["damage_upgrade_level"].configure(command=None, text="Max damage upgrade!")
            write_to_file()
        elif coins>=damage_upgrade_needed_coins:              # if enough money - buys upgrade
            pos_x = FIELD_WIDTH / 2
            pos_y = 20
            not_en_coins_text = CANVAS.find_overlapping(pos_x - 10, pos_y - 10, pos_x + 10, pos_y + 10)
            CANVAS.delete(not_en_coins_text)
            coins -= damage_upgrade_needed_coins
            damage_upgrade_level+=1
            damage_upgrade_needed_coins = 200 * (damage_upgrade_level)
            write_to_file()
            redraw_coins_text()
            BUTTONS["damage_upgrade_level"].configure(text=f"Damage upgrade level: {damage_upgrade_level} \n needed coins: {damage_upgrade_needed_coins}")
        else:
            CANVAS.create_text(FIELD_WIDTH / 2, 20, font=("ARIAL", 20, "bold"), text='Not enough coins!', fill="red")
    #
    player_speed_needed_coins = 250 * int((player_speed+0.1) * 10)
    def buy_player_speed():
        global player_speed
        global coins
        player_speed_needed_coins = 250 * int((player_speed+0.1) * 10)
        if player_speed >= 2:
            BUTTONS["player_speed"].configure(command=None, text="Max player speed upgrade!")
        elif coins>=player_speed_needed_coins:
            pos_x = FIELD_WIDTH / 2
            pos_y = 20
            not_en_coins_text = CANVAS.find_overlapping(pos_x - 10, pos_y - 10, pos_x + 10, pos_y + 10)
            CANVAS.delete(not_en_coins_text)
            coins -= player_speed_needed_coins
            player_speed=round(player_speed+0.1, 1)
            player_speed_needed_coins = 250 * int((player_speed+0.1) * 10)
            write_to_file()
            redraw_coins_text()
            BUTTONS["player_speed"].configure(text=f"Player speed upgrade: {player_speed} \n needed coins: {player_speed_needed_coins}")
        else: 
            CANVAS.create_text(FIELD_WIDTH / 2, 20, font=("ARIAL", 20, "bold"), text='Not enough coins!', fill="red")
    #
    bullet_upgrade_level_needed_coins = 1500*(bullet_quantity_upgrade_level+1)
    def bullet_quantity_upgrade():
        global bullet_quantity_upgrade_level
        global coins
        bullet_upgrade_level_needed_coins = 1500 * (bullet_quantity_upgrade_level+1)
        if bullet_quantity_upgrade_level >= 3:
            BUTTONS["bullet_quantity_upgrade_level"].configure(command=None, text="Max bullet quantity upgrade!")
        elif coins>=bullet_upgrade_level_needed_coins:
            pos_x = FIELD_WIDTH / 2
            pos_y = 20
            not_en_coins_text = CANVAS.find_overlapping(pos_x - 10, pos_y - 10, pos_x + 10, pos_y + 10)
            CANVAS.delete(not_en_coins_text)
            coins -= bullet_upgrade_level_needed_coins
            bullet_quantity_upgrade_level+=1
            bullet_upgrade_level_needed_coins = 1500 * (bullet_quantity_upgrade_level+1)
            write_to_file()
            redraw_coins_text()
            BUTTONS["bullet_quantity_upgrade_level"].configure(text=f"Bullet quantity upgrade level: {bullet_quantity_upgrade_level} \n needed coins: {bullet_upgrade_level_needed_coins}")
        else: 
            CANVAS.create_text(FIELD_WIDTH / 2, 20, font=("ARIAL", 20, "bold"), text='Not enough coins!', fill="red")
    #   
    speed_of_bullet_needed_coins = 300 * (speed_of_bullet_upgrade_level+1)
    def speed_of_bullet_upgrade():
        global speed_of_bullet_upgrade_level
        global coins
        speed_of_bullet_needed_coins = 300 * (speed_of_bullet_upgrade_level+1)
        if speed_of_bullet_upgrade_level >= 10:
            BUTTONS["speed_of_bullet_upgrade_level"].configure(command=None, text="Max speed of bullet upgrade!")
        elif coins>=speed_of_bullet_needed_coins:
            pos_x = FIELD_WIDTH / 2
            pos_y = 20
            not_en_coins_text = CANVAS.find_overlapping(pos_x - 10, pos_y - 10, pos_x + 10, pos_y + 10)
            CANVAS.delete(not_en_coins_text)
            coins -= speed_of_bullet_needed_coins
            speed_of_bullet_upgrade_level+=1
            speed_of_bullet_needed_coins = 300 * (speed_of_bullet_upgrade_level+1)
            write_to_file()
            redraw_coins_text()
            BUTTONS["speed_of_bullet_upgrade_level"].configure(text=f"Speed of bullet upgrade level: {speed_of_bullet_upgrade_level} \n needed coins: {speed_of_bullet_needed_coins}")
        else: 
            CANVAS.create_text(FIELD_WIDTH / 2, 20, font=("ARIAL", 20, "bold"), text='Not enough coins!', fill="red")
   
   
    BUTTONS["damage_upgrade_level"].configure(command=buy_damage_upgrade, text=f"Damage upgrade level: {damage_upgrade_level} \n needed coins: {damage_upgrade_needed_coins}")
    BUTTONS["player_speed"].configure(command=buy_player_speed, text=f"Player speed upgrade: {player_speed} \n needed coins: {player_speed_needed_coins}")
    BUTTONS["bullet_quantity_upgrade_level"].configure(command=bullet_quantity_upgrade, text=f"Bullet quantity upgrade level: {bullet_quantity_upgrade_level} \n needed coins: {bullet_upgrade_level_needed_coins}")
    BUTTONS["speed_of_bullet_upgrade_level"].configure(command=speed_of_bullet_upgrade, text=f"Speed of bullet upgrade level: {speed_of_bullet_upgrade_level} \n needed coins: {speed_of_bullet_needed_coins}")
    BUTTONS["go_main_menu"].place(x=(FIELD_WIDTH-160)/2, y=FIELD_HEIGHT - 100, width=160, height=50)  


def scores_func():        # scores menu - shows top 10 scores written in mtopscores.txt
    CANVAS.delete(tk.ALL)

    BUTTONS["run"].place_forget()
    BUTTONS["retry"].place_forget()
    BUTTONS["quit"].place_forget()
    BUTTONS["easyHardness"].place_forget()
    BUTTONS["midHardness"].place_forget()
    BUTTONS["highHardness"].place_forget()
    BUTTONS["top_score"].place_forget()
    BUTTONS["upgrades_menu"].place_forget()

    text = "Top scores: \n"
    for score in top10_scores:
        text+=str(score) + "\n"
    CANVAS.create_text(FIELD_WIDTH / 2, FIELD_HEIGHT / 2 + 30, text=f"{text}", fill="#C88539", font=("Times New Roman", 14, "bold"), justify="center")

    BUTTONS["go_main_menu"].place(x=(FIELD_WIDTH-160)/2, y=FIELD_HEIGHT - 100, width=160, height=50)  

def rungame():      # main game start function
    # removing previous elements
    CANVAS.delete(tk.ALL)
    
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
    CANVAS.delete(tk.ALL)
    BUTTONS["go_main_menu"].place_forget()
    redraw_ammo(game)
    # num of level
    pos_x = FIELD_WIDTH - (0.1 * FIELD_WIDTH)
    pos_y = .05 * FIELD_HEIGHT
    level_text = CANVAS.find_overlapping(pos_x - 30, pos_y + 10, pos_x, pos_y + 10)
    if level_text and CANVAS.type(level_text) == 'text':
        CANVAS.delete(level_text)
    
    CANVAS.create_text(pos_x, pos_y, text=f'Level: {game["level"]}', fill="white")
    # creating players

    player1 = create_player(player1_texture)
    CANVAS.move(player1, 40, 0)
    bul_color1 = "red"  # bullet color for player 1
    
    
    CANVAS.bind_all('<KeyPress-Left>', lambda e: move_player(player1, -10))
    CANVAS.bind_all('<KeyPress-Right>', lambda e: move_player(player1, 10))
    CANVAS.bind_all('<KeyPress-Return>', lambda e: perform_shooting(player1, game, bul_color1))
    game["players"].append(player1)
    
    player2 = create_player(player2_texture)
    bul_color2 = "purple"  # bullet color for player 2
    CANVAS.move(player2, -40, 0)
    CANVAS.bind_all('<KeyPress-1>', lambda e: move_player(player2, -10))
    CANVAS.bind_all('<KeyPress-2>', lambda e: move_player(player2, 10))
    CANVAS.bind_all('<KeyPress-space>', lambda e: perform_shooting(player2, game, bul_color2))
    game["players"].append(player2)
    game["start_time"] = time.time()
    if game["level"]%3==0:      # every 3rd level is boss level
        global warning_text
        warning_text = CANVAS.create_text(FIELD_WIDTH/2, FIELD_HEIGHT/2, font=("ARIAL", 20, "bold"),text="Warning! Boss level!", fill="red")        
        CANVAS.after(int((1.5-(game["hardness"]*0.03))*1000) , lambda: CANVAS.delete(warning_text))     # after some time delete warning text
    game["num_of_enemies"] = DEFAULT_ENEMIES_NUMBER + game["hardness"]
    game["bonuses"].append(Bonus())
    chanse = random.randint(1, 100)
    if chanse >= 0 and chanse <= 70:
        CANVAS.after(3500, lambda : game["bonuses"].append(Bonus(color="pink", x2=10, y2=10)))
    
    def nextstep():  # game main loop
        update_game(game)
        is_won = not game["enemies"] and not game["dead_pieces"] and game["num_of_enemies"]<1
        if not is_won and not game["is_over"]:
            CANVAS.after(TICK, nextstep)  # invoking loop again every tick, between invoking buttons input can be read
            
        elif is_won:
            do_game_win(game)
        else:
            do_game_over(game)


    global coins                # (re)drawing money text
    pos_1 = FIELD_WIDTH / 1.5 
    pos_2 = 30
    COINS = CANVAS.find_overlapping(pos_1 - 10, pos_2 - 10, pos_1 + 10, pos_2 + 10)
    if COINS and CANVAS.type(COINS) == 'text':
        CANVAS.delete(COINS)
    CANVAS.create_text(pos_1, pos_2, text=f'coins: {coins}', fill="white")

    redraw_score(game)
    CANVAS.after(1, nextstep)

def update_game_score(game,killed_enemy_health):        # score per enemy changes on different difficulties
    if game["hardness"] < 7:
        game["score"] += 1 *killed_enemy_health
    elif game["hardness"] < 14:
        game["score"] += 2*killed_enemy_health
    else:
        game["score"] += 4*killed_enemy_health
    

def update_game(game):
    global coins
    current_time = (time.time() - game["start_time"])>=(1.5-(game["hardness"]*0.03))        #(1.5-(game["hardness"]*0.1)) - period of time when new enemy is created (in seconds)
    if current_time and game["num_of_enemies"] >=1:   
        if game["level"] %3==0 and game["num_of_enemies"]%8==0:     # create boss when minimum 8 enemies units are left to spawn on level
            enemy = Enemies(shifty=0.1 + game["hardness"] * 0.1, enemy_heaviness="boss", enemy_texture=enemy_texture_BOSS)
            game["enemies"].append(enemy)
            game["num_of_enemies"] -=6
            game["start_time"] = time.time()
        elif game["num_of_enemies"] % 6 == 0:       # create heavy enemy when minimum 6 enemies units are left to spawn on level
            enemy = Enemies(shifty=0.3 + game["hardness"] * 0.1, enemy_heaviness="heavy", enemy_texture=enemy_texture_HEAVY)
            game["enemies"].append(enemy)
            game["num_of_enemies"] -=1
            game["start_time"] = time.time()
        elif game["num_of_enemies"] % 3 == 0:
            enemy = Enemies(shifty=0.3 + game["hardness"] * 0.1, enemy_heaviness="medium",enemy_texture=enemy_texture_MEDIUM)       
            game["enemies"].append(enemy)
            game["num_of_enemies"] -=1
            game["start_time"] = time.time()
        else:
            enemy = Enemies(shifty=0.3 + game["hardness"] * 0.1, enemy_heaviness="light", enemy_texture=enemy_texture_LIGHT)       
            game["enemies"].append(enemy)
            game["num_of_enemies"] -=1
            game["start_time"] = time.time()
    for bullet in game["bullets"]:
        bullet.move()
        killed_enemy = get_killed(bullet, game["enemies"])
        destroy_bonus = get_killed(bullet, game["bonuses"])
        if destroy_bonus:       # when destoying bonus boxes
            explode_from_all_sides(game, destroy_bonus)
            destroy_bonus.clear()
            game["bonuses"].remove(destroy_bonus)
            if destroy_bonus.color=="yellow":
                game["ammo"].set(game["ammo"].get() + (game["num_of_enemies"]*2 ))
            elif destroy_bonus.color=="pink":
                for enemy in game["enemies"]:
                    coins+=2
                    explode_enemy_randomly(game, enemy)
                    update_game_score(game, enemy.max_health)
                    enemy.clear()
                game["enemies"].clear()
                game["num_of_enemies"] = 0

        
        if killed_enemy:
            killed_enemy.health -= damage_upgrade_level     # Decreasing enemy HP on hit
            if killed_enemy.health > 0:
                killed_enemy.redraw_health()  # redraw health for living enemies
            else:
                # for dead enemies:
                coins+=1*(killed_enemy.max_health //2)
                game_money = open(MONEY_DIR_NAME, 'w')          # rewrite data to file
                game_money.write("money:"+str(coins)+"\n"+
                            "damage_upgrade_level:" + str(damage_upgrade_level)+ "\n"+
                            "player_speed:" + str(player_speed)+"\n"+
                            "bullet_upgrade_level:" + str(bullet_quantity_upgrade_level)+"\n"+
                            "speed_of_bullet_upgrade_level:" + str(speed_of_bullet_upgrade_level)+"\n")

                game_money.close()

                pos_1 = FIELD_WIDTH / 1.5
                pos_2 = 30
                COINS = CANVAS.find_overlapping(pos_1 - 10, pos_2 - 10, pos_1 + 10, pos_2 + 10)
                for elem in COINS:
                    if CANVAS.type(elem) == 'text':
                        CANVAS.delete(elem)
                CANVAS.create_text(pos_1, pos_2, text=f'coins: {coins}', fill="white")

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
            CANVAS.delete(piece.canvid)
            game["dead_pieces"].remove(piece)
        else:
            piece.move()
    



def redraw_ammo(game):
    pos_x = FIELD_WIDTH / 2
    pos_y = 20
    if game["ammo"].get() > 0:
        AMMO = CANVAS.find_overlapping(pos_x - 10, pos_y - 10, pos_x + 10, pos_y + 10)
        for elem in AMMO:
            if CANVAS.type(elem) == 'text':
                CANVAS.delete(elem)
        CANVAS.create_text(pos_x, pos_y, text=f'Ammo: {game["ammo"].get()}', fill="white")        
    else:
        AMMO = CANVAS.find_overlapping(pos_x - 10, pos_y - 10, pos_x + 10, pos_y + 10)
        for elem in AMMO:
            if CANVAS.type(elem) == 'text':
                CANVAS.delete(elem)
        CANVAS.create_text(pos_x, pos_y, text='Ammo: No Ammo', fill="red")

def explode_enemy_randomly(game, enemy):  # Function for drawing explosion when enemy destroyed
    enemy_pos = CANVAS.coords(enemy.canvid)
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
    bonus_pos = CANVAS.coords(bonus.canvid)
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

class Dead_Piece:
    piece_size = 5          
    color = "#EE5F10"
    def __init__(self, x, y, shift_x, shift_y):
        self.canvid = CANVAS.create_rectangle(
            x, y, x + Dead_Piece.piece_size, y + Dead_Piece.piece_size, fill=Dead_Piece.color)
        self.frames = 40
        self.shiftx = shift_x
        self.shifty = shift_y

    def move(self):
        CANVAS.move(self.canvid, self.shiftx, self.shifty)
        self.frames-=1




def do_game_over(game):
    reset_game(game)  # removing the keypress handlers
    global top10_scores
    global top10_scores_win
    if not top10_scores:
        top_scores = open(SCORES_DIR_NAME,"w")
        top_scores.write(str(game["score"]) + "\n")
        top_scores.close()
        top10_scores.append(game["score"])

    else: 
        top10_scores.append(game["score"])
        top10_scores = sorted(top10_scores, reverse=True)
        top10_scores = top10_scores[:10]

        top_scores = open(SCORES_DIR_NAME,"w")
        for i in top10_scores:
            top_scores.write(str(i)+"\n")
        top_scores.close()


    CANVAS.create_text(FIELD_WIDTH / 2, FIELD_HEIGHT / 2 - 30, font=("BRUSH SCRIPT MT", 50, "bold"),
                       text="Game Over...", fill="#D20606")
    CANVAS.create_text(FIELD_WIDTH / 2, FIELD_HEIGHT / 2 + 30, font=("BRUSH SCRIPT MT", 30, "bold"),
                       text=f'Score: {game["score"]}', fill="#D20606")

    BUTTONS["retry"].place(x=100, y=FIELD_HEIGHT - 100, width=80, height=40)  # top-left corner

    BUTTONS["quit"].place(x=FIELD_WIDTH - 180, y=FIELD_HEIGHT - 100, width=80, height=40)  
    BUTTONS["go_main_menu"].place(x=(FIELD_WIDTH-160)/2, y=FIELD_HEIGHT - 100, width=160, height=50)
    


def do_game_win(game):      # when player passed a level 
    reset_game(game)    # removing the keypress handlers
    game["hardness"] += 1
    
    global top10_scores
    global top10_scores_win
    
    top10_scores_win=game["score"]
    CANVAS.create_text(FIELD_WIDTH/2, 60, font=("ARIAL", 10), text="TIP: If you want to save your score - press 'go main menu' or 'quit' \n Don't close the game with alt+f4 or cross in the corner",
                       fill="yellow")

    CANVAS.create_text(FIELD_WIDTH / 2, FIELD_HEIGHT / 2 - 30, font=("BRUSH SCRIPT MT", 50, "bold"), text="You Win!",
                       fill="#69BC4A")
    CANVAS.create_text(FIELD_WIDTH / 2, FIELD_HEIGHT / 2 + 30, font=("BRUSH SCRIPT MT", 30, "bold"),
                       text=f'Score: {game["score"]}', fill="#69BC4A")

    BUTTONS["continue"].place(x=100, y=(FIELD_HEIGHT - 100), width=80, height=40)  # top-left corner
    BUTTONS["quit"].place(x=FIELD_WIDTH - 180, y=FIELD_HEIGHT - 100, width=80, height=40)  # top-left corner
    BUTTONS["go_main_menu"].place(x=(FIELD_WIDTH-160)/2, y=FIELD_HEIGHT - 100, width=160, height=50)
    
    def save_and_quit():
        global top10_scores
        global top10_scores_win
        top10_scores.append(top10_scores_win)
        top10_scores = sorted(top10_scores, reverse=True)
        top10_scores = top10_scores[:10]

        top_scores = open(SCORES_DIR_NAME,"w")
        for i in top10_scores:
            top_scores.write(str(i)+"\n")
        top_scores.close()
        quit()
    
    def save_and_go_main_menu():
        global top10_scores
        global top10_scores_win
        top10_scores.append(top10_scores_win)
        top10_scores = sorted(top10_scores, reverse=True)
        top10_scores = top10_scores[:10]
        
        top_scores = open(SCORES_DIR_NAME,"w")
        for i in top10_scores:
            top_scores.write(str(i)+"\n")
        top_scores.close()
        main()
    
    def onclick():
        game["level"] += 1
        BUTTONS["continue"].place_forget()
        BUTTONS["quit"].place_forget()
        runlevel(game)

    BUTTONS["go_main_menu"].configure(command=save_and_go_main_menu)
    BUTTONS["quit"].configure(command=save_and_quit)
    BUTTONS["continue"].configure(command=onclick)  # click handler can be changed if needed


def reset_game(game):   # removing the keypress handlers
    # returning to main menu
    CANVAS.delete(tk.ALL)

    game["enemies"].clear()
    game["bullets"].clear()
    game["players"].clear()
    game["is_over"] = False
    game["dead_pieces"].clear()
    game["bonuses"].clear()

    # unbinding keyPress handlers from deleted players
    CANVAS.unbind_all('<KeyPress-Left>')
    CANVAS.unbind_all('<KeyPress-Right>')
    CANVAS.unbind_all('<KeyPress-Return>')

    CANVAS.unbind_all('<KeyPress-1>')
    CANVAS.unbind_all('<KeyPress-2>')
    CANVAS.unbind_all('<KeyPress-space>')


def create_player(texture):
    player_id = CANVAS.create_image(  # drawing image
        (FIELD_WIDTH - PLAYER_WIDTH) / 2,
        FIELD_HEIGHT - PLAYER_HEIGHT - FLOOR_SIZE,
        image=texture)
    return player_id


class Enemies:
    max_health = 6  # basic max_health of enemy

    def __init__(self, enemy_texture, shiftx=0, shifty=0, enemy_heaviness = "light"):
        self.enemy_heaviness = enemy_heaviness
        self.shiftx = shiftx
        self.shifty = shifty
        # position of enemy
        x = random.randrange(FIELD_WIDTH * 0.2, FIELD_WIDTH * 0.8, 5)
        y = FIELD_HEIGHT * 0.1
        enemy = CANVAS.create_image(x, y, image=enemy_texture, tag="Enemies")
        self.canvid = enemy
        if enemy_heaviness == "light":
            self.max_health = self.max_health
        elif enemy_heaviness == "medium":
            self.max_health = self.max_health*3
        elif enemy_heaviness == "heavy":
            self.max_health = self.max_health*6
        elif enemy_heaviness == "boss":
            self.max_health = self.max_health*18
       
        self.health = self.max_health
        self.health_cid = None  # Linking health bar id to enemy
        self.health_cid2 = None
        self.redraw_health()

    def move(self):
        CANVAS.move(self.canvid, self.shiftx, self.shifty)
        CANVAS.move(self.health_cid, self.shiftx, self.shifty)
        CANVAS.move(self.health_cid2, self.shiftx, self.shifty)

    def redraw_health(self):  # redraw health
        if self.health_cid:
            CANVAS.delete(self.health_cid)
        if self.health_cid2:
            CANVAS.delete(self.health_cid2)
        pos = CANVAS.bbox(self.canvid)
        width = (pos[2] - pos[0]) * (self.health / self.max_health)
        height = 10
        self.health_cid2 = CANVAS.create_rectangle(
            pos[0], pos[1] - height - 5,
            pos[0] + (pos[2] - pos[0]), pos[1] - 5,
            fill='red'
        )
        self.health_cid = CANVAS.create_rectangle(
            pos[0], pos[1] - height - 5,
            pos[0] + width, pos[1] - 5,
            fill='green'
        )

    def clear(self):
        CANVAS.delete(self.canvid)
        CANVAS.delete(self.health_cid)
        CANVAS.delete(self.health_cid2)

def move_player(player, step):
    step*=player_speed
    CANVAS.move(player, step, 0)
    player_pos = CANVAS.bbox(player)
    if player_pos[0] < FIELD_WIDTH * 0.1:
        CANVAS.move(player, -step, 0)
    elif player_pos[2] >= FIELD_WIDTH * 0.9:
        CANVAS.move(player, -step, 0)

class Bullet:
    def __init__(self, player_x, player_y, bul_color, diagonal_shift_x=0):
        self.diag_shift_x = diagonal_shift_x
        # self.canvid = CANVAS.create_rectangle(         # rectangle bullets
        #     (player_x-4), player_y-65,
        #     (player_x + 4), player_y-5,
        #     fill=bul_color, tag="bullet")
        self.canvid = CANVAS.create_oval(            # oval bullets
            (player_x-5), player_y-5-30,
            (player_x + 5), player_y-5,
            fill=bul_color, tag="bullet")
            
        
    def move(self):
        global speed_of_bullet_upgrade_level
        CANVAS.move(self.canvid, self.diag_shift_x, -20 - (speed_of_bullet_upgrade_level))

    def clear(self):
        CANVAS.delete(self.canvid)
       

def perform_shooting(player, game, bul_color):
    # function for creating a bullet
    # the movement of the bullet and the collision check is handled by the update_game function
    ammo = game["ammo"].get()
    if ammo > 0:
        player_pos = CANVAS.bbox(player)
        player_x = (player_pos[0]+player_pos[2])//2
        player_y = player_pos[1]
        bullet_shift = 15
        diagonal_shift_x = 2            # shift for additional bullets, which will go to the sides also, not just straight
        for i in range(bullet_quantity_upgrade_level):      # spawn as many bullets as the upgrade level
            shift_x=((0-bullet_quantity_upgrade_level /2)+i)*bullet_shift+bullet_shift/2
            if bullet_quantity_upgrade_level==1:
                bullet = Bullet(player_x = player_x, player_y=player_y, bul_color = bul_color,diagonal_shift_x = 0)  
            elif bullet_quantity_upgrade_level==2 and i==0:
                bullet = Bullet(player_x = player_x + shift_x, player_y=player_y, bul_color = bul_color,diagonal_shift_x = 0-diagonal_shift_x)
            elif bullet_quantity_upgrade_level == 2 and i==1:
                bullet = Bullet(player_x = player_x + shift_x, player_y=player_y, bul_color = bul_color,diagonal_shift_x = diagonal_shift_x)
            else:
                bullet = Bullet(player_x = player_x + shift_x, player_y=player_y, bul_color = bul_color,diagonal_shift_x = diagonal_shift_x*(i-1))   
            game["bullets"].append(bullet)
        game["ammo"].set(ammo - 1)


class Bonus:
    def __init__(self, color="yellow", shiftx=0, shifty=0.5, x2=0, y2=0):
        self.shiftx = shiftx
        self.shifty = shifty
        x = random.randrange(FIELD_WIDTH * 0.2, FIELD_WIDTH * 0.8, 5)
        y = random.randrange(FIELD_HEIGHT * 0.1, FIELD_HEIGHT * 0.4, 5)
        bonus_id = CANVAS.create_rectangle(x, y, x+30+x2, y+30+y2, fill=color, tag="Bonuses")
        self.color = color
        self.canvid = bonus_id
    def move(self):
        CANVAS.move(self.canvid, self.shiftx, self.shifty)
    def clear(self):
        CANVAS.delete(self.canvid)


def get_killed(bullet, items):
    for i in range(bullet_quantity_upgrade_level):
        bullet_pos = CANVAS.bbox(bullet.canvid-i)
        for item in items:
            item_pos = CANVAS.bbox(item.canvid)
            if (item_pos[0] <= bullet_pos[0] <= item_pos[2] and item_pos[1] <= bullet_pos[1] <= item_pos[3]
                    or item_pos[0] <= bullet_pos[2] <= item_pos[2] and item_pos[1] <= bullet_pos[3] - 30 <= item_pos[3]):
                return item
        return None


def redraw_score(game):
    pos_x = 0.1 * FIELD_WIDTH
    pos_y = 0.05 * FIELD_HEIGHT

    # Find an already drawn score in the corner of the screen and delete it before drawing a new one
    SCORE = CANVAS.find_overlapping(pos_x - 10, pos_y - 10, pos_x + 10, pos_y + 10)
    for elem in SCORE:
        if elem and CANVAS.type(elem) == 'text':
            CANVAS.delete(elem)
    CANVAS.create_text(pos_x, pos_y, text=f'Score: {game["score"]}', fill="white")


def is_outside_borders(item):
    # This function checks if the window element is within the window borders.
    item_pos = CANVAS.bbox(item.canvid)
    left_top_x, left_top_y = item_pos[0], item_pos[1]
    right_bottom_x, right_bottom_y = item_pos[2], item_pos[3]
    return (left_top_x < 0
            or left_top_y < 0
            or right_bottom_x > FIELD_WIDTH
            or right_bottom_y > FIELD_HEIGHT - PLAYER_HEIGHT - FLOOR_SIZE)


if __name__ == '__main__':
    main()
