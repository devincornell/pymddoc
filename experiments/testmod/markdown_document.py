import typing
from pathlib import Path
import dataclasses
from .metadata import Metadata
import pypandoc

@dataclasses.dataclass
class MarkdownDocument:
    '''Used to manipulate markdown data using pypandoc.'''
    md_text: str

    @classmethod
    def from_file(cls, fpath: Path) -> typing.Self:
        with fpath.open('r') as f:
            return cls.from_str(f.read())
        
    @classmethod
    def from_str(cls, md_text: str) -> typing.Self:
        return cls(str(md_text))
    
    def convert_text(self,
        to_format: typing.Literal['html', 'docx', 'pdf'],
        template: typing.Optional[Path],
        extra_args: typing.Optional[list[str]],
    ) -> str | bytes:
        extra_args = extra_args if extra_args is not None else []
        if template is not None:
            extra_args.append(f'--template={template}')
        
        return pypandoc.convert_text(
            self.md_text, 
            to=to_format,
            format='md',
            extra_args=extra_args,
        )

        
    def extract_metadata(self) -> Metadata:
        '''Get metadata from the document'''
        return Metadata.from_markdown_text(self.md_text)



