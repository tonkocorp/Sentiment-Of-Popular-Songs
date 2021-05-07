
import os
import sys
from os.path import getmtime
import test

# Parse script arguments and configuration files.
# ...

WATCHED_FILES = ['songs.db']
WATCHED_FILES_MTIMES = [(f, getmtime(f)) for f in WATCHED_FILES]

while True:
    # Wait for inputs and act on them.
    # ...

    # Check whether a watched file has changed.
    for f, mtime in WATCHED_FILES_MTIMES:
        if getmtime(f) != mtime:
            # One of the files has changed, so restart the script.
            print('--> restarting')
            # When running the script via `./daemon.py` (e.g. Linux/Mac OS), use
            os.execv('app.py', sys.argv)
            # When running the script via `python daemon.py` (e.g. Windows), use
            # os.execv(sys.executable, ['python'] + sys.argv)
