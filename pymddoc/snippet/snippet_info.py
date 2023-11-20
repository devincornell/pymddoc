import inspect
import dataclasses
import io
import typing
import contextlib

#if typing.TYPE_CHECKING:
from .snippet_formatter import SnippetFormatter

@dataclasses.dataclass
class SnippetInfo:
    source: str
    stdout: str
    formatter: SnippetFormatter
    
    def render(self) -> str:
        return self.formatter.render(
            source = self.source,
            stdout = self.stdout,
        )
    