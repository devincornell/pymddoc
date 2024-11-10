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


## Installation
You can install the latest version of `PyMdDoc` using pip:

```bash
pip install git+ssh://git@github.com/devincornell/pymddoc.git@main
```


## Overview

The process of compiling your markdown document involves several steps.

1. Author the markdown document.
2. Read the markdown from a file or string.
3. Use a compile function from within `pymddoc`.
    a. First, render the markdown with Jinja.
    b. Then, compile the markdown with Pandoc.
4. Save the compiled document to a file or a string (in the case of html).

First, create a markdown document with the document content and links to images.

```markdown
    ---
    title: Example Markdown
    author: John Doe
    date: 2021-01-01
    bibliography: ["data/references.bib"]
    ---

    ## Supported by Jinja

    {# this is a Jinja comment #}

    The `OUTPUT_FORMAT` variable allows you to write output format-specific content.

    {% if OUTPUT_FORMAT == 'html' %}
    This is an HTML document.
    {% else %}
    This is not an HTML document.
    {% endif %}


    ## Custom `PyMdDoc` Functions

    ### Insert Tables from CSV or Excel Files

    These built-in functions will accomplish this.

    {{csv_to_markdown('data/testtable.csv')}}

    {{excel_to_markdown('data/testtable.xlsx')}}


    ### Insert SVG or PDF Images

    {{svg_to_png('data/testimage.svg')}}

    {{pdf_to_png('data/testimage.pdf')}}


    ## Pandoc Compilation

    Any pandoc features are allowed.

    ### Citations

    Use citations like this [@Angelou1969] or this [-@Cohen1963]. The bib file is provided in the compile function.

    ### Code Snippets

    You can also use code snippets:

        ```python
        def example_function():
            return "Hello, world!"
        ```

    ### Custom HTML

    ::: { #favorite .note font-size="1.5em" }
    You can also create Div blocks with ids, classes, and other attributes.
    :::

```

That's all folks!

