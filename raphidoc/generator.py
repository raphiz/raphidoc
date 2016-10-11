import os
import glob
import logging
import shutil

import markdown
import html5lib
import weasyprint
from lxml import html
from jinja2 import Template, Environment, FileSystemLoader

from . import mdx_math
from .config import load_config

logger = logging.getLogger(__name__)


class Page():
    def __init__(self, working_directory, path, md):
        self.path = path
        self.working_directory = working_directory

        # TODO: what if no html extension? What if pure html doc?
        self.output_path = path.replace('.md', '.html')
        self.md = md

    def render(self):
        with open(os.path.join(self.working_directory, self.path)) as f:
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


class Generator:

    def __init__(self, working_directory):
        self.working_directory = os.path.abspath(working_directory)

    def generate(self):
        self.config = load_config(self.working_directory)
        # TODO: load 'output' & markdown exteions from config
        self.output_directory = os.path.join(self.working_directory, 'output', self.identifier)
        # TODO: Configure math via config (eg. additional packages, output directory etc.)
        self.md = markdown.Markdown(extensions=[mdx_math.MathExtension(self.output_directory),
                                                'markdown.extensions.def_list',
                                                'markdown.extensions.codehilite',
                                                'markdown.extensions.admonition',
                                                'pymdownx.github(no_nl2br=True)'])

        self._setup_output()
        self._copy_assets()

        pages = []
        for path in self.config['pages']:
            page = Page(self.working_directory, path, self.md)
            page.render()
            pages.append(page)

        self.process(pages)

        self.config = None
        self.output_directory = None
        self.md = None

    def _setup_output(self):
        if os.path.exists(self.output_directory):
            logger.debug("Cleaning up existing directory `{}`".format(self.output_directory))
            for f in glob.glob(self.output_directory + '/*'):
                if os.path.isdir(f):
                    shutil.rmtree(f)
                else:
                    os.unlink(f)
        else:
            logger.debug("Generating output directories `{}`".format(self.output_directory))
            os.makedirs(self.output_directory)

    def _copy_assets(self):
        # TODO: if assets directory contains folders html/ or pdf/ - only copy these directories!
        shutil.copytree(os.path.join(self.config['theme'], 'assets'),
                        os.path.join(self.output_directory, 'assets'))

        for asset in self.config['assets']:
            abspath = os.path.join(self.working_directory, asset)
            if not os.path.exists(abspath):
                logger.warning('Asset `{0}` was declared in config but does not exist!'
                               .format(asset))
                continue
            if os.path.isdir(abspath):
                shutil.copytree(abspath, os.path.join(self.output_directory, asset))
            else:
                destination_dir = os.path.join(self.output_directory, os.path.dirname(asset))
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)
                shutil.copy(abspath, os.path.join(self.output_directory, asset))


class HTMLGenerator(Generator):
    identifier = 'html'

    def process(self, pages):
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

        env = Environment(loader=FileSystemLoader(self.config['theme']))
        template = env.get_template('page.html')

        # Write the output
        for page in pages:
            raw = page.result
            if page.toc:
                raw = raw.replace('{{TOC}}', toc_html)

            templated = template.render(content=raw)

            destination_dir = os.path.join(self.output_directory,
                                           os.path.dirname(page.output_path))
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
            with open('{0}/{1}'.format(self.output_directory, page.output_path), 'w') as f:
                f.write(templated)


class PDFGenerator(Generator):
    identifier = 'pdf'

    def process(self, pages):
        env = Environment(loader=FileSystemLoader(self.config['theme']))
        template = env.get_template('pdf.html')

        complete = ''
        for page in pages:
            raw = page.result
            if page.toc:
                # TODO: Generate!
                pass
            complete += raw + '\n'

        tmp_html = os.path.join(self.output_directory, 'pdf.tmp.html')
        with open(tmp_html, 'w') as f:
            f.write(template.render(content=complete))

        document = weasyprint.HTML(tmp_html).render()

        # TODO: make output fle path configurable
        pdf_destination_path = os.path.join(self.output_directory, 'index.pdf')
        document.write_pdf(pdf_destination_path)
        logger.info('PDF written to file://{}'.format(pdf_destination_path))
