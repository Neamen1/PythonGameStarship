import os
from global_constans import SCORES_DIR_NAME, DATA_DIR_NAME
def read_score(top10_scores):           # loading scores
    if not os.path.exists(SCORES_DIR_NAME):
        top_scores = open(SCORES_DIR_NAME,"w")
        top_scores.close()
    top_scores = open(SCORES_DIR_NAME,'r')
    for top_line in top_scores:  
        if top_line == '\n':
            continue
        top10_scores.append(int(top_line))
    top_scores.close()

def read_data():       # reading game data from data file
    game_money = open(DATA_DIR_NAME, 'r')
    for mon in game_money:
        if mon.startswith("money:"):
            coins = int(mon.replace("money:", ''))
        elif mon.startswith("damage_upgrade_level:"):
            damage_upgrade_level = int(mon.replace("damage_upgrade_level:", ''))
        elif mon.startswith("player_speed:"):
            player_speed = float(mon.replace("player_speed:", ''))
        elif mon.startswith("bullet_upgrade_level:"):
            bullet_quantity_upgrade_level = int(mon.replace("bullet_upgrade_level:", ''))
        elif mon.startswith("speed_of_bullet_upgrade_level:"):
            speed_of_bullet_upgrade_level = int(mon.replace("speed_of_bullet_upgrade_level:", ''))
    game_money.close()
    return coins, damage_upgrade_level, player_speed, bullet_quantity_upgrade_level, speed_of_bullet_upgrade_level