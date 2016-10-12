# Raphidoc

It's not fast - It's not clean, It's not pretty - but it works :laughing:


## Further Ideas

* Add a CSV Table directive
* Use weasy-hyphens?
* Use PDF bookmarks?
* PDF TOC - based on `print_outline`

```python
# Output on http://www.w3.org/TR/CSS21/intro.html
#     1. Introduction to CSS 2.1 (page 2)
#       1. A brief CSS 2.1 tutorial for HTML (page 2)
#       2. A brief CSS 2.1 tutorial for XML (page 5)
#       3. The CSS 2.1 processing model (page 6)
#         1. The canvas (page 7)
#         2. CSS 2.1 addressing model (page 7)
#       4. CSS design principles (page 8)
def print_outline(bookmarks):
    for (label, (page, _, _), children) in bookmarks:
        print('%s%d. %s (page %d)' % (
            ' ' * indent, i, label.lstrip('0123456789. '), page+1))
        print_outline(children)
print_outline(document.make_bookmark_tree())
```
