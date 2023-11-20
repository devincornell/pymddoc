
# %%
import pymddoc
import inspect


# %%
doc = pymddoc.Document(
    title = 'My Document',
    snippet_template=pymddoc.templates.default(
        stdout_header='###### output:'
    ),
)

# %%
doc.markdown('''
            
# Introduction

This is a paragraph.

''')

# %%
with doc.snippet(inspect.currentframe(), print_stdout=True) as snippet:
    print('hello world')
    print('another hello world')
    print('yet another hello world')

# %%
doc.markdown('''
So that went well.

This shows a list comprehension:
''')
# %%
with doc.snippet(inspect.currentframe()) as snippet:
    [print(i) for i in range(10)]

# %%
doc.markdown('''
This is how you make a true markdown function:
''')

# %%
with doc.snippet(inspect.currentframe()) as snippet:
    def mytestfunc(a, b):
        return a + b
    
return doc

# %%
if __name__ == '__main__':
    doc = mytestfunc()
    print(doc.render_markdown())
    #print(doc.render_html())


