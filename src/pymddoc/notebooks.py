import jinja2

from .util import indent

def convert_ipynb2md(template: str, ipynb_data: dict) -> str:
    env = jinja2.Environment()
    template = env.from_string(template, globals={'indent': indent})
    markdown = template.render(**ipynb_data)
    return markdown




