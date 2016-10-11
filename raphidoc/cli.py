import click
import logging
import os

from . import generator
from . import utils
from . import __VERSION__

logger = logging.getLogger('raphidoc')


@click.group()
@click.version_option(version=__VERSION__)
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
@click.option('-w', '--watch', is_flag=True, default=False, help='Watch and re-generate on change')
@click.option('-e', '--exclude', multiple=True, help='Files and directory to ignore when changed')
def html(watch, exclude):
    logger.info('Generating html')
    generator.generate_html()
    if watch:
        utils.watch(exclude, generator.generate_html, True)


@click.command()
@click.option('-w', '--watch', is_flag=True, default=False, help='Watch and re-generate on change')
@click.option('-e', '--exclude', multiple=True, help='Files and directory to ignore when changed')
def pdf(watch, exclude):
    logger.info('Generating PDF')
    generator.generate_pdf()
    if watch:
        utils.watch(exclude, generator.generate_pdf, False)


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
        cli.add_command(pdf)
        cli(standalone_mode=False)
    except Exception as e:
        logger.error(e)
        logger.debug(e, exc_info=True)
        exit(1)

if __name__ == '__main__':
    main()
