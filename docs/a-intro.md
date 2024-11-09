

# Depricated Introduction

`pymddoc` is a python package for creating markdown documents with embedded code snippets.

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


