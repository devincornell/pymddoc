
import pymddoc

document = pymddoc.Document(
    metadata = pymddoc.Metadata.new(
        title = 'My Test Document',
        subtitle = 'A test document for pymddoc',
        id = 'my-test-document',
        author = 'Devin J. Cornell',
        date = '2021-09-10',
    ),
    snippet_template = pymddoc.templates.default(),
)

document.markdown(
indent = ' ',
id = 'my-first-section',
text = '''
# Today's lesson on extravagance: Inherant Boldness

Why do we do the things we do? I have no idea, but I can tell you how great they are. No matter how great they are, they always fall for the best.

| 1 | 2 | 3 |
|---|---|---|
| 4 | 5 | 6 |
| 7 | 8 | 9 |

''')

document.markdown('############### no args to constructor #################')

mylife = None

@document.snippet
def myfunc():
    global mylife
    # good example
    mylife = 42
    return mylife

document.markdown('############### (id on markdown and) custom template + id on snippet #################', id='holla')

    
@document.snippet(
    template = '###### code:\n\n```python\n{{source}}\n```\n\n###### output:\n\n```\n{{stdout}}\n{{output}}\n```',
    id = 'my-second-section',
)
def myfunc2():
    global mylife
    # good example
    mylife = mylife * 2

document.markdown('############### itnoring stdout template, not filtering declaration #################')

@document.snippet(
    template=pymddoc.templates.ignore_stdout(),
    filter_global_declaration=True,
)
def myfunc3():
    global mylife
    # good example
    class MyClass:
        def __init__(self, x=mylife):
            self.x = x
        def __repr__(self):
            return f'MyClass({self.x})'
    return MyClass()

if __name__ == '__main__':

    print(document.render_markdown())

