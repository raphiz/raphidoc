import os

import yaml
from weasyprint import HTML
import markdown
from . import mdx_math

# TODO: add commands build, clean, serve and auto-build
# TODO: output/html and output/pdf ?


# TODO: fix formulas...

def main():
    # TODO: check if file exist..
    cfg = None
    with open('raphidocs.yml') as f:
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
    with open('%s/page.html' % cfg['theme']) as f:
        page_template = f.read()

    complete = ''
    for name, path in cfg['pages'].items():
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
    with open('output/tmp.pdf.html', 'w') as f:
        f.write(complete)
    # TODO: delete this file afterwards!

    # TODO: run this in the "safely" in the output dir...
    HTML(string=complete, base_url='./').write_pdf('index.pdf')




    print("okay!")
