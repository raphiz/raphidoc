import time
import logging

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from http.server import HTTPServer, SimpleHTTPRequestHandler

logger = logging.getLogger(__name__)


class EventHandler(PatternMatchingEventHandler):
    def on_any_event(self, event):
        # Manually filter output directory - pattern does not
        # work somehow...
        if (event.src_path.startswith('./output')):
            return

        logger.debug(event)
        logger.info('Regenerating...')
        self.callback()


def watch(excludes, callback, serve=False):
    handler = EventHandler()
    handler._ignore_patterns = excludes
    handler.callback = callback

    observer = Observer()
    observer.schedule(handler, './', recursive=True)
    observer.start()

    if serve:
        logger.error("NOT IMPLEMENTED!")
    else:
        logger.info("Watching - press Ctrl + C to abort")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
