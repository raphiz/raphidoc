from markdown.inlinepatterns import Pattern
from markdown.util import etree
from markdown.extensions import Extension
import markdown
from hashlib import md5
import os
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
$"""

AFTER_TEX = """$
\\end{document}
"""

# TODO: make configurable
DIRECTORY = 'output/assets'
DIRECTORY = 'output/assets'

class MathPattern(markdown.inlinepatterns.Pattern):
    def __init__(self):
        markdown.inlinepatterns.Pattern.__init__(self, r'\$\$(.*)\$\$')

    def handleMatch(self, m):
        # print(m.group(2))
        node = markdown.util.etree.Element('img')
        code = m.group(2).strip()
        node.set('src', self.generateImage(code))
        node.set('alt', code)
        node.set('class', 'inline-math')
        return node

    def generateImage(self, code):
        digest = md5(code.encode('utf-8')).hexdigest()
        file_name = '{}/{}'.format(DIRECTORY, digest)
        # TODO: cleaner solutoon
        png = "assets/{}.png".format(digest)
        tex = file_name + ".tex"

        # if the image already exists
        if os.path.exists(png):
            return png

        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)

        with open(tex, "w") as f:
            f.writelines([BEFORE_TEX, code, AFTER_TEX])
            f.close()

        compile_latex = ('latex -interaction=batchmode -output-directory={d}'
                         ' {t} > /dev/null'.format(d=DIRECTORY, t=tex))
        if os.system(compile_latex) != 0:
            raise Exception('Failed to compile latex')
        latex2png = 'dvipng -D 250 -o {f}.png -T tight {f}.dvi > /dev/null'.format(f=file_name)
        if os.system(latex2png) != 0:
            raise Exception('Failed to converte to png :(')

        # clean up
        os.remove(tex)
        os.remove('{f}.log'.format(f=file_name))
        os.remove('{f}.dvi'.format(f=file_name))
        os.remove('{f}.aux'.format(f=file_name))
        return png


class MathExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('math', MathPattern(), '<escape')


def makeExtension(**kwargs):
    return MathExtension(**kwargs)
