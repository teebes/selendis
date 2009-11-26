*********
Stark API
*********

Stark implements a RESTful API so that any client can interact with the world.

.. _player:

Player
======

``/api/players/me.(json|xml)``:

*Returns the information about the logged in user, including which room they are in and what they are holding in their inventory.*

* Methods: GET, PUT
* Returns:

  * ``name``: the player's name
  * ``level``: the player's level
  * ``items``: the items in the player's inventory (see :ref:`item`)
  * ``room``: the the player is in (see :ref:`room`)
  * ``id``: the player's id
  * ``builder_mode``: whether the player is in builder mode
  * ``mp``: the player's current movement points
  * ``max_mp``: the player's max possible movement points

* PUT arguments:

  * ``xpos``: must be provided with ypos, will change the player's location 
  * ``ypos``: must be provided with xpos, will change the player's location

.. _room:

Room
====

``/api/rooms/<id>.(json|xml)``:

*Returns room information to players and allows builders to manipulate rooms.*

* Methods: GET, POST, PUT, DELETE
* Returns:

  * ``xpos``: the x coordinate of the room
  * ``ypos``: the y coordinate of the room
  * ``title``: the name of the room  
  * ``description``: the description of the room
  * ``type``: the type of the room (indoors, road, field, water, city or shop)
  * ``items``: the items that are up for grabs in the room (children: ``type``, ``id``, ``name``)
  * ``north``: how this room connects to the north
  * ``east``: how this room conncts to the east
  * ``south``: how this room conncts to the south
  * ``west``: how this room conncts to the west
  * ``mob_related``: the mobs currently in the room (children: ``name``, ``id``)
  * ``player_related``: the players currently in the room (children: ``name``, ``id``)

* POST arguments:

  * ``xpos``: the y coordinate of the new room
  * ``ypos``: the x coordinate of the new room
  
* PUT arguments:

  * ``north``, ``east``, ``south`` or ``west`` (optional): if the arg value is 'toggle', the room's connection in the corresponding direction will be created or disabled
  * ``title``: (optional): the new room title
  * ``description``: (optional): the new room description
  * ``type``: (optional): the new room type

.. _map:

Map
===

``/api/map.(json|xml)``:

*Returns all of the necessary information to draw a map around the player's location*

* Methods: GET
* Returns:

  * ``starting_point``: The coordinates of the point to the most northwest of the map so that the graphical client knows how to interpret the position of the other points
  * ``player_position``: The coordinates of the player's current position
  * ``rooms``: the list of the room objets that make up the map (see :ref:`room`)

.. _item:

Item
====

``/api/items/<id>.(xml|json)``:

*Allows manipulation of items which are either being carried by players or sitting in rooms*

* Methods: GET, PUT
* Returns:

  * ``id``: the id of the item
  * ``type``: the type of the item (weapon, requipment, sustenance, misc)
  * ``name``: the name of the item
  
* PUT arguments:

  * ``owner_type``: Must be provided with ``owner_id``, determines who owns the item (player, mob or room)
  * ``owner_id`` (optional): Must be provided with ``owner_type``, determines who owns the item
  
.. _message:
  
Message
=======

*Messages can be sent in game, either in the form of chats, which are visible by everyone, or private messages intended only for specific players*

* Methods: GET, POST
* Returns:

  * ``content``: the contents of the message
  * ``type``: the type of the message, currently:
  
    * ``chat``: messages visible by everyone
    * ``clan``: player-to-clan messages
    * ``direct``: direct player-to-player messages
    * ``notification``: system messages such as players moving around
    
  * ``created``: when the message was created
  * ``source``: the label for the source of the message (often the originator's name)
  
* POST arguments:

  * ``content``: the contents of the message
  * ``type``: what kind of message
  * ``message``: the actual message