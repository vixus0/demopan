#!/usr/bin/env python

import subprocess as sub
import sys, os, time, signal, struct, shutil, string

from tempfile import mkstemp
from argparse import ArgumentParser
from datetime import datetime

DEFAULT_TF = '{}/.steam/Steam/SteamApps/common/Team Fortress 2/tf'.format(os.getenv('HOME'))
HEADER_FMT = '8sii260s260s260s260sfiii'

def clean_str(str):
    return ''.join(filter(lambda x: x in string.printable, str))

def process_dem(dem):
    siz = struct.calcsize(HEADER_FMT)
    with open(dem, 'rb') as f:
        b = f.read(siz)
    d = struct.unpack(HEADER_FMT, b)
    client = d[4].split(b'\0',1)[0].decode('utf8').replace(' ', '_')
    map = d[5].split(b'\0',1)[0].decode('utf8').replace(' ', '_')
    return clean_str(client), clean_str(map)

def hl2_running(proc='hl2_linux'):
    try:
        tf2_pid = sub.check_output(['pidof', proc])
    except sub.CalledProcessError:
        return False
    return True


if __name__ == "__main__":
    # -- Args
    ap = ArgumentParser(description='Demopan TF2 demo processor.')
    ap.add_argument('--tf', help='TF2 /tf/ directory.', default=DEFAULT_TF)
    ap.add_argument('--demos', help='Demo directory.', default=os.path.join(DEFAULT_TF, 'demos'))
    ap.add_argument('--gameid', help='Steam game ID.', default=440)

    args = ap.parse_args()

    if not os.path.exists(args.tf):
        print('Wrong tf directory.')
        ap.print_help()
        sys.exit(1)

    if not os.path.exists(args.demos):
        print('Demo directory not found.')
        ap.print_help()
        sys.exit(1)


    # -- Touch demo file
    DEM = os.path.join(args.tf, 'demopan.dem')
    sub.call(['touch', DEM])


    # -- File watcher
    watch_fd, watch_path = mkstemp(prefix='demopan')
    pwatch_args = [
        'inotifywait',
        '-q', '-c', '-m', 
        '-e', 'open', '-e', 'close_write',
        '-o', watch_path,
        DEM]
    pwatch = sub.Popen(pwatch_args, stdout=sub.PIPE)

    
    # -- Run game if not running already
    psteam_args = ['steam', 'steam://rungameid/'+str(args.gameid)]
    if not hl2_running():
        psteam = sub.call(psteam_args)

    tf2_running = True
    watchf = os.fdopen(watch_fd, 'r')

    while tf2_running and pwatch.returncode is None:
        where = watchf.tell()
        line = watchf.readline()

        if not line:
            time.sleep(1)
            watchf.seek(where)

        if 'OPEN' in line:
            print('Demo file opened for writing.')
        elif 'CLOSE' in line:
            print('Demo file closed.')

            # Rename demo file
            client, map = process_dem(DEM)

            mtime = os.path.getmtime(DEM)
            d = datetime.utcnow()

            name = d.strftime('%Y%m%d-%H%M-')
            name += '-'.join([map, client])
            name += '.dem'

            NEW_DEM = os.path.join(args.demos, name)

            shutil.copyfile(DEM, NEW_DEM)
            print('Demo saved to: '+NEW_DEM)

        pwatch.poll()
        tf2_running = hl2_running()

    # -- End inotify process
    if not tf2_running:
        os.kill(pwatch.pid, signal.SIGTERM)
    watchf.close()
    os.remove(watch_path)
