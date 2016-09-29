from weasyprint import HTML
import markdown
import os

extensions = ['math', 'markdown.extensions.def_list',
              'markdown.extensions.codehilite', 'markdown.extensions.admonition',
              'pymdownx.github(no_nl2br=True)']
if not os.path.exists('output'):
    os.makedirs('output')

raw_markdown = None
with open('index.md') as f:
    raw_markdown = f.read()

raw_html = markdown.markdown(raw_markdown, extensions)
raw_template = None
with open('template/template.html') as f:
    raw_template = f.read()


raw_template = raw_template.replace('{{content}}', raw_html)
with open('output/index.html', 'w') as f:
    f.write(raw_template)

# Generate PDF
HTML(string=raw_template, base_url='./').write_pdf('output/index.pdf')

# TODO: anchors:  {#header1} (http://stackoverflow.com/questions/3292903/in-markdown-what-is-the-best-way-to-link-to-a-fragment-of-a-page-i-e-some-id)
# TOC? (*https://github.com/Kozea/WeasyPrint/issues/23)

# TODO: CSV Tables with <csv-table>CSV HERE</csv-table>
# http://pythonhosted.org/Markdown/extensions/api.html
# weasy-hyphens?
# bookmarks?
