from __future__ import annotations
import dataclasses
import dateutil.parser

import io
import contextlib
import typing
import inspect

import datetime

@dataclasses.dataclass
class Metadata:
    title: str
    subtitle: str
    author: str
    date: datetime.datetime
    other_metadata: typing.Dict[str, str]
    
    @classmethod
    def new(cls, 
        title: typing.Optional[str] = None,
        subtitle: typing.Optional[str] = None,
        author: typing.Optional[str] = None,
        date: typing.Optional[typing.Union[str, datetime.datetime]] = None,
        **other_metadata,
    ) -> Metadata:
        return cls(
            title = title,
            subtitle = subtitle,
            author = author,
            date = dateutil.parser.parse(date) if date is not None else None,
            other_metadata = other_metadata,
        )
        
    def render_yaml(self) -> str:
        '''Render this text as yaml. Looks funky bc copilot wrote it.
        '''
        return '\n'.join([
            '---',
            *[
                f'{k}: {v}'
                for k, v in self.asdict().items() if v is not None
            ],
            '---\n\n',
        ])
    
    def asdict(self):
        '''Flatten to dict.'''
        return {
            'title': self.title,
            'subtitle': self.subtitle,
            'author': self.author,
            'date': self.date,
            **self.other_metadata,
        }
    