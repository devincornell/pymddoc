


# Citations and Bibliography

Part of the motivation for using `Pandoc` for this package was that it supports citations and bibliographies through citeproc. Given a markdown document with citations in it and a `.bib` file, `Pandoc` can generate a formatted document with citations and a bibliography.

This package maintains some easy-to-use functions for working with citations and bibliographies in markdown documents.




---

``` python linenums="1"
# for demonstration
import tempfile
from IPython.core.display import display, HTML

import sys
sys.path.append('..')
import pymddoc
```



stderr:
 

    /tmp/ipykernel_1016843/3729719973.py:3: DeprecationWarning: Importing display from IPython.core.display is deprecated since IPython 7.14, please import from IPython display
      from IPython.core.display import display, HTML
    

 



---




### Citation Auto-complete

Check out the [pandoc citer](https://marketplace.visualstudio.com/items?itemName=notZaki.pandocciter) VSCode plugin for citation auto-complete as you edit your documents.

In the document YAML header, you will need to provide the bibliography attribute.




---

``` python linenums="1"
markdown_text = '''
---
title: "Hello World"
bibliography: ["data/references.bib"]
---
Use citations like this [@Angelou1969] or this [-@Cohen1963]. These will auto-complete if you use the VSCode plugin.
'''.strip()
```


---




## Compiling Documents with Citations
Most importantly for our purposes, we should be able to compile a document that includes citations automatically from a database. We can do this by specifying the `citeproc_bibliography` argument in `PandocArgs`. This argument should be a path to a `.bib` file.

In this example I write the bibtex data to a temporary file which is then used to compile the document.




---

``` python linenums="1"
bib_file_text = '''
@book{Angelou1969,
    place={New York},
    edition={1},
    title={I Know Why the Caged Bird Sings},
    ISBN={9780375507892},
    publisher={Random House},
    author={Angelou, Maya},
    year={1969},
    month={Jan.}
}
@article{Cohen1963,
    author = "P. J. Cohen",
    title = "The independence of the continuum hypothesis",
    journal = "Proceedings of the National Academy of Sciences",
    year = 1963,
    volume = "50",
    number = "6",
    pages = "1143--1148",
}
'''

md_file_text = '''
Use citations like this [@Angelou1969] or this [-@Cohen1963].
'''.strip()

with tempfile.TemporaryDirectory() as tmpdir:
    bib_fname = tmpdir + '/refs.bib'
    with open(bib_fname, 'w') as f:
        f.write(bib_file_text)
    

    doc = pymddoc.MarkdownDoc.from_str(md_file_text)
    html = doc.render_html(
        pandoc_args=pymddoc.PandocArgs(
            citeproc_bibliography=bib_fname,
        )
    )
display(HTML(html))
```




text:

    <IPython.core.display.HTML object>
 



html:

    <p>Use citations like this <span class="citation"
    data-cites="Angelou1969">(Angelou 1969)</span> or this <span
    class="citation" data-cites="Cohen1963">(1963)</span>.</p>
    <div id="refs" class="references csl-bib-body hanging-indent"
    role="doc-bibliography">
    <div id="ref-Angelou1969" class="csl-entry" role="doc-biblioentry">
    Angelou, Maya. 1969. <em>I Know Why the Caged Bird Sings</em>. 1st ed.
    Random House.
    </div>
    <div id="ref-Cohen1963" class="csl-entry" role="doc-biblioentry">
    Cohen, P. J. 1963. <span>“The Independence of the Continuum
    Hypothesis.”</span> <em>Proceedings of the National Academy of
    Sciences</em> 50 (6): 1143–48.
    </div>
    </div>
    
 


 



---




You can change the bibtex file if you have any issues with the citation information.

 