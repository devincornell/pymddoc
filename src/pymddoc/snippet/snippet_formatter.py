from __future__ import annotations

import jinja2
import dataclasses
import typing

from .renderutils import split_map_join, map_line
from .snippet_templates import templates, SnippetTemplateType

@dataclasses.dataclass
class SnippetFormatter:
    template: SnippetTemplateType
    
    @classmethod
    def default(cls) -> SnippetFormatter:
        '''Get formatter defaults.'''
        return cls(
            template = templates.default(),
        )
        
    def override(self, **kwargs):
        return dataclasses.replace(self, **{k:v for k,v in kwargs.items() if v is not None})
    
    
    def render(self, source: str, stdout: str) -> str:
        '''Accept information about the snippet and produce output according to params.'''
        if isinstance(self.template, str):
            renderer = templates.get_jinja_renderer(self.template)
            return renderer(
                self.format_source(source),
                self.format_stdout(stdout),
            )
        
        elif callable(self.template):
            return self.template(
                self.format_source(source),
                self.format_stdout(stdout),
            )
        else:
            raise ValueError(f'Invalid template type: {type(self.template)}. '
                'Template should be either string or callable accepting '
                'source, stdout, and output.')
    
    ################ format output and stdout  ################    
    def format_stdout(self, stdout: str) -> typing.Optional[str]:
        '''Format stdout before sending to template.'''
        return ss if (ss := stdout.strip()) != '' else None
    
    ################ SOURCE CODE  ################
    def format_source(self, source: str) -> str:
        '''Get source code including function definition and removing indent level.'''
        source = source.rstrip() # remove trailing whitespace
        
        # remove baseline level of indentation
        indents = map_line(lambda l: len(l) - len(l.lstrip()) if len(l) > 0 else float('inf'), source)
        start_indent = min(indents) if len(indents) > 0 else 0
        source = split_map_join(lambda l: l[start_indent:], source)
        
        return source

    
    

    