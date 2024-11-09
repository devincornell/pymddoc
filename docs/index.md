# `PyMdDoc` Python Package

This package integrates the features of [Pandoc](https://pandoc.org/) document conversion with the [Jinja](https://jinja.palletsprojects.com/en/stable/) templating engine to create a powerful interface for creating documents using Markdown. Aside from the features of these powerful tools, the package also includes custom functions to accellerate your writing workflow.

+ Custom `PyMdDoc` functions usable with Jinja
    + Insert tables directly from CSV or Excel files.
    + Convert SVG or PDF files to PNG for compilation.

+ [Jinja](https://jinja.palletsprojects.com/en/stable/) templating engine
    + Add comments
    + Provide and call custom functions
    + Use conditionals, loops and other control structures

+ [Pandoc](https://pandoc.org/) document converter
    + Extract and modify YAML header metadata
    + Code snippet supports
    + Citations from bibtex files using Citeproc
    + Specify id, class, and other html elements


#### Installation
You can install the latest version of `PyMdDoc` using pip:

```bash
pip install git+ssh://git@github.com/devincornell/pymddoc.git@main
```
