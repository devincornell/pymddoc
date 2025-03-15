
ipynb2md_default = '''
{% for cell in cells %}
{% if cell.cell_type == 'code' %}
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
{%endif%}
{{ indent(output.text|join("")) }}
{%endif%}
{%if output.output_type == 'data'%}
{{ indent(output.data.text/plain|join("")) }}
{%endif%}
{%endfor%}

---

{% elif cell.cell_type == 'markdown' %}
{{ cell.source|join("") }}
{% endif %}
{% endfor %}
'''

