


# Jupyter notebooks to Markdown

Another feature of this package is the ability to convert Jupyter notebooks to markdown files. There are both command-line and Python API interfaces for this functionality.



## Command-line interface
To convert a single Jupyter notebook to a markdown file, use the `ipynb2md` command.

``` bash
python -m pymddoc ipynb2md --help
```

output:
``` plaintext

Usage: python -m pymddoc ipynb2md [OPTIONS] IPYNB_FILE MD_FILE

  Convert a Jupyter notebook (json file) to a markdown file. Description:
  reads a jupyter notebook as a regular json file, passes the json to the
  template,     and renders the template with the json information.

Options:
  --template PATH
  --help           Show this message and exit.

```

### Multiple notebooks

To convert multiple Jupyter notebooks to markdown files, use the `ipynb2md-multi` command.

``` bash
python -m pymddoc ipynb2md-multi --help
```

output:
``` plaintext
Usage: python -m pymddoc ipynb2md-multi [OPTIONS] [IPYNB_FILES]...

  Convert multiple Jupyter notebooks (json files) to markdown files.

Options:
  --template PATH
  --help           Show this message and exit.
```

## Python API

You may also access this functionality within Python.




---

``` python linenums="1"
import os
import sys
sys.path.append('../src/')
import pymddoc
```


---




## The `convert_ipynb2md` function
You can convert a single Jupyter notebook to a markdown file by running the `convert_ipynb2md` function. This function takes advantage of the fact that jupyter notbebooks are stored as json files, and is essentially passes the json to the template, and renders the template with the json information.




---

``` python linenums="1"
use_template = pymddoc.ipynb2md_default_template

import json
with open('../tests/example.ipynb', 'r') as f:
    ipynb_json = json.load(f)

markdown = pymddoc.convert_ipynb2md(use_template, ipynb_json).split('\n\n\n')
print("\n".join(markdown))
```



stdout:
 

    
    # Hello world!
    
    
    ---
    
    ``` python linenums="1"
    import os
    os
    ```
    ---
    
    ---
    
    ``` python linenums="1"
    
    ```
    ---
     
    

 



---




## More on Templates

As most of the heavy-lifting in this method is done by the jinja template, you can customize the output by modifying the template. The default template can be accessed via the `ipynb2md_default_template` variable or from `templates['ipynb2md_default']`. You can use this as a starting point for writing your own template.




---

``` python linenums="1"
pymddoc.templates['ipynb2md_default']
print(pymddoc.ipynb2md_default_template)
```



stdout:
 

    
    {% for cell in cells %}
    {% if cell.cell_type == 'markdown' %}
    {{ cell.source|join("") }}
    {% elif cell.cell_type == 'code' %}
    
    ---
    
    ``` python linenums="1"
    {{ cell.source|join("") }}
    ```
    {% for output in cell.outputs%}
    {%if output.output_type == 'stream'%}
    {%if output.name == 'stdout'%}
    stdout:
    {% elif output.name == 'stderr'%}
    stderr:
    {%endif%} {# end if name #}
    
    {{ indent(output.text|join("")) }}
    
    {%elif output.output_type == 'data' or output.output_type == 'display_data' or output.output_type == 'execute_result' %}
    
    {%if 'text/plain' in output.data%}
    text:
    
    {{ indent(output.data['text/plain']|join("")) }}
    {%endif%} {# end test/plain #}
    
    
    {%if 'text/html' in output.data%}
    html:
    
    {{ indent(output.data['text/html']|join("")) }}
    {%endif%} {# end if text/html #}
    
    
    {%endif%} {# end if output_type #}
    
    {%endfor%}
    
    ---
    
    {% endif %}
    {% endfor %} {# end for cells #}
    
    

 



---


 