import click
import logging
import os
from . import generator

import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from http.server import HTTPServer, SimpleHTTPRequestHandler

logger = logging.getLogger('raphidoc')


@click.group()
@click.option('-v', '--verbose', is_flag=True, default=False, help='Verbose output')
@click.option('-d', '--directory', type=click.Path(file_okay=False,
              dir_okay=True, writable=True, exists=True), default='./',
              help='The project working directory (must contain raphidoc.yml)')
def cli(verbose, directory):
    setup_logging(verbose)
    logger.debug("Working directory is `{}`".format(directory))
    os.chdir(directory)


@click.command()
def init():
    logger.info('Not yet implemented - will create raphidoc.yml')


@click.command()
def clean():
    logger.info('Not yet implemented - will create raphidoc.yml')


@click.command()
def html():
    logger.info('Generating html')
    generator.generate_html()


@click.command()
@click.option('-e', '--exclude', multiple=True, help='Files and directory to ignore when changed')
def serve(exclude):

    observer = Observer()

    class EventHandler(PatternMatchingEventHandler):
        def on_any_event(self, event):
            # Manually filter output directory - pattern does not
            # work somehow...
            if (event.src_path.startswith('./output')):
                return
            logger.debug(event)
            logger.info('Regenerating html...')
            generator.generate_html()

    handler = EventHandler()
    handler._ignore_patterns = exclude
    observer.schedule(handler, './', recursive=True)
    observer.start()
    logger.info('Serving at :')
    # TODO: generate for the first time
    # TODO: serve
    # TODO: make generic - so that it works for PDF as well!
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


@click.command()
def pdf():
    logger.info('Generating PDF')
    generator.generate_pdf()


def setup_logging(verbose):
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    if verbose:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)-7s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.debug("Setting up logging complete")


def main():
    try:
        cli.add_command(init)
        cli.add_command(html)
        cli.add_command(serve)
        cli.add_command(pdf)
        cli(standalone_mode=False)
    except Exception as e:
        logger.error(e)
        logger.debug(e, exc_info=True)
        exit(1)

if __name__ == '__main__':
    main()
