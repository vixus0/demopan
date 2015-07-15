#!/usr/bin/env python

from __future__ import print_function

import sys, os, time, signal, struct, string

from argparse import ArgumentParser
from datetime import datetime, timedelta
from threading import Thread

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# Python 2
try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty

def clean_str(str):
    return ''.join(filter(lambda x: x in string.printable, str))

def process_dem(dem):
    HEADER_FMT = '8sii260s260s260s260sfiii'

    siz = struct.calcsize(HEADER_FMT)
    with open(dem, 'rb') as f:
        b = f.read(siz)
    d = struct.unpack(HEADER_FMT, b)
    client = d[4].split(b'\0',1)[0].decode('utf8').replace(' ', '_')
    map = d[5].split(b'\0',1)[0].decode('utf8').replace(' ', '_')
    duration = d[7]
    return clean_str(client), clean_str(map), duration

def save_dem(dem, out_dir):
    client, map, duration = process_dem(dem)
    d = datetime.utcnow() - timedelta(seconds=duration)
    name = '{}-{}-{}.dem'.format(d.strftime('%Y%m%d-%H%M'), map, client)
    out = os.path.join(out_dir, name)
    os.rename(dem, out)
    print('Demo saved to: '+out)

class DemoHandler(PatternMatchingEventHandler):
    def __init__(self, out_dir, timeout):
        super(DemoHandler, self).__init__(['*.dem'])
        self.watchers = {}
        self.outd = out_dir
        self.timeout = timeout

    def watch_dem(self, dem):
        self.watchers[dem] = DemoWatcher(dem, self.outd, self.timeout)

    def on_created(self, ev):
        dem = ev.src_path
        self.watch_dem(dem)

    def on_modified(self, ev):
        dem = ev.src_path

        print('Demo modified: '+dem)

        if dem in self.watchers:
            self.watchers[dem].dem_modified()
        else:
            self.watch_dem(dem)

class DemoWatcher(object):
    def __init__(self, dem, out_dir, timeout):
        self.dem = dem
        self.outd = out_dir
        self.queue = Queue()
        self.timeout = timeout

        print('Tracking demo: '+dem)
        self.thread = Thread(name='Watch: '+dem, target=self.watch)
        self.thread.start()

    def dem_modified(self):
        self.queue.put(datetime.utcnow())

    def watch(self):
        running = True

        while running:
            try:
                ping = self.queue.get(block=True, timeout=self.timeout)
                self.queue.task_done()
            except Empty:
                running = False

        save_dem(self.dem, self.outd)

def main():
    HOME = os.path.expanduser('~')
    STEAM_DIRS = [
            os.path.join(HOME, '.local/share/Steam/SteamApps/common'),
            os.path.join(HOME, 'Library/Application Support/Steam/SteamApps/common'),
            'C:/Program Files/Steam/SteamApps/common'
            ]
    DEFAULT_WATCH = [os.path.join(d, 'Team Fortress 2', 'tf') for d in STEAM_DIRS]
    ASSUME_DONE = 60.0 # seconds after last modify when we assume demo is done

    # -- Args
    ap = ArgumentParser(description='Demopan Source game demo processor.')
    ap.add_argument('-w', help='Directory to watch for recorded demos.', action='append', dest='watch', default=DEFAULT_WATCH)
    ap.add_argument('--demos', help='Directory to save renamed demos.', default=os.path.join(HOME, 'demos'))
    ap.add_argument('--timeout', help='Seconds after recording has stopped to save demo.', type=float, default=ASSUME_DONE)

    args = ap.parse_args()

    if not os.path.exists(args.demos):
        print('Demo save directory not found: '+args.demos+'\n')
        ap.print_help()
        sys.exit(1)


    # -- Watcher
    handler = DemoHandler(args.demos, args.timeout)
    observer = Observer()

    dircount = 0
    
    for dir in args.watch:
        if os.path.exists(dir):
            print('Watching '+dir+' for demos.')
            observer.schedule(handler, dir)
            dircount += 1

    if dircount == 0:
        print('No valid directories to watch!')
        sys.exit(1)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print('Exiting Demopan.')

    observer.join()

    def term_handler():
        observer.stop()
        print('Exiting Demopan.')

    signal.signal(signal.SIGTERM, term_handler)


if __name__ == "__main__":
    main()
