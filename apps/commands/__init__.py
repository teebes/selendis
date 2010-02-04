from stark.apps.anima.models import Message

class Command(object):
    """
    Central command processing object.
    Automatically provides help options based on docstrings
    """
    
    def __init__(self, anima):
        self.anima = anima

    def execute(self, raw_cmd):
        self.raw_cmd = raw_cmd
        self.tokens = filter(lambda x: x, raw_cmd.split(' '))

class Help(Command):
    """Provides information on the specified command"""
    
    template = "help [<topic>]"
    
    def call_1(self, message):
        """
            self.notify('Commands:')
            self.notify('- north, east, south, west, kill')
            self.notify('- get, drop, put, wear, wield, remove')
            self.notify('- chat, say, help')
            if self.builder_mode:
                self.notify('Admin Commands:')
                self.notify('- list, load')        
        """

class Chat(Command):
    """Sends a chat message that all players will see in their console log,
    if they have chat enabled."""

    template = "chat <message>"
    
    def call_1(self, message):
        message = Message.objects.create(
            created=datetime.datetime.now(),
            type='chat',
            content=message,
            author=self.anima,
        )
        return ['log']

class Say(Command):
    """Say something in the room you're in. All players in that room will see
    what you said in their console log"""
    
    template = "say <message>"
    
    def call_1(self, message):
        self.anima.room.notify(
            "%s says %s'" % (self.get_name(), message),
            source={'anima': self.anima, 'message': message},
        )

class Get(Command):
    """
    get <item> [<container>]
    """

    def call_1(self): pass
        

    """
        # - say -
        if tokens[0] == 'say':
            if len(tokens) < 2:
                self.notify('Usage: say message')
                return
            self.room.notify("%s says '%s'" % (self.get_name(), cmd[4:]))
            return

        # - directions -
        if tokens[0] in ('north', 'n'):
            return self.move(xpos=self.room.xpos, ypos=self.room.ypos - 1)
        elif tokens[0] in ('east', 'e'):
            return self.move(xpos=self.room.xpos + 1, ypos=self.room.ypos)
        elif tokens[0] in ('south', 's'):
            return self.move(xpos=self.room.xpos, ypos=self.room.ypos + 1)
        elif tokens[0] in ('west', 'w'):
            return self.move(xpos=self.room.xpos - 1, ypos=self.room.ypos)

        # - wear / wield -
        if tokens[0] in ('wear', 'wield'):
            if len(tokens) < 2:
                self.notify('Usage: wear item')
                return
            items = find_items_in_container(tokens[1], self.inventory())
            for item in items:
                self.wear(item)
            if not items:
                self.notify('You have no %s to wear.' % tokens[1])
                return

        # - remove -
        if tokens[0] == 'remove':
            if len(tokens) < 2:
                self.notify('Usage: remove item')
                return
            eq = filter(lambda x: x, self.equipment().values())
            items = find_items_in_container(tokens[1], eq)
            if items:
                self.remove(items[0])
            else:
                self.notify('You are not wearing a %s.' % tokens[1])
                return

        # - get -
        if tokens[0] == 'get':
            # simple get from room
            if len(tokens) == 0:
                self.notify('Usage: get item [container]')
                return
            elif len(tokens) == 2:
                items = find_items_in_container(tokens[1],
                                                self.room.items.all())
                for item in items:
                    self.get_item(item)
                if not items:
                    self.notify('There is no %s in this room.' % tokens[1])
                    return
            
            # get from container
            elif len(tokens) >= 3:
                # try to get the container from the player's equipment, inv
                # or the room
                eq = filter(lambda x: x, self.equipment().values())
                container = find_items_in_container(tokens[2], eq,
                                                    find_container=True)
                if not container:
                    container = find_items_in_container(tokens[2],
                                                        self.inventory(),
                                                        find_container=True)
                if not container:
                    container = find_items_in_container(tokens[2],
                                                        self.room.items.all(),
                                                        find_container=True)
                
                # if no suitable container has been found, raise eror
                if not container:
                    self.notify(error = 'No such container: %s' % tokens[2])
                    return
                
                # get the item from the found container
                # TODO: should this support getting stuff from
                # multiple container?
                items = find_items_in_container(tokens[1],
                                                container[0].owns.all())

                for item in items:
                    self.get_item_from_container(item)

                if not items:
                    self.notify('There is no %s in %s' %
                                    (tokens[1], tokens[2]))
                    return

        # - put -
        if tokens[0] == 'put':
            if len(tokens) < 3:
                self.notify("Usage: put item container")
                raise Exception('Not enough tokens for put command')
            else:
                # get the items that the user wants to put somewhere
                items = find_items_in_container(tokens[1], self.inventory())
                if not items:
                    self.notify('There is no %s in your inventory' % tokens[1])
                    return
                
                # get the best match from eq, inv and room
                eq = filter(lambda x: x, self.equipment().values())
                containers = find_items_in_container(tokens[2], eq,
                                                     find_container=True)
                if not containers:
                    containers = find_items_in_container(tokens[2],
                                                         self.inventory(),
                                                         find_container=True)
                if not containers:
                    containers = find_items_in_container(tokens[2],
                                                         self.room.items.all(),
                                                         find_container=True)
                if not containers:
                    self.notify('There is no %s in your inventory' % tokens[2])
                    return
                
                for item in items:
                    self.put_item_in_container(item, containers[0])

        # - drop -
        if tokens[0] == 'drop':
            if len(tokens) < 2:
                self.notify('Usage: drop item')
                return
            items = find_items_in_container(tokens[1], self.inventory())
            for item in items:
                self.drop_item(item)
            if not items:
                self.notify('You are not carrying a %s.' % tokens[1])
                return

        # - give -
        if tokens[0] == 'give':
            if len(tokens) < 3:
                self.notify('Usage: give item target')
                return
            items = find_items_in_container(tokens[1], self.inventory())
            if not items:
                self.notify("You are not carrying a %s" % tokens[1])
                return
            target = None
            for player in self.room.player_related.all():
                if tokens[2] in (player.id, player.name):
                    target = player
                    break
            if not target:
                self.notify("No-one by the name %s here." % tokens[2])
                return
            for item in items:
                self.give_item(item, target)

        # - kill -
        if tokens[0] == 'kill':
            if len(tokens) < 2:
                self.notify('Usage: kill target')
                return
            target = None
            for player in self.room.player_related.all():
                if tokens[1] in (player.id, player.name):
                    self.engage('player', player.id)
                    return
            for mob in self.room.mob_related.all():
                if tokens[1] in [mob.id] + mob.name.split(' '):
                    self.engage('mob', mob.id)
                    return

        # - builder only commands -
        
        # list
        if tokens[0] == 'list':
            if not self.builder_mode:
                return
            if len(tokens) < 2:
                self.notify('Usage: list type')
                return
            # get the type
            from stark.apps.world import models as world_models
            type = tokens[1][0].upper() + tokens[1][1:].lower()
            try:
                o = getattr(world_models, type)
            except AttributeError:
                self.notify("No such type '%s'" % tokens[1])
                return
            self.notify("%s:" % type)
            # get all items of that type
            for item in o.objects.all():
                self.notify("- %s [%s]" % (item.name, item.id))
            return
        
        # load
        if tokens[0] == 'load': # load type id
            if not self.builder_mode:
                return
            elif len(tokens) < 3:
                self.notify('Usage: load type id')
                return
            # get the type
            from stark.apps.world import models as world_models
            type = tokens[1][0].upper() + tokens[1][1:].lower()
            try:
                o = getattr(world_models, type)
            except AttributeError:
                self.notify("No such type '%s'" % tokens[1])
                return
            # get the base off the type and id
            try:
                base = o.objects.get(pk=tokens[2])
            except o.DoesNotExist:
                self.notify("No such %s ID: %s" % (type, tokens[2]))
                return
            ItemInstance.objects.create(base=base, owner=self)
            self.room.notify("%s makes a %s out of thin air." %
                             (self.get_name(), base.name))
            return
        
        # - jump -
        if tokens[0] == 'jump':
            if not self.builder_mode:
                return
            if len(tokens) < 2:
                self.notify('Usage: jump [id (x y)]')
                return
            elif len(tokens) == 2: # id passed
                try:
                    room = Room.objects.get(pk=tokens[1])
                    self.room = room
                    self.save()
                except Room.DoesNotExist: return
            elif len(tokens) >= 3: # x + y passed
                try:
                    room = Room.objects.get(xpos=tokens[1], ypos=tokens[2])
                    self.room = room
                    self.save()
                except Room.DoesNotExist: return
            self.room.notify('%s disappears in a cloud of white smoke.' % self.get_name())    
    """ 