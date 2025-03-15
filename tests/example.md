---
title: Example Markdown
author: John Doe
date: 2021-01-01
bibliography: ["test_data/references.bib"]
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

{{csv_to_markdown('test_data/testtable.csv')}}

{{excel_to_markdown('test_data/testtable.xlsx')}}


### Insert SVG or PDF Images

{{svg_to_png('test_data/drawing.svg')}}

{{pdf_to_png('test_data/drawing.pdf')}}


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