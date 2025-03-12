import functools
import typing
import jinja2

CallableTemplateType = typing.Callable[[str, typing.Optional[str]],str]
SnippetTemplateType = typing.Union[str, CallableTemplateType]

class templates:
    @classmethod
    def default(cls,
        source_header: str = '',
        stdout_header: str = '',
        source_indent: str = '    ', 
        stdout_indent: str = '    >> ', 
    ) -> CallableTemplateType:
        '''Shows indented source and output.'''
        return cls.get_jinja_renderer(
            template = DEFAULT_TEMPLATE,
            source_header = source_header,
            stdout_header = stdout_header,
            source_indent = source_indent,
            stdout_indent = stdout_indent,
        )
    
    @classmethod
    def source_only(cls,
        source_indent: str = '    ', 
    ) -> CallableTemplateType:
        '''Shows indented source and output.'''
        return cls.get_jinja_renderer(
            template = SOURCE_ONLY_TEMPLATE,
            source_indent = source_indent,
        )

    @classmethod
    def get_jinja_renderer(cls,
        template: str, 
        **template_params
    ) -> CallableTemplateType:
        '''Wrap a template function with a default formatter.'''
        def jinja_renderer(source: str, stdout: typing.Optional[str]) -> str:
            return jinja2.Template(template).render(
                source = source,
                stdout = stdout,
                **template_params,
            )
        return jinja_renderer


DEFAULT_TEMPLATE = (
'```python'
'{{source_header}}'
'{% for line in source.splitlines() %}'
'\n{{source_indent}}{{line}}'
'{% endfor %}'
'\n```\n\n'
'{% if stdout is not none%}'
'{{stdout_header}}\n\n'
'```'
'{% for line in stdout.splitlines() %}'
'\n{{stdout_indent}}{{line}}'
'{% endfor %}'
'\n```\n'
'{% endif %}'
)

SOURCE_ONLY_TEMPLATE = (
'```python'
'{% for line in source.splitlines() %}'
'\n{{source_indent}}{{line}}'
'{% endfor %}'
'\n```\n\n'
)







        
    


