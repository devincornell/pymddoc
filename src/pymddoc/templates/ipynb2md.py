
ipynb2md_default = '''
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
'''
ipynb2md_default = "\n".join([l.strip() for l in ipynb2md_default.split('\n')])
