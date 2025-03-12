from __future__ import annotations

import dataclasses

import io
import contextlib
import typing
import inspect
import pypandoc

from ..snippet import split_map_join, map_line

@dataclasses.dataclass
class Markdown:
    '''Represents a markdown text in the document.'''
    text: str
    indent: str
    
    def pandoc_render(self, format: str, **pandoc_kwargs) -> str:
        '''Render this text to desired format using pandoc.'''
        text = self.get_text()
        return pypandoc.convert_text(text, format, format='md', **pandoc_kwargs)
    
    def get_text(self) -> str:
        '''Get the preprocessed text of the markdown.'''
        text = self.remove_indent(self.text)
        text = split_map_join(lambda l: self.indent+l, text)
        return text

    ################ Util ################
    @classmethod
    def remove_indent(cls, text: str) -> str:
        '''Remove the indent level of the text.'''
        indents = map_line(lambda l: len(l) - len(l.lstrip()) if len(l) > 0 else float('inf'), text)
        start_indent = min(indents) if len(indents) > 0 else 0
        return split_map_join(lambda l: l[start_indent:], text)
    

