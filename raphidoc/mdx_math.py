import os
import logging
import subprocess
import re
import json
import hashlib

from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import markdown

from .exceptions import RaphidocException
from . import utils

"""
Math extension for Python-Markdown using Node & MathJax.
"""

logger = logging.getLogger(__name__)

# Global - very ugly, but used to improve performace
FAILED_INSTALLATION = False


def svg_rewrite(svg):
    svg = re.sub('(xmlns(\:[a-z]*)?="[^"]+")', '', svg)
    svg = re.sub('xlink:href', 'href', svg)

    tree = etree.fromstring(svg)
    for use in tree.iter('use'):
        ref_id = use.get('href')[1:]
        ref = tree.find('.//path[@id=\'%s\']' % ref_id)
        use.attrib.pop('href')
        use.tag = ref.tag
        transform = use.attrib.pop('transform', '')

        x = use.attrib.pop('x', 0)
        y = use.attrib.pop('y', 0)
        transform += 'translate(%s, %s)' % (x, y)

        if len(use.attrib) > 0:
            raise RaphidocException('Unexpected attribute(s) on "use" element found: %s'
                                    % [k for k in ref.attrib.keys()])
        for key, value in ref.attrib.items():
            # TODO: BUG HERE?!
            if key == 'translate':
                translate += value
            elif key != 'id':
                use.attrib[key] = value
        use.attrib['transform'] = transform
    tree.remove(tree.find('defs'))
    return etree.tostring(tree).decode()


def run_in_node(program, cache_directory):
    """
    Runs the given program in node and returns *only* it's stdout.
    Any errors will be ignored (except exceptions)
    """
    p1 = subprocess.Popen('node',
                          cwd=cache_directory,
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)

    stdout, stderr = p1.communicate(program.encode())
    if p1.returncode != 0:
        raise RaphidocException("Failed to convert math formula via node.\n{0}".format(
                                stderr.decode()))
    return stdout.decode()


def install_dependencies(cache_directory):
    global FAILED_INSTALLATION
    logger.info('checking node installation')
    if not utils.is_in_path('node', 'npm'):
        logger.warning('Could not find npm and/or node in PATH')
        FAILED_INSTALLATION = True
        return
    if not os.path.exists(cache_directory):
        os.makedirs(cache_directory)
    logger.info('installing mathjax-node')
    proc = subprocess.Popen(['npm', 'install', 'mathjax-node'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            cwd=cache_directory)
    ret = proc.wait(50)

    FAILED_INSTALLATION = ret != 0
    if FAILED_INSTALLATION:
        logger.warning('Failed to install node module `mathjax-node`')
    else:
        logger.info('Mathjax-node installed')


def compile_latex(formula, inline, cache_directory, no_cache=False, after_error=False):
    """
    Compiles the given Tex formula and returns it as a SVG.
    If the formula is invalid, an SVG is returned as well - but it contains an error message.
    (See MathJax for details)
    """
    if FAILED_INSTALLATION:
        return '<span class="missing-formula">{0}</span>'.format(formula)

    digest = hashlib.md5(str(str(inline) + formula).encode('utf-8')).hexdigest()
    if not no_cache:
        cached = os.path.join(cache_directory, '{}.svg'.format(digest))
        if os.path.exists(cached):
            logger.debug('Loading formula {} from cache'.format(formula))
            with open(cached, 'r') as f:
                return f.read()
    try:
        logger.debug('Rendering formula {}'.format(formula))
        program = """var mjAPI = require("mathjax-node/lib/mj-single.js");
        mjAPI.typeset({
          math: %s,
          format: "%s", // "TeX", "inline-TeX", "MathML"
          svg:true
        }, function (data) {
            console.log(data.svg);
        });
        """ % (json.dumps(formula), "inline-TeX" if inline else "TeX")
        svg = run_in_node(program, cache_directory)
        svg = svg_rewrite(svg)
        if not no_cache:
            with open(cached, 'w') as f:
                f.write(svg)
        return svg
    except Exception as e:
        if after_error:
            raise e
        install_dependencies(cache_directory)
        return compile_latex(formula, inline, cache_directory, no_cache, after_error=True)


class MathInlinePattern(markdown.inlinepatterns.Pattern):

    def handleMatch(self, m):
        code = m.group(2).strip()
        node = etree.fromstring(compile_latex(code, True, self.cache_directory))
        return node


class MathBlockProcessor(BlockProcessor):

    RE = re.compile(r'(\\\[)(?P<formula>\n(.*\n?)*)(\\\])')

    def test(self, parent, block):
        return bool(self.RE.fullmatch(block))

    def run(self, parent, blocks):
        raw_block = blocks.pop(0)
        code = self.RE.search(raw_block).group('formula')
        node = etree.fromstring(compile_latex(code, False, self.cache_directory))
        parent.append(node)
        return node


class MathExtension(markdown.Extension):

    def __init__(self, output_directory):
        markdown.Extension.__init__(self)
        self.cache_directory = os.path.join(output_directory, '.cache')

    def extendMarkdown(self, md, md_globals):
        inline = MathInlinePattern(r'\$\$(((?!\$\$).)*)\$\$')
        inline.cache_directory = self.cache_directory
        md.inlinePatterns.add('inlinemath', inline, '<escape')
        block = MathBlockProcessor(md.parser)
        block.cache_directory = self.cache_directory
        md.parser.blockprocessors.add('blockmath', block, '_begin')


def makeExtension(**kwargs):
    return MathExtension(**kwargs)
