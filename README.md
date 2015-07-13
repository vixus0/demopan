
                                                 
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


Key binding
-----------

Put this in your game's `autoexec.cfg`:

    alias panon 'echo DEMOPAN RECORDING; record demopan; alias panpan panoff'
    alias panoff 'echo DEMOPAN STOP; stop; alias panpan panon'
    alias panpan panon
    bind KEY panpan


Enjoy and please post any issues you have here.
