from django.db import transaction

from stark.apps.anima.models import Player, Mob
from stark.apps.commands.models import Alias as Alias_Model
from stark.apps.world.models import Room, RoomConnector, ItemInstance
from stark.apps.world import models as world_models
from stark.apps.world.utils import find_items_in_container, can_hold_item, rev_direction, find_actionable_item

def execute_command(anima, raw_cmd, remote=False):
    tokens = filter(None, raw_cmd.split(' '))
    cmd = tokens.pop(0)
    try:
        cmd_class = globals()[cmd[0].upper() + cmd[1:].lower()]
    except KeyError:
        # if it's a player, try an alias
        if anima.__class__ == Player:
            try:
                alias = Alias_Model.objects.get(name=cmd, player=anima)
                return execute_command(anima, alias.command)
            except Alias_Model.DoesNotExist: pass
        
        anima.notify("Invalid command: '%s' - try 'help'" % cmd)
        return ['log']
    cmd_object = cmd_class(anima, raw_cmd, tokens=tokens, remote=remote)
    return cmd_object.execute()


# commands register (TODO: figure out an autoregister)
register = [
    'alias',
    'chat',
    'east',
    'drop',
    'kill',
    'get',
    'give',
    'help',
    'north',
    'put',
    'remove',
    'say',
    'south',
    'tell',
    'wear',
    'west',
    'wield',
]

# candidates to add next:
# - eq
# - inv
# - look

MOVE_COST = 2

class Command(object):
    # Abstract class, not meant to actually as anything other than a
    # base class
    
    def __init__(self, anima, raw_cmd, tokens=None, remote=False):
        """
        Calling a command remotely (by setting remote=True)
        bypasses validation and returns only
        the output. This is useful when using bots
        """
        self.anima = anima
        self.raw_cmd = raw_cmd
        self.remote = remote
        if tokens is not None:
            self.tokens = tokens
        else:
            tokens = filter(None, raw_cmd.split(' '))
            if len(tokens) == 1: # singleton commands like 'help', 'east'
                self.tokens = []
            else:
                self.tokens = tokens[1:]

    def validate_input(self):
        template_tokens = self.template.split(' ')[1:]
        # exclude optional arguments
        required_tokens = filter(
            lambda x: x and not (x[0] == '[' and x[-1] == ']'),
            template_tokens
        )
        if len(self.tokens) < len(required_tokens):
            return "%s\nUsage: %s" % (self.raw_cmd, self.template)

        return True

    @transaction.commit_on_success
    def execute(self):
        validation = self.validate_input()
        
        if validation != True:
            # validation failed if the function returned anything
            # other than True
            if self.remote:
                return validation
            else:
                self.anima.notify(validation)
                return ['log']
        
        result = self._execute()
        
        if result is None:
            # silent command
            return []
        
        if type(result) in (tuple, list):
            output, deltas = result
            if 'log' not in deltas:
                deltas.append('log')
        else:
            output, deltas = result, ['log']

        if self.remote:
            return output
        
        self.anima.notify("%s\n%s" % (self.raw_cmd, output))
        
        return deltas

class Alias(Command):
    """Aliases a command. 'alias' lists aliases, 'alias n north' will bind 'n' to 'north', 'alias n' will clear the 'n' alias."""
    template = "alias [<alias_name>] [<command>]"

    def _execute(self):
        # list aliases
        if len(self.tokens) == 0:
            aliases= Alias_Model.objects\
                        .filter(player=self.anima)\
                        .order_by('name')\
                        .values('name', 'command')
            if not aliases:
                return "No aliases defined"
            alist = ["%s: %s\n" % (x['name'], x['command']) for x in aliases]
            return ''.join(alist)
        
        # clear an alias
        elif len(self.tokens) == 1:
            print 'here'
            try:
                alias = Alias_Model.objects.get(name=self.tokens[0])
                alias.delete()
                return "Alias cleared."
            except Alias_Model.DoesNotExist:
                return "No such alias: '%s'" % self.tokens[0]
        
        # create an alias
        alias_name = self.tokens[0]
        aliased_command = ' '.join(self.tokens[1:])
        Alias_Model.objects.all()
        aliases = Alias_Model.objects.filter(player=self.anima,
                                             name=alias_name)
        if aliases:
            aliases[0].update(command=aliased_command)
        else:
            Alias_Model.objects.create(player=self.anima,
                                       name=alias_name,
                                       command=aliased_command)
        return "Alias set."

class Chat(Command):
    """Sends a chat message that all players will see in their console log, if they have chat enabled."""

    template = "chat <message>"
    
    def _execute(self):
        message = ' '.join(self.tokens)
        for player in Player.objects.filter(status='logged_in'):
            if player == self.anima:
                continue
            player.notify("%s chats '%s'" % (self.anima.get_name(), message))
        return "You chat '%s'" % message

class Direction(Command):
    def _execute(self):
        direction = self.template
        
        if self.anima.target:
            return "You cannot move while in combat."
        
        # get the connector based on the class parameters
        new_x = self.anima.room.xpos + self.delta[0]
        new_y = self.anima.room.ypos + self.delta[1]
        try:
            connector = RoomConnector.objects.get(from_room=self.anima.room,
                                                  to_room__xpos=new_x,
                                                  to_room__ypos=new_y)
        except RoomConnector.DoesNotExist:
            return "You cannot go that way."

        to_room = connector.to_room

        # unless a mob or a player in builder mode,
        # check for move points and deduct points
        if not (self.anima.__class__ == Mob or
                getattr(self.anima, 'builder_mode', False)):
            if self.anima.mp < MOVE_COST:
                return "Not enough movement points to move."
            else:
                self.anima.mp -= MOVE_COST

        # tell every player in the room the anima was in that it's gone
        self.anima.room.notify("%s leaves %s." % (self.anima.get_name(),
                                                 direction),
                               exclude = [self.anima])

        # move the user
        self.anima.room = to_room

        # save
        self.anima.save()

        # tell every player in the room the anima is moving to that it's
        # arrived
        self.anima.room.notify("%s has arrived from the %s." %
                                             (self.anima.get_name(),
                                              rev_direction(direction)),
                               exclude = [self.anima])

        return "You leave %s." % direction, ['room', 'log']

class Drop(Command):
    """Drop an item that is your inventory to the ground"""

    template = "drop <item>"

    def _execute(self):
        # get the items that match the argument
        items = find_items_in_container(self.tokens[0],
                                        self.anima.inventory)
        if not items:
            return "You are not carrying a '%s'." % self.tokens[0]
            
        source_msg = []
        room_msg = []
        for item in items:
            item.owner = self.anima.room
            item.save()
            room_msg.append("%s drops %s." % (self.anima.get_name(),
                                              item.get_name()))
            source_msg.append("You drop %s." % item.get_name())

        self.anima.room.notify('\n'.join(room_msg), exclude=[self.anima])
        return '\n'.join(source_msg), ['player', 'room']

class East(Direction):
    """Moves the player one room to the north"""
    template = "east"
    delta = (1, 0)

class Get(Command):
    """Get items from the ground or from a container such as a bag."""
    
    template = "get <item> [container]"
    
    def _get_items_in(self, container, source=None):
        """
        Common bit of code used by both get_from_room and get_from_container
        and therefore pulled out for DRY.
        room is pass True if it's a get specifically from a room,
        False if it's from any other container (so that it doesn't say
        "you get a dagger from The Central Square" but rather simply
        "you get a dagger" when from a room).
        """
        output = []
        room_output = []
        for item in container:
            # weight check
            if can_hold_item(self.anima, item):
                item.owner = self.anima
                item.save()
                
                # log to room
                room_msg = "%s gets %s" % (self.anima.get_name(),
                                           item.get_name())
                if source:
                    room_msg += " from %s" % source
                room_output.append(room_msg + '.')
                
                # log to self
                self_msg = "You get %s" % item.get_name()
                if source:
                    self_msg += " from %s" % source
                output.append(self_msg + '.')
            else:
                output.append("You can't carry %s: it's too heavy."
                              % item.get_name())

        self.anima.room.notify('\n'.join(room_output), exclude=[self.anima])
        return '\n'.join(output), ['room', 'player']

    
    def get_from_room(self):
        items = find_items_in_container(self.tokens[0],
                                        self.anima.room.items.all())
        if not items:
            return "There is no %s in this room." % tokens[1]

        return self._get_items_in(items, source=None)

    def get_from_container(self):
        # get the container
        containers = find_actionable_item(self.anima, self.tokens[1])
        
        if not containers:
            return "No such item: %s" % self.tokens[1]
        elif not containers[0].base.capacity:
            return "%s is not a container" % self.tokens[1]
        
        # get the item from the first found container
        # TODO: decide what to do about multiple containers here
        items = find_items_in_container(self.tokens[0],
                                        containers[0].owns.all())
        if not items:
            return "No '%s' found in '%s'" % (self.tokens[0], self.tokens[1])
        
        return self._get_items_in(items, source=containers[0].get_name())

    def _execute(self):
        if len(self.tokens) == 1:
            return self.get_from_room()
        else:
            return self.get_from_container()

class Give(Command):
    """Give an item to someone."""
    
    template = "give <item> <recipient>"
    
    def _execute(self):
        # find the item to give in inventory
        items = find_items_in_container(self.tokens[0],
                                        self.anima.inventory)
        if not items:
            return "You are not carrying %s." % self.tokens[0]

        # find the target in the room
        target = None
        for player in self.anima.room.player_related.all():
            if self.tokens[1] in (player.id, player.name):
                target = player
                break
        if not target:
            return "No-one by the name %s here." % self.tokens[1]
            
        # transfer each item
        output = []
        room_msg = []
        for item in items:
            # weight check
            if can_hold_item(target, item):
                output.append("You give %s to %s" % (item.get_name(),
                                                     target.get_name()))
                item.owner = self.anima
            else:
                output.append("You can't carry %s: it's too heavy"
                              % item.get_name())
        self.anima.room.notify('\n'.join(room_msg), exclude=[self.anima])
        return '\n'.join(output), ['room', 'player']

class Help(Command):
    """Help page. Also Provides information specified commands."""
    
    template = "help [<command>]"
    
    def general_help(self):
        # general help page, list the available commands
        commands = "Availble commands: ('help <topic>' for more info)\n%s" \
                        % ''.join([" %s\n" % i for i in register])

        # builder help
        if getattr(self.anima, 'builder_mode', False):
            commands += "\nBuilder commands:\n%s" \
                         % ''.join([" %s\n" % i for i in builder_register])

        return commands
    
    def topic_help(self):
        topic = self.tokens[0].lower()
        cls_name = topic[0].upper() + topic[1:].lower()
        if (getattr(self.anima, 'builder_mode', False) and topic in builder_register) or \
           topic in register:
        
            cls = globals()[cls_name]
        else:
            return ("Can't get help topic because command doesn't exist: "
                    "'%s'" % topic)

        return "Usage: %s\n%s" % (cls.template, cls.__doc__)

    def _execute(self):
        if len(self.tokens) == 0:
            return self.general_help()
        else:
            return self.topic_help()


class Kill(Command):
    """Kill someone, or something. Be careful, they will fight back!"""
    template = "kill <target>"
    
    def _execute(self):
        # try a player
        for player in self.anima.room.player_related.all():
            if self.tokens[0] in (player.id, player.name):
                self.anima.target = player
                self.anima.save()
                return "Ok."
        
        # try a mob
        for mob in self.anima.room.mob_related.all():
            if self.tokens[0] in [mob.id] + mob.name.split(' '):
                self.anima.target = mob
                self.anima.save()
                return "Ok."

        return "No-one by that name here."

class North(Direction):
    """Moves the player one room to the north"""
    template = "north"
    delta = (0, -1)    

class Put(Command):
    """Put an item in a container such as a bag."""
    
    template = "put <item> <container>"

    def _execute(self):
        # get the items that the user wants to put somewhere
        items = find_items_in_container(self.tokens[0],
                                        self.anima.inventory)
        if not items:
            return ("You are not carrying a '%s'" % self.tokens[0])
        
        # find the container
        containers = find_actionable_item(self.anima, self.tokens[1])

        if not containers:
            return "No such item: %s" % self.tokens[1]
        elif not containers[0].base.capacity:
            return "%s is not a container" % self.tokens[1]
            
        room_msg = []
        source_msg = []
        for item in items:
            # weight check
            if can_hold_item(containers[0], item):
                item.owner = containers[0]
                item.save()
                room_msg.append("%s puts %s in %s." % (
                                    self.anima.get_name(),
                                    item.get_name(),
                                    containers[0].get_name(),
                                ))
                source_msg.append("You put %s in %s." %
                              (item.get_name(), containers[0].get_name()))
                item.owner = containers[0]
                item.save()
            else:
                source_msg.append("%s cannot fit inside %s."
                                  % self.tokens[0:1])

        self.anima.room.notify('\n'.join(room_msg), exclude=[self.anima])
        return '\n'.join(source_msg), ['player', 'room']

class Remove(Command):
    """Remove a piece of equipment"""

    template = "remove <item>"
    
    def _execute(self):
        # get non-empty eq items
        eq = filter(lambda x: x, self.anima.equipment.values())
        items = find_items_in_container(self.tokens[0], eq)
        if not items:
            return "You are not wearing a %s." % self.tokens[0]
        output = []
        room_output = []
        for item in items:
            output.append("You remove %s." % item.get_name())
            room_output.append("%s removes %s." % (self.anima.get_name(),
                                                   item.get_name()))

            setattr(self.anima, item.base.slot, None)
            self.anima.save()

        self.anima.room.notify('\n'.join(room_output), exclude=[self.anima])
        return '\n'.join(output), ['player']

class Say(Command):
    """Say something in the room you're in. All players in that room will see what you said in their console log"""
    
    template = "say <message>"
    
    def _execute(self):
        message = ' '.join(self.tokens)
        self.anima.room.notify(
            "%s says '%s'" % (self.anima.get_name(), message),
            exclude=[self.anima])
        return "You say '%s'" % message

class South(Direction):
    """Moves the player one room to the south"""
    template = "south"
    delta = (0, 1)

class Tell(Command):
    """Send a direct message to a player"""
    template = "tell <player> <msg>"
    
    def _execute(self):
        try:
            target = Player.objects.get(name=self.tokens[0],
                                        status='logged_in')
        except Player.DoesNotExist:
            return "No-one by the name '%s' here." % self.token[0]
        msg = ' '.join(self.tokens[1:])
        target.notify("%s tells you '%s'" % (self.anima.get_name(), msg))
        return "You tell %s '%s'" % (self.tokens[0], msg)

class Wear(Command):
    """Wear a piece of equipment"""
    
    template = "wear <item>"
    
    def _execute(self):
        items = find_items_in_container(self.tokens[0],
                                        self.anima.inventory)
        if not items:
            return "You are not carrying '%s'." % self.tokens[0]
        
        output = []
        room_output = []
        for item in items:
            # to support both wear and wield
            if item.__class__.__name__ == "Weapon":
                wear_verb = 'wield'
            else:
                wear_verb = 'wear'
            
            if getattr(self.anima, item.base.slot):
                output.append("You're already wearing something on this slot.")
                continue
            
            # put the item on the slot
            setattr(self.anima, item.base.slot, item)
            self.anima.save()
            
            # notify room
            room_output.append("%s %ss %s." % (self.anima.get_name(),
                                               wear_verb,
                                               item.base.name))
            
            # notify player
            output.append("You %s %s." % (wear_verb, item.base.name))

        self.anima.room.notify('\n'.join(room_output), exclude=self.anima)
        return '\n'.join(output), ['player']


class West(Direction):
    """Moves the player one room to the west"""
    template = "west"
    delta = (-1, 0)

class Wield(Wear):
    """Wield a weapon"""
    
    template = "wield <weapon>"


# ------ BUILDERS ONLY ----

builder_register = [
    'list',
    'load',
    'jump',
    'order',
]

class Jump(Command):
    """Jump to the given room ID or x/y coordinates. If passing x/y, usage is: jump <x> <y>"""
    template = "jump <room_id>"

    def _execute(self):
        # get the room to jump to based on input
        if len(self.tokens) == 1: # room_id
            try:
                room = Room.objects.get(pk=self.tokens[0])
            except Room.DoesNotExist:
                return "No such room ID: %s" % self.tokens[0]
        else: # x y coords
            try:
                room = Room.objects.get(xpos=self.tokens[0],
                                        ypos=self.tokens[1])
            except Room.DoesNotExist:
                return "No room exists at coordiates (%s, %s)" % (
                                            self.tokens[0], self.tokens[1])
        
        # jump to the room
        self.anima.room = room
        self.anima.save()
        room.notify(
            '%s disappears in a cloud of white smoke.' % self.anima.get_name(),
            exclude=[self.anima]
        )

        return "You jump to %s" % room.get_name(), ['room']

def _get_world_model_for_type(type):
    # DRY - used by both List and Load
    # convert the type to the corresponding world model
    type = type[0].upper() + type[1:].lower()
    try:
        model = getattr(world_models, type)
        return model
    except AttributeError:
        return None

class List(Command):
    """List all item bases of a given type"""    
    template = "list <type>"
    
    def _execute(self):
        model = _get_world_model_for_type(self.tokens[0])
        if not model:
            return "No such type '%s'" % self.tokens[0]

        output = []
        for item in model.objects.all():
            output.append("- %s [%s]" % (item.name, item.id))
        return '\n'.join(output)

class Load(Command):
    """Load an instance of a given base"""
    template = "load <type> <id>"

    def _execute(self):
        model = _get_world_model_for_type(self.tokens[0])
        if not model:
            return "No such type '%s'" % self.tokens[0]

        # get the base
        try:
            base = model.objects.get(pk=self.tokens[1])
        except o.DoesNotExist:
            return "No such %s ID: %s" % (self.tokens[0], self.tokens[1])

        # all is well, load the item
        ItemInstance.objects.create(base=base, owner=self.anima)
        self.anima.room.notify("%s makes %s out of thin air." %
                                (self.anima.get_name(), base.name),
                                exclude=[self.anima])
        return "You make %s out of thin air " % base.name, ['player']

class Order(Command):
    """Make a mob execute the given command"""
    template = "order <mob> <cmd>"
    
    def _execute(self):
        for mob in self.anima.room.mob_related.all():
            if self.tokens[0] in [mob.id] + mob.get_name().split(' '):
                execute_command(mob, ' '.join(self.tokens[1:]), remote=True)
                break

        return None