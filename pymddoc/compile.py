import typing
from pathlib import Path
import dataclasses
import jinja2.meta
import pypandoc
import json
import jinja2
import tempfile

from .util import val_or_None, map_or_None


###################### Converting to Other Formats with Pandoc ######################
def convert_text(
    input_text: str,
    input_format: str,
    output_format: typing.Literal['html'],
    standalone: bool = False,
    embed_resources: bool = False,
    toc: bool = False,
    citeproc_bibliography: typing.Optional[Path] = None,
    template: typing.Optional[Path] = None,
    extra_args: typing.Optional[list[str]] = None,
    **kwargs
) -> str:
    '''Convert the markdown file to another template.
        See this page for more about pandoc markdown:
            https://quarto.org/docs/authoring/markdown-basics.html
    '''
    extra_args = parse_args(
        standalone=standalone,
        embed_resources=embed_resources,
        toc=toc,
        citeproc_bibliography=citeproc_bibliography,
        template=template,
        extra_args=extra_args,
    )
    return pypandoc.convert_text(
        source=input_text, 
        to=output_format,
        format=input_format,
        extra_args=extra_args,
        **kwargs
    )

def convert_file(
    input_path: Path,
    input_format: str,
    output_path: Path,
    output_format: typing.Optional[typing.Literal['html', 'pdf', 'docx']] = None,
    standalone: bool = False,
    embed_resources: bool = False,
    toc: bool = False,
    citeproc_bibliography: typing.Optional[Path] = None,
    template: typing.Optional[Path] = None,
    extra_args: typing.Optional[list[str]] = None,
    **kwargs
) -> str | bytes:
    '''Convert the markdown text to a file using pandoc.
        See this page for more about pandoc markdown:
            https://quarto.org/docs/authoring/markdown-basics.html
    '''
    input_path = map_or_None(input_path, Path)
    output_path = map_or_None(output_path, Path)

    extra_args = parse_args(
        standalone=standalone,
        embed_resources=embed_resources,
        toc=toc,
        citeproc_bibliography=citeproc_bibliography,
        template=template,
        extra_args=extra_args,
    )

    return pypandoc.convert_file(
        source_file=str(input_path), 
        to = val_or_None(output_format, output_path.suffix[1:]),
        format=input_format,
        outputfile=str(output_path),
        extra_args=extra_args,
        **kwargs,
    )

def parse_args(
    standalone: bool = False,
    embed_resources: bool = False,
    toc: bool = False,
    citeproc_bibliography: typing.Optional[Path] = None,
    template: typing.Optional[Path] = None,
    extra_args: typing.Optional[list[str]] = None,
) -> list[str]:
    '''Accept specific args to create list of arguments for the pandoc conversion.
    Example: pandoc ... --standalone --embed-resources -f markdown --toc --citeproc --bibliography {filename}
    Args:
        standalone: bool = False
            If true, the output will be a standalone document.
        embed_resources: bool = False
            If true, resources will be embedded in the output.
        toc: bool = False
            If true, a table of contents will be generated.
        citeproc_bibliography: typing.Optional[Path] = None
            If not None, the path to a bibliography file.
        template: If not None, the path to a template file.
        extra_args: typing.Optional[list[str]] = None
    '''
    extra_args: list[str] = val_or_None(extra_args, [])

    if template is not None:
        extra_args.append(f'--template={template}')

    if standalone:
        extra_args.append('--standalone')
    
    if embed_resources:
        extra_args.append('--embed-resources')

    if toc:
        extra_args.append('--toc')

    if citeproc_bibliography is not None:
        extra_args += ['--citeproc', f'--bibliography {citeproc_bibliography}']

    return extra_args
