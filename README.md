# Raphidoc

Raphidoc is a documentation generator with first class PDF support.

Where other tools such as mkdocs or sphinx have great support for HTML, it's allways
painful to generate PDFs.

Raphidocs tries to unite the best of both worlds into one tool.

## Current Features

* Generate HTML & PDF documents with ...
    * emojis :tada:
    * table of contents (in PDF with links & Page numbers)
    * Math Formulas (as PNG - in the future with SVG)
    * Github Flavoured Markdown
    * admonition for RST-Like directives
    * more :rainbow:
* Style & organize PDFs and HTML with pure CSS & HTML!
* Watch for changes & regenereate

## Example usage

See the `example/` directory for a sample Project.

```bash
$ cd example/
$ raphidoc pdf -w # Generate PDF and watch for changes
$ raphidoc html -w # Generate HTML, watch for changes and serve it
```

## Further Ideas

Up Next:

* Better rewrite single page: especially RELATIVE LINKS AND IMAGES ("multipage mode")
    ➪ Rewrite: image paths, css/js imports/includes paths, links & anchors - others?
    ➪ [Postprocessor](http://pythonhosted.org/Markdown/extensions/api.html#postprocessors)?!  
    * Choose singlepage / multipage mode in HTML-Generator -> PDF can then simply convert it
* Recover from errors when watching (eg. file not found)
* Watch for .md files in working dir and report if not included!
* make release

Long term:

* Find a better name
* Better error reporting for tex formulas! (Which formula? Latex output).
* Inline SVG formulas with MathJax. This actually works (see `mathjax-svg-math`) - but SVG is currently not supported by weasyprint :disappointed:
* Auto-Refresh HTML (when with -w) - solve similar to previewr
* Table of images/tables/notes/formulas usw -> performance?(https://github.com/tvogels/serif)
* Add a CSV Table directive
* Use weasy-hyphens?
* Math formulas on sub-pages?!
* Auto detect relative images
* Generate index for eg. tipps etc.
* Graphiviz
* Tests, tests, tests...
