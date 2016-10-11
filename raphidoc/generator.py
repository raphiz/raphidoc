import logging
import os
import shutil
import yaml
import markdown
import html5lib
import weasyprint
from lxml import html
from jinja2 import Template, Environment, FileSystemLoader

from .exceptions import RaphidocException
from . import mdx_math

logger = logging.getLogger(__name__)

CONFIG_FILE_NAME = 'raphidoc.yml'
OUTPUT_DIRECTORY = 'output'


class Page():
    def __init__(self, path, md):
        self.path = path
        # TODO: what if no html extension? What if pure html doc?
        self.output_path = path.replace('.md', '.html')
        self.md = md

    def render(self):
        with open(self.path) as f:
            raw = f.read()
            self.result = self.md.convert(raw)
            self.toc = '{{TOC}}' in self.result
            return self.result

    def generate_toc(self):
        toc = []
        tree = html5lib.parse(self.result, treebuilder='lxml',
                              namespaceHTMLElements=False).getroot()
        for heading in tree.cssselect('h1, h2, h3, h4, h5, h6, h8'):
            url = '{0}#{1}'.format(self.output_path, heading.get('id'))
            title = html.tostring(heading, method='text').decode('utf-8').strip()
            toc.append((heading.tag, url, title))
        return toc


def _generate(output_format, callback):
    output_directory = os.path.join(OUTPUT_DIRECTORY, output_format)
    config = _load_config()

    _setup_output(output_directory)
    _copy_assets(config, output_directory)

    md = _load_markdown(config)
    pages = _generate_pages(config, md)

    callback(config, output_directory, pages, md)


def generate_html():
    """
        Generates the paeg - in the current working directory!
    """
    _generate('html', _gernerate_html)


def _gernerate_html(config, output_directory, pages, md):
    toc = []
    for page in pages:
        toc += page.generate_toc()

    # TODO: properly and hierarchically format the toc
    # TODO: extract (and make configurable in theme?)
    toc_html = Template("""
    <ul>
        {% for x,y,z in pages %}
        <li class="toc-{{x}}"><a href="{{y}}">{{z}}</a></li>
        {% endfor %}
    </ul>
    """).render(pages=toc)

    env = Environment(loader=FileSystemLoader(config['theme']))
    template = env.get_template('page.html')

    # Write the output
    for page in pages:
        raw = page.result
        if page.toc:
            raw = raw.replace('{{TOC}}', toc_html)

        templated = template.render(content=raw)
        if not os.path.exists(os.path.join(output_directory, os.path.dirname(page.output_path))):
            os.makedirs(os.path.join(output_directory, os.path.dirname(page.output_path)))

        with open('{0}/{1}'.format(output_directory, page.output_path), 'w') as f:
            f.write(templated)


def generate_pdf():
    """
        Generates the paeg - in the current working directory!
    """
    _generate('pdf', _gernerate_pdf)


def _gernerate_pdf(config, output_directory, pages, md):
    env = Environment(loader=FileSystemLoader(config['theme']))
    template = env.get_template('pdf.html')

    complete = ''
    for page in pages:
        raw = page.result
        if page.toc:
            # TODO: Generate!
            pass
        complete += raw + '\n'

    tmp_html = '{0}/pdf.tmp.html'.format(output_directory)
    with open(tmp_html, 'w') as f:
        f.write(template.render(content=complete))

    document = weasyprint.HTML(tmp_html).render()
    # TODO: make configurable
    document.write_pdf(os.path.join(output_directory, 'index.pdf'))


def _generate_pages(config, md):
    pages = []
    for path in config['pages']:
        page = Page(path, md)
        page.render()
        pages.append(page)
    return pages


def _load_markdown(config):
    # TOOD: load more from config
    md = markdown.Markdown(extensions=[mdx_math.MathExtension(), 'markdown.extensions.def_list',
                                       'markdown.extensions.codehilite',
                                       'markdown.extensions.admonition',
                                       'pymdownx.github(no_nl2br=True)'])
    return md


def _copy_assets(config, output_directory):
    # TODO: if assets directory contains folders html/ or pdf/ - only copy these directories!
    shutil.copytree('{}/assets/'.format(config['theme']), '{}/assets'.format(output_directory))
    for asset in config['assets']:
        if not os.path.exists(asset):
            logger.warning('Asset `{0}` was declared in config but does not exist!'.format(asset))
            continue
        if os.path.isdir(asset):
            shutil.copytree(asset, '{}/{}'.format(output_directory, asset))
        else:
            if not os.path.exists(os.path.join(output_directory, os.path.dirname(asset))):
                os.makedirs(os.path.join(output_directory, os.path.dirname(asset)))
            shutil.copy(asset, '{}/{}'.format(output_directory, asset))


def _setup_output(output_directory):
    if os.path.exists(output_directory):
        logger.debug("Cleaning up existing directory `{}`".format(output_directory))
        import glob
        for f in glob.glob(output_directory + '/*'):
            if os.path.isdir(f):
                shutil.rmtree(f)
            else:
                os.unlink(f)
    else:
        logger.debug("Generating output directories `{}`".format(output_directory))
        os.makedirs(output_directory)


def _load_config():
    logger.debug("Loading configuration")
    if not os.path.exists(CONFIG_FILE_NAME):
        raise RaphidocException('Configuration file {} does not exist'.format(CONFIG_FILE_NAME))

    with open(CONFIG_FILE_NAME) as f:
        config = yaml.load(f.read())
        logger.debug("Configuration loaded")
        return config

        # TODO: validate!
        # TODO: scan for *.md, *.markdown pages that are not in raphidoc.yml
        # TODO: resolve theme path
