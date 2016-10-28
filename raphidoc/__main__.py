import click
import logging
import os
import shutil

from .generator import HTMLGenerator, PDFGenerator
from . import utils
from . import __VERSION__

logger = logging.getLogger('raphidoc')


@click.group()
@click.version_option(version=__VERSION__)
@click.option('-v', '--verbose', is_flag=True, default=False, help='Verbose output')
@click.option('-d', '--directory', type=click.Path(file_okay=False,
              dir_okay=True, writable=True, exists=True), default='./',
              help='The project working directory (must contain raphidoc.yml)')
@click.pass_context
def cli(ctx, verbose, directory):
    setup_logging(verbose)
    logger.debug("Working directory is `{}`".format(directory))
    ctx.obj['working_directory'] = directory


@click.command()
@click.pass_context
def init(ctx):
    target = ctx.obj['working_directory']
    if len(os.listdir(target)) != 0:
        logger.error("The target directory {0} is not empty!".format(target))
        return
    with open(os.path.join(target, 'raphidoc.yml'), 'w') as f:
        f.write("""version: 1.0
title: %s
author: John Doe

pages:
   - index.md

assets:
    - images/

theme: raphi_theme""" % os.path.basename(target))
    with open(os.path.join(target, 'index.md'), 'w') as f:
        f.write("# Hello World! \n\n {{TOC}} \n\n This is Raphidoc!\n")
    with open(os.path.join(target, '.gitignore'), 'w') as f:
        f.write("output/\n")
    os.mkdir(os.path.join(target, 'images'))


@click.command()
@click.option('-w', '--watch', is_flag=True, default=False, help='Watch and re-generate on change')
@click.option('-e', '--exclude', multiple=True, help='Files and directory to ignore when changed')
@click.option('-b', '--bind', default='0.0.0.0', help='Specify alternate bind address')
@click.option('-p', '--port', default=8000, help='Specify alternate port')
@click.pass_context
def html(ctx, watch, exclude, bind, port):
    logger.info('Generating html')

    html_generator = HTMLGenerator(ctx.obj['working_directory'])
    html_generator.generate()

    if watch:
        # TODO: what if output directory changes?
        utils.watch(exclude, html_generator.generate, ctx.obj['working_directory'], True,
                    os.path.join('output', html_generator.identifier),
                    bind, port)


@click.command()
@click.option('-w', '--watch', is_flag=True, default=False, help='Watch and re-generate on change')
@click.option('-e', '--exclude', multiple=True, help='Files and directory to ignore when changed')
@click.pass_context
def pdf(ctx, watch, exclude):
    logger.info('Generating PDF')
    pdf_generator = PDFGenerator(ctx.obj['working_directory'])
    pdf_generator.generate()

    if watch:
        # TODO: what if output directory changes?
        utils.watch(exclude, pdf_generator.generate, ctx.obj['working_directory'], False)


@click.command()
@click.pass_context
def clean(ctx):
    logger.info('Cleaning up...')
    shutil.rmtree(os.path.join(ctx.obj['working_directory'], 'output'))


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
        cli.add_command(clean)
        cli(obj={}, standalone_mode=False)
    except Exception as e:
        logger.error(e)
        logger.debug(e, exc_info=True)
        exit(1)

if __name__ == '__main__':
    main()
