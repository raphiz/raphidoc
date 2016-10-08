# TOC:


# Heading 1 :wink:

## Heading 1.1
### Heading 1.2.1

## Heading 1.2

# Heading 2
## Heading 2.1
### Heading 2.1.1

# Heading 3

[HERE](http://www.google.com)

Apple
:   Pomaceous fruit of plants of the genus Malus in
    the family Rosaceae.

Orange :wink:
:   The fruit of an evergreen tree of the genus Citrus.

```c++
std::out << x << y
```

What is `hello`? $$e^e$$

$$\frac{-b \pm \sqrt{b^2 -4ac} }{2a}$$


```python
import markdown
from markdown.extensions import toc
from pymdownx import github


def load_markdown():
    ext_toc = toc.TocExtension(marker=None)
ext_github = github.GithubExtension(no_nl2br=True)
```

Orange?

!!! danger "Don't try this at home"
    AHRG

!!! note
    note this

!!! todo
    - [X] item 1
    * [X] item A
    * [ ] item B
        more text
        + [x] item a
        + [ ] item b
        + [x] item c
    * [X] item C
    - [ ] item 2
    - [ ] item 3
