# Introduction to `PyMdDoc`

See the [project website](http://devinjcornell.com/pymddoc) for more information.

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


## Planned Features

+ [ ] Edit metdata dynamically
+ [ ] Excecute and insert code snippets with stdout
+ [x] read and convert tables to markdown
+ [x] read pdf files for pdf/docx conversion
+ [x] Embed pdf/svg images
+ [x] Create comments (already supported through jinja)
+ [x] Control over bibtex/citations with citeproc

## Installation
You can install the latest version of `PyMdDoc` using pip:

```bash
pip install git+ssh://git@github.com/devincornell/pymddoc.git@main
```


## Python API Overview

The process of compiling your markdown document involves several steps.

1. Author the markdown document.
2. Read the markdown from a file or string.
3. Use a compile function from within `pymddoc`.

    a. First, render the markdown with Jinja.

    b. Then, compile the markdown with Pandoc.
    


### 1. Create the Markdown Document

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

### 2. Read the Markdown Document

Next read the file into the `MarkdownDoc` object. You load it as a file or a string.

```python
doc = pymddoc.MarkdownDoc.from_str('file.md')
```

This is the string version:

```python
doc = pymddoc.MarkdownDoc.from_str('this is a markdown string!')
```

You can extract metadata as a dict using the following function:

```python
doc.extract_metadata()
```

### 3. Compile the Markdown Document

Next, render the file to the desired format. This will render the Jinja templates and functions.

The HTML can be output as a string or a file. Use this function to render the markdown to a string:

```python
html = doc.render_to_string('html')
```

As a shortcut, you can use the `render_html` function.

```python
html = doc.render_html()
```

When compiling pdf or docx files, you can use the `render_to_file` function. It will automatically infer output format from the file extension.

```python
doc.render_to_file('output.pdf')
```

Same goes for compiling to docx.

```python
doc.render_to_file('output.docx')
```

Same goes for compiling to docx.

```python
doc.render_to_file('output.docx')
```

You can also call type-specific functions for rendering to specific formats.

```python
doc.render_to_docx('output.docx')
doc.render_to_pdf('output.pdf')
```

You can use the `vars` arugment to pass variables to the Jinja template, and pass a `PandocArgs` object to the render functions to have more control over the Pandoc conversion.

```python
doc.render_to_pdf(
    output_path=f'output.pdf',
    vars={'text_here': 'Hello, world!'},
    pandoc_args = pymddoc.PandocArgs(
        toc = True,
        embed_resources=True,
        extra_args=['--mathjax'],
    )
)
```

See the Python API Documentation for more information!
