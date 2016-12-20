import time
import os
import subprocess
import logging

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from http.server import HTTPServer, SimpleHTTPRequestHandler

logger = logging.getLogger(__name__)


def is_in_path(*args):
    """
    Checks wheather there the programms "node" and "npm" are in the path.
    If so, returns True - otherwise False.
    """
    binaries = {binary: False for binary in args}
    for path in os.environ["PATH"].split(os.pathsep):
        path = path.strip('"')
        for binary in args:
            if os.path.exists(os.path.join(path, binary)):
                binaries[binary] = True
    return all(binaries.values())

def princepdf(source, destination):
    # TODO: debug if in debug!
    p1 = subprocess.Popen(['prince', source, destination],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    stdout, stderr = p1.communicate()
    # TODO: proper error handling & log output properly!
    print(stdout.decode())
    print(stderr.decode())


class EventHandler(PatternMatchingEventHandler):
    def on_any_event(self, event):
        # Manually filter output directory - pattern does not
        # work somehow...
        if (event.src_path.startswith(os.path.join(self.working_directory, 'output'))):
            return

        logger.debug(event)
        logger.info('Regenerating...')
        self.callback()


class HttpRequestNoLoggingHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def watch(excludes, callback, working_directory, serve=False, output_directory='./',
          host='', port=8000):
    handler = EventHandler()
    # TODO: join excludes with working directory?
    handler._ignore_patterns = excludes
    handler.callback = callback
    handler.working_directory = working_directory

    observer = Observer()
    observer.schedule(handler, working_directory, recursive=True)
    observer.start()

    if serve:
        os.chdir(os.path.join(working_directory, output_directory))
        logger.info("Serving at http://%s:%s" % (host, port))
        httpd = HTTPServer((host, port), HttpRequestNoLoggingHandler)
        httpd.serve_forever()
    else:
        logger.info("Watching - press Ctrl + C to abort")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
