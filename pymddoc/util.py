import typing
import tempfile
import pathlib

def val_or_None(v: typing.Any, default: typing.Any):
    '''Return v if it is not None, otherwise return default.'''
    return v if v is not None else default

def map_or_None(v: typing.Any, f: typing.Callable[[typing.Any], typing.Any]):
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


