import os
import base64
import logging
import subprocess
import re
import json

from markdown.inlinepatterns import Pattern
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
from markdown.extensions import Extension
import markdown

from .exceptions import RaphidocException

"""
Math extension for Python-Markdown using Node & MathJax.
"""

logger = logging.getLogger(__name__)

# Global - very ugly, but used to improve performace
INSTALLED = None


def node_installed():
    """
    Checks wheather there the programms "node" and "npm" are in the path.
    If so, returns True - otherwise False.
    """
    node = False
    npm = False
    for path in os.environ["PATH"].split(os.pathsep):
        path = path.strip('"')
        if os.path.exists(os.path.join(path, 'npm')):
            npm = True
        if os.path.exists(os.path.join(path, 'node')):
            node = True
        if node and npm:
            return True
    return False


def run_in_node(program):
    """
    Runs the given program in node and returns *only* it's stdout.
    Any errors will be ignored (except exceptions)
    """
    p1 = subprocess.Popen('node',
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)

    stdout, stderr = p1.communicate(program.encode())
    return stdout.decode()


def install_dependencies():
    # TODO: Run in CWD
    # TODO: shortcut: if CWD contains a folder node_modules/mathjax-node, log info and skip
    global INSTALLED
    if not node_installed():
        INSTALLED = False
        return INSTALLED

    # ret = subprocess.call(['npm', 'install', 'mathjax-node'], timeout=50)
    # INSTALLED = ret == 0
    # return INSTALLED
    INSTALLED = True
    return INSTALLED


def compile_latex(formula, inline=False):
    """
    Compiles the given Tex formula and returns it as a SVG.
    If the formula is invalid, an SVG is returned as well - but it contains an error message.
    (See MathJax for details)
    """
    if INSTALLED is None:
        install_dependencies()

    if not INSTALLED:
        logger.warning("MathJax or Node is not installed!")
        return formula

    program = """var mjAPI = require("mathjax-node/lib/mj-single.js");
    mjAPI.typeset({
      math: %s,
      format: "%s", // "TeX", "inline-TeX", "MathML"
      svg:true
    }, function (data) {
        console.log(data.svg);
    });
    """ % (json.dumps(formula), "inline-TeX" if inline else "TeX")
    return run_in_node(program)


def base64_image_url(svg):
    return 'data:image/svg+xml;charset=utf-8;base64,' + base64.b64encode(svg.encode()).decode()


class MathInlinePattern(markdown.inlinepatterns.Pattern):

    def handleMatch(self, m):
        # TODO: Allow to fully inline SVG - via config?
        node = etree.Element('img')
        code = m.group(2).strip()
        node.set('src', base64_image_url(compile_latex(code, True)))
        node.set('alt', code)
        node.set('class', 'inline-math')
        return node


class MathBlockProcessor(BlockProcessor):

    RE = re.compile(r'(\\\[)(?P<formula>\n(.*\n?)*)(\\\])')

    def test(self, parent, block):
        return bool(self.RE.fullmatch(block))

    def run(self, parent, blocks):
        raw_block = blocks.pop(0)
        code = self.RE.search(raw_block).group('formula')
        node = etree.Element("img")
        node.set('src', base64_image_url(compile_latex(code, False)))
        node.set('alt', code)
        node.set('class', 'block-math')
        parent.append(node)


class MathExtension(markdown.Extension):

    def __init__(self, output_directory):
        markdown.Extension.__init__(self)
        self.output_directory = output_directory

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('inlinemath',
                              MathInlinePattern(r'\$\$(((?!\$\$).)*)\$\$'),
                              '<escape')
        md.parser.blockprocessors.add('blockmath',
                                      MathBlockProcessor(md.parser), '_begin')


def makeExtension(**kwargs):
    return MathExtension(**kwargs)
