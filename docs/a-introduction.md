# Introduction

`pymddoc`\* is a python package for creating markdown documents with embedded code snippets. The idea is that you create a new document object and sequentially add components of the document as desired. This introduction will walk through the basic steps for creating a document.

Steps for creating a document:

1. create a .py script that will contain code to generate the document
2. create a `DocMaker` object by calling `Document` with desired templates and metadata
3. add markdown using the `.markdown()` method
4. add code snippets using the context manager returned by the `.snippet()` method
5. render the document to markdown or html


```
import sys
sys.path.append('..')
import pymddoc
import inspect
```

### Open a New Document

The first step in creating a document is to call the `Document` function, which returns a `DocMaker` object. This object will be used to create the document. This function takes a number of parameters for metadata, templates, and other configurations. See the API documentation for more details.


```
doc = pymddoc.Document(
    title = 'My Document',
    date = 'Nov 20, 2023',
    snippet_template=pymddoc.templates.default(
        stdout_header='###### output:'
    ),
)
```

See the documentation for the `Document` function for more information about optional metadata that can be passed, but you can see that here we have only used the title and date parameters. Note that this information will be exported to the output markdown text as YAML metadata.


```
doc.metadata
```




    Metadata(title='My Document', subtitle=None, author=None, date=datetime.datetime(2023, 11, 20, 0, 0), other_metadata={})



### Markdown

We can insert markdown using the `.markdown()` method. Simply pass a string to the method and it will be inserted into the document directly. 

Note that this is standard markdown, so you may use any features supported by your markdown compiler (pandoc if you use the built-in html renderer).

Here I will define a new function and print the result.


```
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


```
with doc.snippet(inspect.currentframe(), print_stdout=True):
    def mytestfunc(a, b):
        return a + b
    print(mytestfunc(1, 2))
```

    3



```

```

### Rendering the Document

The document object now contains all the information needed to construct the markdown, including metadata, source code, and stdout of the code snippets. Use the `render_markdown()` method to render the document to markdown.




```
print(doc.render_markdown())
```

    ---
    title: My Document
    date: 2023-11-20 00:00:00
    ---
    
    ```python
        COULD NOT FIND SOURCE
    ```
    
    
    
    ```
        >> 3
    ```
    
    
    



```

```
