import os
import hashlib

from markdown.inlinepatterns import Pattern
from markdown.util import etree
from markdown.extensions import Extension
import markdown

from .exceptions import RaphidocException
"""
Math extension for Python-Markdown

Based on http://freewisdom.org/projects/python-markdown/mdx_math

Works only on *nix systems. Latex must be installed

TODO: Add support for multi line <math></math> tags

"""
BEFORE_TEX = """\\documentclass[12pt]{article}
\\usepackage[latin1]{inputenc}
\\usepackage{amsmath}
\\usepackage{amsfonts}
\\usepackage{amssymb}
\\pagestyle{empty}
\\begin{document}
\["""

AFTER_TEX = """\]
\\end{document}
"""


class MathPattern(markdown.inlinepatterns.Pattern):
    def __init__(self, output_directory, destination):
        markdown.inlinepatterns.Pattern.__init__(self, r'\$\$(.*)\$\$')
        self.output_directory = output_directory
        self.destination = destination

    def handleMatch(self, m):
        node = markdown.util.etree.Element('img')
        code = m.group(2).strip()
        node.set('src', self.generateImage(code))
        node.set('alt', code)
        node.set('class', 'inline-math')
        return node

    def generateImage(self, code):
        digest = hashlib.md5(code.encode('utf-8')).hexdigest()
        directory = os.path.join(self.output_directory, self.destination)

        png = os.path.join(directory, digest + '.png')
        png_link = os.path.join(self.destination, digest + '.png')
        tex = os.path.join(directory, digest + '.tex')

        # if the image already exists
        if os.path.exists(png):
            return png_link

        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(tex, "w") as f:
            f.writelines([BEFORE_TEX, code, AFTER_TEX])
            f.close()

        compile_latex = ('latex -interaction=batchmode -output-directory={d}'
                         ' {t} > /dev/null'.format(d=directory, t=tex))
        if os.system(compile_latex) != 0:
            raise RaphidocException('Failed to compile latex')
        latex2png = 'dvipng -D 250 -o {d}/{f}.png -T tight {d}/{f}.dvi > /dev/null'.format(
                     d=directory, f=digest)
        if os.system(latex2png) != 0:
            raise RaphidocException('Failed to converte to png :(')

        # clean up
        os.remove(tex)
        os.remove(os.path.join(directory, digest + '.log'))
        os.remove(os.path.join(directory, digest + '.dvi'))
        os.remove(os.path.join(directory, digest + '.aux'))
        return png_link


class MathExtension(markdown.Extension):

    def __init__(self, output_directory, destination='assets'):
        markdown.Extension.__init__(self)
        self.output_directory = output_directory
        self.destination = destination

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('math', MathPattern(self.output_directory, self.destination),
                              '<escape')


def makeExtension(**kwargs):
    return MathExtension(**kwargs)
