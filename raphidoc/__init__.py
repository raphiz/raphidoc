

import os

import yaml
from weasyprint import HTML
import markdown
import shutil
from . import mdx_math

# TODO: add commands build, clean, serve and auto-build
# TODO: output/html and output/pdf ?


# TODO: fix formulas...


def main():
    # TODO: check if file exist..
    cfg = None
    with open('raphidoc.yml') as f:
        cfg = yaml.load(f.read())

    #TOOD: setup required directories...
    if not os.path.exists('output'):
        os.makedirs('output')

    extensions = [mdx_math.MathExtension(), 'markdown.extensions.def_list',
                  'markdown.extensions.codehilite', 'markdown.extensions.admonition',
                  'pymdownx.github(no_nl2br=True)']


    # TODO: Validate config - especially check if theme dir exists

    # TODO: make loading of themes fail safe!
    # TODO: how to transfer assets from themes? (eg compy assets directory)
    page_template = None
    with open('{}/page.html'.format(cfg['theme'])) as f:
        page_template = f.read()

    # TODO: merge if exists?
    shutil.rmtree('output/assets/')
    shutil.copytree('{}/assets/'.format(cfg['theme']), '{}/assets'.format('output/'))

    complete = ''
    for item in cfg['pages']:
        name, path = item.popitem()
        if not os.path.exists(path):
            print('todo: propper warning!')

        raw_markdown = None
        with open(path) as f:
            raw_markdown = f.read()

        raw_html = markdown.markdown(raw_markdown, extensions)

        complete += raw_html

        # TODO: more advanced templating?
        # jinja is probably an overkill - however it's required for a pretty menu
        # TODO: move into a function
        templated = page_template.replace('{{content}}', raw_html)

        # TODO: better solution for file extension!
        # eg. if extension is not .md - try to remove the file extension - if not possible, just append .html?
        with open('output/%s.html' % path[:-3], 'w') as f:
            f.write(templated)

        # TODO: add (configurabel) spacer between pages
        complete += '\n<hr>\n'

    pdf_template = None
    with open('%s/pdf.html' % cfg['theme']) as f:
        pdf_template = f.read()
    # todo: call templating function
    complete = pdf_template.replace('{{content}}', complete)
    with open('output/tmp.pdf.html', 'w') as f:
        f.write(complete)
    # TODO: delete this file afterwards!

    # TODO: run this in the "safely" in the output dir...
    document = HTML(string=complete, base_url='./output/').render()

    # Print the outline of the document.
    # Output on http://www.w3.org/TR/CSS21/intro.html
    #     1. Introduction to CSS 2.1 (page 2)
    #       1. A brief CSS 2.1 tutorial for HTML (page 2)
    #       2. A brief CSS 2.1 tutorial for XML (page 5)
    #       3. The CSS 2.1 processing model (page 6)
    #         1. The canvas (page 7)
    #         2. CSS 2.1 addressing model (page 7)
    #       4. CSS design principles (page 8)
    def print_outline(bookmarks, indent=0):
        for i, (label, (page, _, _), children) in enumerate(bookmarks, 1):
            print('%s%d. %s (page %d)' % (
                ' ' * indent, i, label.lstrip('0123456789. '), page+1))
            print_outline(children, indent + 2)
    print_outline(document.make_bookmark_tree())

    document.write_pdf('output/index.pdf')




    print("okay!")
