---
title: "Introduction to `PyMdDoc`"
---

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


# Planned Features

+ [ ] bibtex/citations
+ [ ] read pdf files for pdf/docx conversion
+ [ ] support for svg images

+ [ ] metadata editing
+ [ ] excellent support code snippets
+ [x] read and convert tables to markdown
+ [x] comments (supported through jinja)



---
title: "hello world"
bibliography: ["data/references.bib"]
---

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



# Depricated

# Introduction

`pymddoc`\* is a python package for creating markdown documents with embedded code snippets.

\*: name is a work in progress

Steps for creating a document:

1. create a .py script that will contain code to generate the document
2. create a `DocMaker` object by calling `Document` with desired templates and metadata
3. add markdown using the `.markdown()` method
4. add code snippets using the context manager returned by the `.snippet()` method
5. render the document to markdown or html

### Open a New Document

The first step in creating a document is to call the `Document` function, which returns a `DocMaker` object. This object will be used to create the document. This function takes a number of parameters for metadata, templates, and other configurations. See the API documentation for more details.



```python
    import pymddoc
    doc = pymddoc.Document(
        title = 'My Document',
        date = 'Nov 20, 2023',
    )
```




### Markdown

We can insert markdown using the `.markdown()` method. Simply pass a string to the method and it will be inserted into the document directly. 

Note that this is standard markdown, so you may use any features supported by your markdown compiler (pandoc if you use the built-in html renderer).

Here I will define a new function and print the result.


```python
    doc.markdown('''
    # example header

    + item 1
    + item 2

    | col 1 | col 2 |
    |-------|-------|
    | a     | b     |
    | c     | d     |
    ''')
```




### Code Snippets

Create code snippets using the `.snippet()` method. When executed, it returns a context manager that captures the source code and stdout as a markdown code block (denoted by "```").

Create the code snippet like the following:


```python
    with doc.snippet(inspect.currentframe(), print_stdout=True):
        def mytestfunc(a, b):
            return a + b
        print(mytestfunc(1, 2))
```

###### output:

```
    >> 3
```



### Rendering the Document

The document object now contains all the information needed to construct the markdown, including metadata, source code, and stdout of the code snippets. Use the `render_markdown()` method to render the document to markdown.


```python
    print(doc.render_markdown())
```

###### output:

```
    >> ---
    >> title: My Document
    >> date: 2023-11-20 00:00:00
    >> ---
    >> 
    >> 
    >> # example header
    >> 
    >> + item 1
    >> + item 2
    >> 
    >> | col 1 | col 2 |
    >> |-------|-------|
    >> | a     | b     |
    >> | c     | d     |
    >> 
    >> 
    >> ```python
    >>     def mytestfunc(a, b):
    >>         return a + b
    >>     print(mytestfunc(1, 2))
    >> ```
    >> 
    >> 
    >> 
    >> ```
    >>     >> 3
    >> ```
```



You can see that the source code and stdout are included in the markdown. The stdout is indented and the source code is stripped of its baseline indentation.

Use the `render_html()` method to render the document to html using pandoc.


```python
    print(doc.render_html())
```

###### output:

```
    >> <h1 id="example-header">example header</h1>
    >> <ul>
    >> <li>item 1</li>
    >> <li>item 2</li>
    >> </ul>
    >> <table>
    >> <thead>
    >> <tr class="header">
    >> <th>col 1</th>
    >> <th>col 2</th>
    >> </tr>
    >> </thead>
    >> <tbody>
    >> <tr class="odd">
    >> <td>a</td>
    >> <td>b</td>
    >> </tr>
    >> <tr class="even">
    >> <td>c</td>
    >> <td>d</td>
    >> </tr>
    >> </tbody>
    >> </table>
    >> <div class="sourceCode" id="cb1"><pre
    >> class="sourceCode python"><code class="sourceCode python"><span id="cb1-1"><a href="#cb1-1" aria-hidden="true" tabindex="-1"></a>    <span class="kw">def</span> mytestfunc(a, b):</span>
    >> <span id="cb1-2"><a href="#cb1-2" aria-hidden="true" tabindex="-1"></a>        <span class="cf">return</span> a <span class="op">+</span> b</span>
    >> <span id="cb1-3"><a href="#cb1-3" aria-hidden="true" tabindex="-1"></a>    <span class="bu">print</span>(mytestfunc(<span class="dv">1</span>, <span class="dv">2</span>))</span></code></pre></div>
    >> <pre><code>    &gt;&gt; 3</code></pre>
```



You can see that the output is now html which can be inserted into a larger template. Simply add html tags manually if you wish to create a web page (although it will likely render without).                  


