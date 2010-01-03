import math
import random

def determine_attack_outcome(offense, defense):
    """
    attack logic hook. Needs to return a tuple (hit, damage), where hit is
    a boolean of whether it was a hit (True) or a miss (False). Meant to
    be overwritten.
    """
    # -- get the offense data
    offense_score = 10
    damage = 1
    # add weapon damage
    if offense.main_hand:
        rolls = offense.main_hand.base.num_dice
        max = offense.main_hand.base.num_faces
        damage += rolls * random.randint(1, max)
    
    # -- get the defense data
    defense_scores = [10]
    mitigation = 70
    
    # go through the defenses
    hit = True
    for defense_score in defense_scores:
        if defense_score > offense_score:
            # defense worked, it's a miss
            hit = False
            break
    
    # calculate damage
    if hit:
        damage = int(math.ceil(damage * float(mitigation) / 100))
    else:
        damage = 0
    
    return (hit, damage)