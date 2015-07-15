
                                                               
                     |                                         
                   __|   _   _  _  _    __    _   __,   _  _   
                  /  |  |/  / |/ |/ |  /  \_|/ \_/  |  / |/ |  
                  \_/|_/|__/  |  |  |_/\__/ |__/ \_/|_/  |  |_/
                                           /|                  
                                           \|                  

                   A simple cross-platform Steam demo organiser


[![PyPI version](https://badge.fury.io/py/demopan.svg)](http://badge.fury.io/py/demopan)


Easy Install
------------

  1.  Install pip for your OS: https://pip.pypa.io/en/latest/installing.html
  2.  Open a terminal (Terminal.app in OSX).
  3.  Install Demopan and its dependencies from PyPI: `pip install --user demopan` or `sudo pip install demopan`.


Manual Install
--------------

  1. Download and install [watchdog](https://pypi.python.org/pypi/watchdog).
  2. Download the Demopan [package](https://github.com/vixus0/demopan/tarball/0.2)
  4. Install with `python setup.py install` or similar.


Usage
-----

Demopan watches directories for demo files and sorts them when it thinks they're done
being recorded. The best way to use it is by running it on startup and just forgetting
about it.

A demo may take around a minute to appear in the demos folder after you stop the 
recording in-game.

    demopan [-h] [--demos dir] [-w dir]

  * `--demos`: The place you want to save your demos.
  * `-w`: A directory to watch for demo files.

Demopan automatically watches the default directories on Linux, OSX and Windows but you can
specify more of your own with the `-w` flag. Use the flag multiple times for more folders.

When you have finished recording a demo, Demopan will save it in the demos folder as:

    YYYYmmdd-HHMM-map-player.dem


Key binding
-----------

For a quick way to start/stop recordings, put this in your game's `autoexec.cfg`:

    alias panon "say_team [DEMOPAN] Get am, Boyos!; record demopan; alias panpan panoff"
    alias panoff "say_team [DEMOPAN] End recording; stop; alias panpan panon"
    alias panpan panon
    bind F8 panpan

Enjoy! Please post any issues you have to [github](https://github.com/vixus0/demopan).
