'''
The goal of this file is to read in a template, run any requested code, and compile to html/etc using pandoc.

You should be able to write academic papers and everything else.
'''
from __future__ import annotations
import typing

import jinja2


def compile(
    template_str: str,
    functions: dict[str,typing.Callable[...,typing.Any]],
) -> str:
    env = jinja2.Environment()
    template = env.from_string(
        source = template_str,
        globals = func_dict,
    )
    template.globals.update(func_dict)
    rendered = template.render(name="World")

    # compile with pandoc




if __name__ == '__main__':
    func_dict = {
        "hello_world": lambda: "hello world from within the function",
        "multiply": lambda x,y: x * y,
    }
    compile('Hi my name is {{name}}. I was wondering what you thought about the passage of prop 16?')