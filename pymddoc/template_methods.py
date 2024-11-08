import pathlib
import pandas as pd
import typing
from .util import val_or_None, TempPath


def csv_to_md(
    fname: str, 
    num_rows: int | None = None,
    read_kwargs: dict[str,typing.Any] | None = None, 
    to_markdown_kwargs: dict[str,typing.Any] | None = None
) -> str:
    '''Read a csv file from disk and insert it into the document as markdown.
    Args:
        fname: str: The file name to read.
        num_rows: int | None: The number of rows to read.
        read_kwargs: dict[str,typing.Any] | None: The keyword arguments to pass to the read
            function.
        to_markdown_kwargs: dict[str,typing.Any] | None: The keyword arguments to pass to the
    '''
    return table_to_md(
        pd.read_csv,
        fname = fname,
        num_rows=num_rows,
        read_kwargs=read_kwargs,
        to_markdown_kwargs=to_markdown_kwargs,
    )


def excel_to_md(
    fname: str, 
    num_rows: int | None = None,
    read_kwargs: dict[str,typing.Any] | None = None, 
    to_markdown_kwargs: dict[str,typing.Any] | None = None
) -> str:
    '''Read an excel file from disk and insert it into the document as markdown.
    Args:
        fname: str: The file name to read.
        num_rows: int | None: The number of rows to read.
        read_kwargs: dict[str,typing.Any] | None: The keyword arguments to pass to the read
            function.
        to_markdown_kwargs: dict[str,typing.Any] | None: The keyword arguments to pass to the
    '''
    return table_to_md(
        pd.read_excel,
        fname = fname,
        num_rows=num_rows,
        read_kwargs=read_kwargs,
        to_markdown_kwargs=to_markdown_kwargs,
    )

def table_to_md(
    read_func: typing.Callable[..., pd.DataFrame],
    fname: str, 
    num_rows: int | None = None,
    read_kwargs: dict[str,typing.Any] | None = None, 
    to_markdown_kwargs: dict[str,typing.Any] | None = None
) -> str:
    '''Read a table file from disk and insert it into the document as markdown.
    Args:
        read_func: typing.Callable[..., pd.DataFrame]: The function to read the table.
        fname: str: The file name to read.
        num_rows: int | None: The number of rows to read.
        read_kwargs: dict[str,typing.Any] | None: The keyword arguments to pass to the read
            function.
        to_markdown_kwargs: dict[str,typing.Any] | None: The keyword arguments to pass to the
    '''
    #read_kwargs = read_kwargs if read_kwargs is not None else {}
    read_kwargs = val_or_None(read_kwargs, {})
    #to_markdown_kwargs = to_markdown_kwargs if to_markdown_kwargs is not None else {}
    to_markdown_kwargs = val_or_None(to_markdown_kwargs, {})

    df = read_func(fname, **read_kwargs)

    if num_rows is not None:
        df = df.head(int(num_rows))

    to_markdown_kwargs = {'index': False, **to_markdown_kwargs}
    df_md = df.to_markdown(**to_markdown_kwargs)

    return df_md


def comment(message: str):
    '''Write text that will not appear in the document.'''
    return ''




TEMPLATE_METHODS = {
    'c': comment,
    'comment': comment,
    'csv_to_markdown': csv_to_md,
    'excel_to_markdown': excel_to_md,
    'home_dir': str(pathlib.Path('~/').expanduser()),
}

