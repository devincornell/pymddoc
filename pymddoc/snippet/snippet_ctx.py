import inspect
import dataclasses
import io
import typing
import contextlib

from .snippet_formatter import SnippetFormatter
from .snippet_info import SnippetInfo

@dataclasses.dataclass
class SnippetCtx:
    '''Context manager for capturing source code and stdout.'''
    frame: inspect.FrameInfo
    print_stdout: bool
    snippet_info_callback: typing.Callable[[SnippetInfo], None]
    formatter: SnippetFormatter
    source: typing.Optional[str]
    stdout: typing.Optional[str]
    stdout_ctx: typing.Optional[contextlib._RedirectStream]
    
    
    @classmethod
    def new(cls, 
        frame: inspect.FrameInfo,
        print_stdout: bool,
        snippet_info_callback: typing.Callable[[SnippetInfo], None],
        formatter: SnippetFormatter,
    ):
        return SnippetCtx(
            frame = frame,
            print_stdout = print_stdout,
            snippet_info_callback = snippet_info_callback,
            formatter=formatter,
            source = None,
            stdout = None,
            stdout_ctx = None,
        )
    
    ############ context managers ############
    def __enter__(self):
        self.source = self.read_source()
        self.start_capture_stdout()
        return self
    
    def __exit__(self, *args):
        self.stdout = self.end_capture_stdout(*args)
        
        # send back to manager object.
        self.snippet_info_callback(self.snippet_info())
        
        if self.print_stdout:
            print(self.stdout)
        
    ############ returning block info ############
    def snippet_info(self) -> SnippetInfo:
        return SnippetInfo(
            source = self.source,
            stdout = self.stdout,
            formatter=self.formatter,
        )
        
    ############ Standard Output ############
    def start_capture_stdout(self):
        self.buff = io.StringIO()
        self.stdout_ctx = contextlib.redirect_stdout(self.buff)
        self.stdout_ctx.__enter__()
        
    def end_capture_stdout(self, *args):
        stdout = self.buff.getvalue()
        self.stdout_ctx.__exit__(*args)
        return stdout.rstrip()
        
    ############ Getting source code ############
    def read_source(self) -> str:
        tb = inspect.getframeinfo(self.frame)
        fname = inspect.getsourcefile(self.frame)
        start, end = tb.positions.lineno, tb.positions.end_lineno
        
        try:
            with open(fname, 'r') as f:
                # NOTE: readlines retains newline at end of line
                source = ''.join(f.readlines()[start:end]).rstrip()
        except FileNotFoundError:
            source = 'COULD NOT FIND SOURCE'
        return source

    

