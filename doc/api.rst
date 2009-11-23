*********
Stark API
*********

Player
======

``/api/players/me.(json|xml)``:

*Returns the information about the logged in user, including which room they are in and what they are holding in their inventory.*

* Methods: GET, PUT
* Returns:

  * ``name``: the player's name
  * ``level``: the player's level
  * ``items``: the player's inventory
  * ``room``: the player's room
  * ``id``: the player's id
  * ``builder_mode``: whether the player is in builder mode

* PUT arguments:

  * ``xpos`` (required): must be provided with ypos, will change the player's location 
  * ``ypos`` (required): must be provided with xpos, will change the player's location

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

  * ``xpos`` (required): the y coordinate of the new room
  * ``ypos`` (required): the x coordinate of the new room
  
* PUT arguments:

  * ``north``, ``east``, ``south`` or ``west`` (optional): if the arg value is 'toggle', the room's connection in the corresponding direction will be created or disabled
  * ``title``: (optional): the new room title
  * ``description``: (optional): the new room description
  * ``type``: (optional): the new room type

Map
===

``/api/map.(json|xml)``:

*Returns all of the necessary information to draw a map around the player's location*

* Methods: GET
* Returns:

  * ``starting_point``: The coordinates of the point to the most northwest of the map so that the graphical client knows how to interpret the position of the other points
  * ``player_position``: The coordinates of the player's current position
  * ``rooms``: the list of the room objets that make up the map
