import typing
from pathlib import Path
import dataclasses
import pypandoc
import json
import tempfile

from .metadata import Metadata


@dataclasses.dataclass
class MarkdownDocument:
    '''Used to manipulate markdown data using pypandoc.'''
    md_text: str

    @classmethod
    def from_file(cls, fpath: Path) -> typing.Self:
        with Path(fpath).open('r') as f:
            return cls.from_str(f.read())
        
    @classmethod
    def from_str(cls, md_text: str) -> typing.Self:
        return cls(str(md_text))
    
    def convert_text(self,
        to_format: typing.Literal['html'],
        template: typing.Optional[Path] = None,
        extra_args: typing.Optional[list[str]] = None,
        **kwargs
    ) -> str:
        '''Convert the markdown file to another template.'''
        extra_args = extra_args if extra_args is not None else []
        if template is not None:
            extra_args.append(f'--template={template}')
        
        return pypandoc.convert_text(
            source=self.md_text, 
            to=to_format,
            format='md',
            extra_args=extra_args,
            **kwargs
        )
    
    def convert_file(self,
        output: Path,
        output_format: typing.Optional[typing.Literal['html', 'pdf', 'docx']] = None,
        template: typing.Optional[Path] = None,
        extra_args: typing.Optional[list[str]] = None,
        **kwargs
    ) -> str | bytes:
        '''Convert the markdown text to a file.'''
        output = Path(output)

        extra_args = extra_args if extra_args is not None else []
        if template is not None:
            extra_args.append(f'--template={template}')
        
        with tempfile.TemporaryDirectory() as tmp:
            tmp_source_path = Path(f'{tmp}/source_input.md')
            with tmp_source_path.open('w') as f:
                f.write(self.md_text)

            return pypandoc.convert_file(
                source_file=str(tmp_source_path), 
                to = output_format if output_format is not None else output.suffix[1:],
                outputfile=str(output),
                format='md',
                extra_args=extra_args,
                **kwargs,
            )

    def extract_metadata(self) -> Metadata:
        '''Get metadata from the document'''
        return Metadata.from_markdown_text(self.md_text)



