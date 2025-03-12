import typing
from pathlib import Path
import dataclasses
import jinja2.meta
import pypandoc
import json
import jinja2
import tempfile

from .util import val_or_None, map_or_None

InputFormat = typing.Literal['md', 'markdown']
RenderFormat = typing.Literal['html', 'pdf', 'docx']

@dataclasses.dataclass
class PandocArgs:
    '''Dataclass that contains arguments for pandoc conversion.
        See this page for more about pandoc markdown:
            https://quarto.org/docs/authoring/markdown-basics.html
    Args:
        standalone: adds the --standalone flag to the pandoc command.
        embed_resources: adds the --embed-resources flag to the pandoc command.
        toc: adds the --toc flag to the pandoc command.
        citeproc_bibliography: adds the --citeproc and --bibliography {fname}
            arguments to the pandoc command.
        template: adds the --template={fname} argument to the pandoc command.
        extra_args: additional arguments to add to the pandoc command.
        **pandoc_kwargs: passed to pandoc.
    '''
    standalone: bool = False
    embed_resources: bool = False
    toc: bool = False
    citeproc_bibliography: Path | None = None
    template: Path | None = None
    extra_args: list[str] | None = None
    pandoc_kwargs: dict[str,typing.Any] | None = None

    def to_list(self) -> tuple[list[str], dict[str,typing.Any]]:
        '''Accept specific args to create list of arguments for the pandoc conversion.
        Example: pandoc ... --standalone --embed-resources -f markdown --toc --citeproc --bibliography {filename}
        '''
        extra_args: list[str] = val_or_None(self.extra_args, [])

        if self.template is not None:
            extra_args.append(f'--template={self.template}')

        if self.standalone:
            extra_args.append('--standalone')
        
        if self.embed_resources:
            extra_args.append('--embed-resources')

        if self.toc:
            extra_args.append('--toc')

        if self.citeproc_bibliography is not None:
            extra_args += ['--citeproc', '--bibliography', f'{self.citeproc_bibliography}']

        return extra_args, val_or_None(self.pandoc_kwargs, {})



###################### Converting to Other Formats with Pandoc ######################
def pandoc_convert_text(
    input_text: str,
    input_format: typing.Literal['md', 'markdown'],
    output_format: typing.Literal['html'],
    pandoc_args: PandocArgs | None = None,
) -> str:
    '''Convert the markdown file to another template.
        See this page for more about pandoc markdown:
            https://quarto.org/docs/authoring/markdown-basics.html
    Args:
        input_text: the markdown text to convert.
        input_format: the format of the input file.
        output_format: the format of the output file.
        pandoc_args: the arguments for the pandoc conversion.
    '''
    pandoc_args = val_or_None(pandoc_args, PandocArgs())
    extra_args, kwargs = pandoc_args.to_list()

    return pypandoc.convert_text(
        source=input_text, 
        to=output_format,
        format=input_format,
        extra_args=extra_args,
        **kwargs
    )

def pandoc_convert_file(
    input_path: Path,
    input_format: str,
    output_path: Path,
    output_format: typing.Optional[typing.Literal['html', 'pdf', 'docx']] = None,
    pandoc_args: PandocArgs | None = None,
) -> str:
    '''Convert the markdown text to a file using pandoc.
        See this page for more about pandoc markdown:
            https://quarto.org/docs/authoring/markdown-basics.html
    Args:
        input_path: path to the input markdown file.
        input_format: the format of the input file.
        output_path: path to the output file.
        output_format: the format of the output file.
        pandoc_args: the arguments for the pandoc conversion.
    '''
    input_path = map_or_None(input_path, Path)
    output_path = map_or_None(output_path, Path)
    
    pandoc_args = val_or_None(pandoc_args, PandocArgs())
    extra_args, kwargs = pandoc_args.to_list()

    return pypandoc.convert_file(
        source_file=str(input_path), 
        to = val_or_None(output_format, output_path.suffix[1:]),
        format=input_format,
        outputfile=str(output_path),
        extra_args=extra_args,
        **kwargs,
    )

