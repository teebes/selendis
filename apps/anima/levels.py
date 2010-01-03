LEVELS = [
    [1, 0], # first
    [2, 10], # 10 more
    [3, 20], # 10 more
    [4, 35], # 15 more
    [5, 55], # 20 more
    [6, 80], # 25 more
    [7, 110], # 30 more
    [8, 150], # 40 more
    [9, 200], # 50 more
    [10, 260], # 60 more
    [11, 330], # 70 more
]

def get_level_for_exp(experience):
    # returns a tuple (level, next exp requirement)

    for level in sorted(LEVELS, reverse=True):
        (number, requirement) = level
        if experience > requirement:
            if level == LEVELS[-1]: # last level, return 0 tnl
                return (number, requirement)
            else:
                return (number, LEVELS[LEVELS.index(level) + 2][1])
    
    # if a user didn't get a level for any exp, then the levels are
    # misconfigured
    raise Exception('Levels are misconfigured')
