# `PyMdDoc` Python Package

This package offers a powerful interface for compiling markdown documents to a number of other formats using a combination of [Pandoc](https://pandoc.org/) document conversion and the [Jinja](https://jinja.palletsprojects.com/en/stable/) templating engine with custom functions that can be used to insert tables from CSV or Excel files, insert SVG or PDF images directly, and offer conditional logic for compiling to different document formats.

The combination of these three elements offer the following features:

+ Custom `PyMdDoc` functions usable from Jinja
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
