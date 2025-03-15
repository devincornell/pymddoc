import typing
import tempfile
import pathlib

from .errors import PandocError

T = typing.TypeVar("T")
U = typing.TypeVar("U")


def indent(text: str) -> str:
    indented_text = "    " + "\n    ".join(text.split("\n"))
    return indented_text

def pandoc_execute(command: typing.Callable, *args, **kwargs):
    '''Run a pandoc command and return the output.'''
    try:
        return command(*args, **kwargs)
    except RuntimeError as e:
        raise PandocError(f'{e}') from e

def val_or_None(v: T | None, default: T) -> T:
    '''Return v if it is not None, otherwise return default.'''
    return v if v is not None else default

def map_or_None(v: T, f: typing.Callable[[T], U]) -> U:
    '''Apply f to v if v is not None, otherwise return None.'''
    return f(v) if v is not None else None

class TempPath:
    '''Create a temporary path that is deleted when the context is exited.'''
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()

    def __enter__(self):
        return pathlib.Path(self.tmp)

    def __exit__(self, *args):
        self.tmp.cleanup()


