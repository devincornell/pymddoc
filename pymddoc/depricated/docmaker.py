from __future__ import annotations

import inspect
import dataclasses
import typing
import pathlib
import jinja2
import pypandoc # type: ignore
import datetime

from .markdown import Markdown
from ..snippet import SnippetCtx, SnippetFormatter, SnippetTemplateType, SnippetInfo, split_map_join
from ..metadata import Metadata


Component = typing.Union[Markdown, SnippetInfo]

def Document(
        title: typing.Optional[str] = None,
        subtitle: typing.Optional[str] = None,
        author: typing.Optional[str] = None,
        date: typing.Optional[typing.Union[str, datetime.datetime]] = None,
        other_metadata: typing.Optional[typing.Dict[str, str]] = None,
        snippet_template: typing.Optional[SnippetTemplateType] = None,
) -> DocMaker:
    '''Construct a new docmaker.'''
    return DocMaker.from_params(
        title = title,
        subtitle = subtitle,
        author = author,
        date = date,
        other_metadata = other_metadata,
        snippet_template = snippet_template,
    )

@dataclasses.dataclass
class DocMaker:
    '''Will create a document that can be rendered to markdown or html.'''
    metadata: Metadata
    default_snippet_formatter: SnippetFormatter
    components: typing.List[Component]
    
    @classmethod
    def from_params(cls,
        title: typing.Optional[str] = None,
        subtitle: typing.Optional[str] = None,
        author: typing.Optional[str] = None,
        date: typing.Optional[typing.Union[str, datetime.datetime]] = None,
        other_metadata: typing.Optional[typing.Dict[str, str]] = None,
        snippet_template: typing.Optional[SnippetTemplateType] = None,
    ) -> DocMaker:
        formatter = SnippetFormatter.default()
        other_metadata = other_metadata if other_metadata is not None else dict()
        return cls(
            metadata = Metadata.new(
                title = title,
                subtitle = subtitle,
                author = author,
                date = date,
                **other_metadata,
            ),
            default_snippet_formatter = formatter.override(
                template = snippet_template,
            ),
            components = list(),
        )
    
    ################ expose metadata ################
    @property
    def title(self) -> str:
        return self.metadata.title
    
    @property
    def subtitle(self) -> str:
        return self.metadata.subtitle
    
    @property
    def author(self) -> str:
        return self.metadata.author
    
    @property
    def date(self) -> typing.Optional[datetime.datetime]:
        return self.metadata.date
    
    @property
    def other_metadata(self) -> typing.Dict[str, str]:
        return self.metadata.other_metadata
    
    ################ snippets ################
    def markdown(self, 
        text: str, 
        indent: str = '', 
    ) -> Markdown:
        '''Add markdown to the document.'''
        new_md = Markdown(
            text = text,
            indent = indent,
        )
        self.components.append(new_md)
        return new_md
    
    ################ snippets ################
    def snippet(self, 
        frame: inspect.FrameInfo,
        template: typing.Optional[SnippetTemplateType] = None,
        print_stdout: bool = False,
    ) -> SnippetCtx:
        '''Context manager for adding code snippets to the document.'''
        return SnippetCtx.new(
            frame = frame,
            print_stdout = print_stdout,
            snippet_info_callback = self.components.append,
            formatter = self.default_snippet_formatter.override(
                template=template,
            ),
        )
    
    ################ rendering a document directly from the py file ################
    def render_html(self, **markdown_kwargs) -> str:
        '''Render the document to html.'''
        text = self.render_markdown(**markdown_kwargs)
        return pypandoc.convert_text(text, 'html', format='md')
    
    def render_markdown(self, include_yaml: bool = True) -> str:
        '''Render the existing document into markdown.'''
        output = ''
        
        if include_yaml:
            output += self.metadata.render_yaml()
        
        for comp in self.components:
            if isinstance(comp, Markdown):
                output += comp.get_text()
            elif isinstance(comp, SnippetInfo):
                output += comp.render()
            output += '\n\n'
            
        output = split_map_join(lambda l: l if len(l.strip()) > 0 else l.strip(), output)
        return output
    
    
    