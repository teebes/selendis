from stark import config
from stark.apps.anima.models import Player, Mob
from stark.utils import QuerySetChain

def tick_regen():
    """
    Regen every anima in the world that qualifies during a big tick.
    
    This entire function is a DRY abomination
    
    There is an architectural problem right now that requires the checks for
    max_hp and max_mp to be added as a where clause for performance reasons.
    But that is logic repeated from their respective property definitions,
    which violates DRY. This is because there is currently no way for Django's
    ORM to do queries based on model properties.
    
    Also, because there is no way to combine querysets that have a common
    abstract base class, the same queries need to be applied to both players
    and mobs.
    """
    
    # TODO: regen rates should be smarter than just constants
    TICK_HP_REGEN_RATE = getattr(config, 'TICK_HP_REGEN_RATE', 4)
    TICK_MP_REGEN_RATE = getattr(config, 'TICK_MP_REGEN_RATE', 20)

    players = Player.objects.filter(status='logged_in')
    mobs = Mob.objects.all()
    
    # Moves
    for player in players.extra(where=['mp < mp_base']):
        player.regen('mp', TICK_MP_REGEN_RATE)
    for mob in mobs.extra(where=['mp < mp_base']):
        mob.regen('mp', TICK_MP_REGEN_RATE)

    # Health
    for player in players.extra(where=["hp < hp_base +"
                                       "constitution * 10 + (level - 1) * 2"]):
        player.regen('hp', TICK_HP_REGEN_RATE)
    for mob in mobs.extra(where=["hp < hp_base +"
                                      "constitution * 10 + (level - 1) * 2"]):
        mob.regen('hp', TICK_HP_REGEN_RATE)
