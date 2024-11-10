
import pymddoc
import inspect

def main() -> pymddoc.DocMaker:
    import pymddoc

    document = pymddoc.Document(
        title = 'Introduction',
        snippet_template=pymddoc.templates.default(
            stdout_header='###### output:'
        ),
    )


    document.markdown('''
                
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

    ''')

    with document.snippet(inspect.currentframe()):
        import pymddoc
        doc = pymddoc.Document(
            title = 'My Document',
            date = 'Nov 20, 2023',
        )

    document.markdown('''
    ### Markdown

    We can insert markdown using the `.markdown()` method. Simply pass a string to the method and it will be inserted into the document directly. 

    Note that this is standard markdown, so you may use any features supported by your markdown compiler (pandoc if you use the built-in html renderer).

    Here I will define a new function and print the result.
    ''')

    with document.snippet(inspect.currentframe()):
        doc.markdown('''
        # example header
        
        + item 1
        + item 2
        
        | col 1 | col 2 |
        |-------|-------|
        | a     | b     |
        | c     | d     |
        ''')
        
    document.markdown('''
    ### Code Snippets

    Create code snippets using the `.snippet()` method. When executed, it returns a context manager that captures the source code and stdout as a markdown code block (denoted by "```").

    Create the code snippet like the following:
    ''')
        
    with document.snippet(inspect.currentframe()):
        with doc.snippet(inspect.currentframe(), print_stdout=True):
            def mytestfunc(a, b):
                return a + b
            print(mytestfunc(1, 2))


    document.markdown('''
    ### Rendering the Document

    The document object now contains all the information needed to construct the markdown, including metadata, source code, and stdout of the code snippets. Use the `render_markdown()` method to render the document to markdown.
    ''')

    with document.snippet(inspect.currentframe()):
        print(doc.render_markdown())

    document.markdown('''
    You can see that the source code and stdout are included in the markdown. The stdout is indented and the source code is stripped of its baseline indentation.

    Use the `render_html()` method to render the document to html using pandoc.
    ''')

    with document.snippet(inspect.currentframe()):
        print(doc.render_html())

    document.markdown('''
    You can see that the output is now html which can be inserted into a larger template. Simply add html tags manually if you wish to create a web page (although it will likely render without).                  
    ''')
    
    return document

if __name__ == '__main__':
    document = main()
    md = document.render_markdown()
    print(md)
    with open('README.md', 'w') as f:
        f.write(md)

