# API Introduction

This page describes the API of the `PyMdDoc` package.

The `MarkdownDoc` class maintains the main interface for creating documents. It manages a single markdown document which can be rendered and converted to another document type. It can be created from a string using `from_str()` or a file using `from_file()`.


```python
import sys
sys.path.append('..')
import pymddoc
```

I will use this functions to make html outputs more readable.


```python
def print_formatted_html(html_string):
    '''Print HTML that is formatted with indentation.'''
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_string, 'html.parser')
    clean_html = soup.prettify()
    print(clean_html)
```

### Ingest Markdown Documents

The following example demonstrates how to create a simple markdown document.


```python
example_markdown = '''
---
title: Example Markdown
author: John Doe
date: 2021-01-01
---

{# this is a jinja comment #}

# Header 1

You can use italics and bold text as supported by pandoc.

::: { #favorite .note font-size="1.5em" }
You can also create Div blocks with ids, attributes, and other attributes.
:::

You can also use code snippets:

```python
    def example_function():
        return "Hello, world!"
```.
<br/>
'''.strip()

doc = pymddoc.MarkdownDoc.from_str(example_markdown)
print(doc)
```

    MarkdownDoc({'author': 'John Doe', 'date': '2021-01-01', 'title': 'Example Markdown'})


You can extract the YAML header metadata from the document using the `extract_metadata()` method. This method returns a dictionary of the metadata from the document.


```python
doc.extract_metadata()
```




    {'author': 'John Doe', 'date': '2021-01-01', 'title': 'Example Markdown'}



### Rendering Documents

There are several different methods for rendering markdown documents to other document types.

You can use the method `render_to_string()` to convert the document to any text-based format.


```python
html = doc.render_to_string('html')
print_formatted_html(html)
```

    <h1 id="header-1">
     Header 1
    </h1>
    <p>
     You can use italics and bold text as supported by pandoc.
    </p>
    <div class="note" data-font-size="1.5em" id="favorite">
     <p>
      You can also create Div blocks with ids, attributes, and other
    attributes.
     </p>
    </div>
    <p>
     You can also use code snippets:
    </p>
    <p>
     <code>
      python     def example_function():         return "Hello, world!"
     </code>
     .
     <br/>
    </p>
    


To convert to pdf or docx formats, you will want to write to a file. In this case, you can use the `render_to_file()` method. It can automatically infer the file type using the file extension.


```python
import tempfile
with tempfile.TemporaryDirectory() as tempdir:

    doc.render_to_file(f'{tempdir}/test.pdf')
```

There are also some type-specific methods for rendering html, pdf, or docx files.


```python
with tempfile.TemporaryDirectory() as tempdir:
    
    doc.render_to_pdf(f'{tempdir}/test.pdf')
    doc.render_to_docx(f'{tempdir}/test.docx')
    html = doc.render_html()
print_formatted_html(html)
```

    <h1 id="header-1">
     Header 1
    </h1>
    <p>
     You can use italics and bold text as supported by pandoc.
    </p>
    <div class="note" data-font-size="1.5em" id="favorite">
     <p>
      You can also create Div blocks with ids, attributes, and other
    attributes.
     </p>
    </div>
    <p>
     You can also use code snippets:
    </p>
    <p>
     <code>
      python     def example_function():         return "Hello, world!"
     </code>
     .
     <br/>
    </p>
    


### Jinja Templating Features
You can pass variables to be inserted in the markdown document using Jinja templating with the `vars` argument to most render functions.


```python
d = pymddoc.MarkdownDoc.from_str('{{ text_here }}')
html = d.render_html(vars={'text_here': 'Hello, world!'})
print_formatted_html(html)
```

    <p>
     Hello, world!
    </p>
    


While Pandoc supports a number of output formats, it is necessarily inconsistent in how it renders various elements of the document. Using the `OUTPUT_FORMAT` constant available through `PyMdDoc`, you can conditionally render elements based on the output format. 


```python
example_markdown = '''
{% if OUTPUT_FORMAT == 'html' %}
This is an HTML document.
{% else %}
This is not an HTML document.
{% endif %}
'''.strip()

doc = pymddoc.MarkdownDoc.from_str(example_markdown)
print(doc.render_html())
```

    <p>This is an HTML document.</p>
    


### Pandoc Arguments
You can use the `pandoc_args` argument to pass additional arguments to the pandoc command from any render function. This can be useful for specifying the output format or other options.

Pass arguments using the `PandocArgs` dataclass. The docstring of that class contains a list of all the available arguments.


```python
print(pymddoc.PandocArgs.__doc__)
```

    Dataclass that contains arguments for pandoc conversion.
            See this page for more about pandoc markdown:
                https://quarto.org/docs/authoring/markdown-basics.html
        Args:
            standalone: adds the --standalone flag to the pandoc command.
            embed_resources: adds the --embed-resources flag to the pandoc command.
            toc: adds the --toc flag to the pandoc command.
            citeproc_bibliography: adds the --citeproc and --bibliography {fname}
                arguments to the pandoc command.
            template: adds the --template={fname} argument to the pandoc command.
            extra_args: additional arguments to add to the pandoc command.
            **pandoc_kwargs: passed to pandoc.
        


And you can pass it as an argument to any render function.


```python
with tempfile.TemporaryDirectory() as tempdir:

    doc.render_to_pdf(
        output_path=f'{tempdir}/test.pdf',
        pandoc_args = pymddoc.PandocArgs(
            toc = True,
            embed_resources=True,
            extra_args=['--mathjax'],
        )
    )
```

See other pages for examples of using custom functions within the markdown document.
