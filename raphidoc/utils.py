import time
import os
import logging

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from http.server import HTTPServer, SimpleHTTPRequestHandler

logger = logging.getLogger(__name__)


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
