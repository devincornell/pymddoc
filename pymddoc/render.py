import typing
import jinja2
import pathlib

import jinja2.meta


def jinja_render(self, 
    input_text: str,
    vars: dict[str,typing.Any],
    strict: bool = True,
) -> typing.Self:
    '''Return the same document rendered as a jinja template.'''
    try:
        # NOTE: not sure which of these causes the exception
        template = text_as_jinja_template(input_text)
        rendered_text = template.render(vars)
    except jinja2.exceptions.TemplateSyntaxError as e:
        raise _add_line_number_to_exception_message(e)
    
    if strict and (jv := len(get_jinja_variables(input_text=rendered_text))):
        raise ValueError(f'strict=True but not all jinja template variables '
            f'have been provided: {jv}')
    return rendered_text


def get_jinja_variables(input_text: str) -> list[str]:
    '''Get list of jinja variables to populate.'''
    env = _get_jinja_environment()
    try:
        # NOTE: not sure which of these causes the exception
        parsed = env.parse(input_text)
        return jinja2.meta.find_undeclared_variables(parsed)
    except jinja2.exceptions.TemplateSyntaxError as e:
        raise _add_line_number_to_exception_message(e)


def text_as_jinja_template(
    input_text: str,
    globals: dict[str, typing.Any] | None = None,
) -> jinja2.Template:
    '''Get a jinja template of the current document.'''
    env = _get_jinja_environment()
    return env.from_string(
        source = input_text,
        globals = globals,
    )

@staticmethod
def _add_line_number_to_exception_message(
    e: jinja2.exceptions.TemplateSyntaxError
) -> jinja2.exceptions.TemplateSyntaxError:
    '''Add line number to error message of TemplateSyntaxError.'''
    if 'Missing end of comment tag' in e.message:
        addendum = ('This may be due to lack of whitespace around curly '
            'brackets in markdown classes. Use spacing such as "{ #id" '
            'when specifying an ID using pandoc\'s marking tool. It may '
            'otherwise be some other interaction between jinja and pandoc.'
        )
    else:
        addendum = ''

    return jinja2.exceptions.TemplateSyntaxError(
        message=f'{e.message} on line {e.lineno}. {addendum}',
        lineno=e.lineno,
        name=e.name,
        filename=e.filename,
    )

@staticmethod
def _get_jinja_environment(**environment_kwargs) -> jinja2.Environment:
    '''Get environment for jinja. Consistency across the object.'''
    return jinja2.Environment(**environment_kwargs)


