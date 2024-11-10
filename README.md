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


# Planned Features

+ [ ] metadata editing
+ [ ] excellent support code snippets
+ [x] read and convert tables to markdown
+ [x] read pdf files for pdf/docx conversion
+ [x] support for svg images
+ [x] comments (supported through jinja)
+ [x] bibtex/citations


## Jinja and Pandoc

This package integrates `Pandoc` document conversion with the Jinja templating engine to create a powerful and interface for compiling markdown documents to a number of other formats.

The general idea is that you can draw up new ideas while not caring what happens.


### Jinja Templating Syntax

{# this is a comment with jinja! It will not be shown to pandoc. #}




## Citations

Pro tip: see the [pandoc citer](https://marketplace.visualstudio.com/items?itemName=notZaki.pandocciter) VSCode plugin for citation auto-complete.

You can insert citations like this  [@Welch2006; @Pedersen2008]. Cite direct references to authors using the following syntax: Pedersen et al. [-@Pedersen2008] noted that eigenvectors are the best way to determine the principal components.


::: {.warning}
This is the last warning!
:::

```python
def main():
    print(f'Why the heck would you go there?')
```

{# embed the pdf as a png #}

![]({{svg_to_png("https://storage.googleapis.com/public_data_09324832787/static_factory_methods.svg")}}){ #hello .myclass size="80%" }


{# embed the pdf as a png #}

![]({{pdf_to_png("data/hist_rt_comparison.pdf")}}){ .myclass size="80%" }

{# embed the pdf directly #}
![](data/hist_rt_comparison.pdf){ .myclass size="80%" }


::: {.classname}
{{ csv_to_markdown('data/testtable.csv') }}
:::

{# this is a comment! #}













## Inserting Tables

You can insert tables into the markdown document using the builtin jinja function `csv_to_markdown`. This function will read the referenced CSV file and convert it to markdown format using pandas so it can be inserted directly in the document before compilation.

```markdown
{{ csv_to_markdown('data/testtable.csv') }}
```

## SVG Images

The pandoc PDF compiler does not have native support for SVG images, but you can use the builtin jinja function `svg_to_png` to convert local or remote svg images to png for compilation. The function will download the image (if it is remote) and convert it to a png file in a temporary directory. The function returns the path to that temporary file, which can be referenced directly in the markdown document..

```markdown
![Alt text.]({{svg_to_png("https://storage.googleapis.com/public_data_09324832787/static_factory_methods.svg")}}){ #hello .myclass size="80%" }
```

## PDF Images


