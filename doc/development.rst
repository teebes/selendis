***********
Development
***********

Source Code
===========

The source code for this project is hosted on
github: http://github.com/teebes/stark

According to the latest
`github graph <http://github.com/teebes/stark/graphs/languages>`_ at the time
of this writing, it is 66% JavaScript and 34% Python.

What I can say for sure is that it's 95% unfinished and I definitely need all
the help I can get, from building a convincing starting world to the browser
client to the backend. So if you want to help drop me a line
`on twitter <http://twitter.com/teebesz>`_.

Road Map
========

Everything still needs to be built at this point so any improvement is good.
That being said, generally I'm trying to focus first more on the server side
while only building a good enough client to basically test what's going on
underneath. The idea is that while eventually other clients may be developped
to interact with the world, the backend will need to have a solid foundation
for that to happen.

Still to be coded:

* Regen system: This should be next. HP/MP need to regen regularly, which of course means that movement needs to cost something, which means a MP system needs to be defined
* Combat system:

  * round system where each fighter does damage to the other based on n-sided die rolls
  * special attacks like bash/stun, interrupts, stabs

* Stats system: HP, SP, MP, Str, Int, Wil, Dex, the usual stuff
* Environment: smart mobs (let's start with shopkeepers), better items, spawn control