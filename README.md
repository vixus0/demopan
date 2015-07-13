
                                                 
       |                                         
     __|   _   _  _  _    __    _   __,   _  _   
    /  |  |/  / |/ |/ |  /  \_|/ \_/  |  / |/ |  
    \_/|_/|__/  |  |  |_/\__/ |__/ \_/|_/  |  |_/
                             /|                  
                             \|                  

             A simple Steam demo organiser.


Requirements
------------

  * Linux
  * Steam
  * inotify-tools
  * Python 3


Usage
-----

demopan.py [--tf] [--demos] [--gameid]

  * tf: The location of your TF2 (or other game) directory.
  * demos: The place you want to save your demos.
  * gameid: The Steam game ID (eg. 440 for TF2)

Note, this will run the game for you. You will need to bind a key to

    record demopan

and another to

    stop

in your game.

Enjoy and please post any issues you have here.
