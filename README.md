Here is a simple maze generator bazed on concepts of "rooms" and "walls".
At first, all the rooms are full and all the walls are unbroken. We put a "worm" in a room (I put it in the middle one)
and it starts to eat it's way out leaving empty rooms and broken walls behind. The worm can feel the nearby 
behind-the-wall-rooms' contents so if the room is already empty -it doesn't go there. The worm remember all it's steps 
and gets out from dead end by coming back before the first chance to turn to a new room. Once it understand all the rooms are
already empty - it's game over for the worm and we get our maze done.
No matter where I'd decide to make entrance and exit, there is always only one way between them.
