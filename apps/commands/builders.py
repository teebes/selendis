from stark.apps.commands import Command
from stark.apps.world import models as world_models
from stark.apps.world.models import ItemInstance, Room

register = [
    'list',
    'load',
    'jump',
]

def _get_world_model_for_type(type):
    # DRY
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
            self.anima.room.notify("%s makes a %s out of thin air." %
                                    (self.anima.get_name(), base.name))
            return "You make a %s out of thin air " % base.name, ['player']

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