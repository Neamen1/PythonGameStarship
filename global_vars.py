import read_game_data as rgd
import tkinter as tk
from global_constans import FIELD_WIDTH, FIELD_HEIGHT

coins, damage_upgrade_level, player_speed, bullet_quantity_upgrade_level, speed_of_bullet_upgrade_level = rgd.read_data()
top10_scores=[]
rgd.read_score(top10_scores)
current_score=None

ROOT = tk.Tk()      # tkinter root variable 
CANVAS = tk.Canvas(ROOT, width=FIELD_WIDTH, height=FIELD_HEIGHT, bg="black", highlightthickness=0)      # setting window parameters
CANVAS.pack()