import typing
from pathlib import Path
import dataclasses
import jinja2.meta
import pypandoc # type: ignore
import json
import jinja2
import tempfile

from .metadata import Metadata
from .builtin_methods import get_builtin_methods
from .util import val_or_None

from .render import jinja_render, jinja_get_variables
from .compile import pandoc_convert_text, pandoc_convert_file, PandocArgs




@dataclasses.dataclass(repr=False)
class MarkdownDoc:
    '''Used to manipulate markdown data using pypandoc.'''
    md_text: str

    @classmethod
    def from_file(cls, fpath: Path) -> typing.Self:
        '''Read markdown from the file.'''
        with Path(fpath).open('r') as f:
            return cls.from_str(f.read())
        
    @classmethod
    def from_str(cls, md_text: str) -> typing.Self:
        '''Instantiate from a string.'''
        return cls(str(md_text))
    
    ###################### Extract Component Data ######################
    def extract_metadata(self) -> Metadata:
        '''Get metadata from the document'''
        return Metadata.from_markdown_text(self.md_text)

    ###################### type-specific methods ######################
    def render_to_docx(self,
        output_path: Path,
        vars: typing.Optional[dict[str,typing.Any]] = None,
        strict_render: bool = True,
        pandoc_args: PandocArgs | None = None,
    ) -> str | bytes:
        '''Render the markdown document as a jinja template and then.'''
        return self.render_to_file(
            output_path=output_path,
            output_format='docx',
            vars=vars,
            strict_render=strict_render,
            pandoc_args=pandoc_args,
        )

    def render_to_pdf(self,
        output_path: Path,
        vars: typing.Optional[dict[str,typing.Any]] = None,
        strict_render: bool = True,
        pandoc_args: PandocArgs | None = None,
    ) -> str:
        '''Render the markdown document as a jinja template and then.'''
        return self.render_to_file(
            output_path=output_path,
            output_format='pdf',
            vars=vars,
            strict_render=strict_render,
            pandoc_args=pandoc_args,
        )

    def render_html(self,
        vars: typing.Optional[dict[str,typing.Any]] = None,
        strict_render: bool = True,
        pandoc_args: PandocArgs | None = None,
    ) -> str:
        '''Render the markdown document to html with jinja/pandoc.'''
        return self.render_to_string(
            output_format='html',
            vars=vars,
            strict_render=strict_render,
            pandoc_args=pandoc_args,
        )
    
    ###################### generic rendering ######################
    def render_to_file(self,
        output_path: Path,
        output_format: typing.Literal['html', 'pdf', 'docx'] | None = None,
        vars: typing.Optional[dict[str,typing.Any]] = None,
        strict_render: bool = True,
        pandoc_args: PandocArgs | None = None,
    ) -> str:
        '''Render/compile the markdown document to a file using jinja/pandoc.
        Args:
            output_path: path to the output file.
            output_format: the format of the output file.
            vars: the variables to substitute into the jinja template.
            strict_render: if True, raise an error if not all variables are provided.
            pandoc_args: the arguments for the pandoc conversion.
        '''
        with tempfile.TemporaryDirectory() as tmp:

            # jinja render step
            rendered = jinja_render(
                input_text=self.md_text,
                vars={
                    **get_builtin_methods(
                        tmp_dir=tmp, 
                        output_format=output_format
                    ), 
                    **val_or_None(vars, {}),
                }, 
                strict=strict_render,
            )

            # create dummy file to temporarily dump input
            tmp_source_path = Path(f'{tmp}/source_input.md')
            with tmp_source_path.open('w') as f:
                f.write(rendered)

            return pandoc_convert_file(
                input_path=tmp_source_path,
                input_format='md',
                output_path=output_path,
                output_format=output_format, 
                pandoc_args=pandoc_args,
            )


    def render_to_string(self,
        output_format: typing.Literal['html'],
        vars: typing.Optional[dict[str,typing.Any]] = None,
        strict_render: bool = True,
        pandoc_args: PandocArgs | None = None,
    ) -> str:
        '''Render the markdown document to a string using jinja/pandoc.
        Args:
            output_format: the format of the output file.
            vars: the variables to substitute into the jinja template.
            strict_render: if True, raise an error if not all variables are provided.
            pandoc_args: the arguments for the pandoc conversion.
        '''

        with tempfile.TemporaryDirectory() as tmp:

            # jinja render step
            rendered = jinja_render(
                input_text=self.md_text,
                vars={
                    **get_builtin_methods(tmp_dir=tmp, output_format=output_format), 
                    **val_or_None(vars, {}),
                }, 
                strict=strict_render,
            )

            # pandoc compile step
            return pandoc_convert_text(
                input_text=rendered,
                input_format='md',
                output_format=output_format, 
                pandoc_args=pandoc_args,
            )

    ###################### templating ######################
    def render_template(self,
        vars: dict[str,typing.Any],
        strict_render: bool = False,
    ) -> typing.Self:
        '''Render the markdown document as a jinja template.'''
        return self.from_str(
            md_text=jinja_render(
                input_text=self.md_text,
                vars=vars,
                strict=strict_render,
            )
        )
    
    def get_template_variables(self) -> list[str]:
        '''Get the variables in the jinja template.'''
        return jinja_get_variables(self.md_text)

    ###################### dunder ######################
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.extract_metadata()})'
