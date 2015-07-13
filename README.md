
                                                 
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

Demopan will automatically run TF2 (or your game of choice) for you.

When you have finished recording a demo, Demopan will save it in the demos folder as:

    YYYYmmdd-HHMM-map-player.dem


Key binding
-----------

Put this in your game's `autoexec.cfg`:

    alias panon "say_team '[DEMOPAN] Get 'am, Boyos!'; record demopan; alias panpan panoff"
    alias panoff "say_team '[DEMOPAN] End recording'; stop; alias panpan panon"
    alias panpan panon
    bind F8 panpan


Enjoy and please post any issues you have to [github](https://github.com/vixus0/demopan).
