import jinja2
import json
import pathlib
from pathlib import Path
import sys
import click

from .info import package_name
from .templates import templates
from .markdown_doc import MarkdownDoc
from .errors import PandocError

from .notebooks import convert_ipynb2md

def get_default_ipynb2md_template():
    """Get the content of the default template inside the package."""
    return templates['ipynb2md_default']

def handle_error(e: Exception) -> None:
    print(f'Error: {e}', file=sys.stderr)


@click.group()
def cli():
    pass

@cli.command()
@click.argument('ipynb_file', type=click.Path(exists=True))
@click.argument('md_file', type=click.Path())
@click.option("--template", type=click.Path(exists=True), default=None)
def ipynb2md(ipynb_file: str, md_file: str, template: str) -> None:
    '''Convert a Jupyter notebook (json file) to a markdown file.
    Description: reads a jupyter notebook as a regular json file, passes the json to the template,
        and renders the template with the json information.
    '''
    with Path(ipynb_file).open('r') as f:
        ipynb_dict = json.load(f)
    
    if template is not None:
        with Path(template).open('r') as f:
            template_str = f.read()
    else:
        template_str = get_default_ipynb2md_template()

    markdown = convert_ipynb2md(template_str, ipynb_dict)

    with Path(md_file).open('w') as f:
        f.write(markdown)


@cli.command()
@click.argument('ipynb_files', nargs=-1, type=click.Path(exists=True))
@click.option("--template", type=click.Path(exists=True), default=None)
def ipynb2md_multi(ipynb_files: list[str], template: str) -> None:
    '''Convert a Jupyter notebook (json file) to a markdown file.
    Description: reads a jupyter notebook as a regular json file, passes the json to the template,
        and renders the template with the json information.
    '''
    for ipynb_file in ipynb_files:
        with Path(ipynb_file).open('r') as f:
            ipynb_dict = json.load(f)
        
        if template is not None:
            with Path(template).open('r') as f:
                template_str = f.read()
        else:
            template_str = get_default_ipynb2md_template()

        markdown = convert_ipynb2md(template_str, ipynb_dict)

        md_file = Path(ipynb_file).with_suffix('.md')
        with Path(md_file).open('w') as f:
            f.write(markdown)


@cli.command()
@click.argument('md_file', type=click.Path())
def metadata(md_file: str) -> None:
    '''Extract metadata from a markdown file as json.
    '''
    doc = MarkdownDoc.from_file(md_file)
    try:
        md = doc.extract_metadata()
    except PandocError as e:
        handle_error(e)
        return
    print(json.dumps(md, indent=2))


@cli.command()
@click.argument('md_file', type=click.Path())
@click.argument('out_file', type=click.Path())
@click.option('--out_format', type=click.Choice(['html', 'pdf', 'docx']), default=None)
@click.option('--strict_render', type=click.BOOL, default=True)
def render(md_file: str, out_file: str, out_format: str|None, strict_render: bool) -> None:
    '''Render and compile a markdown file.
    '''
    doc = MarkdownDoc.from_file(md_file)
    try:
        doc.render_to_file(
            output_path=Path(out_file),
            output_format=out_format,
            strict_render=bool(strict_render),
        )
    except PandocError as e:
        handle_error(e)


if __name__ == '__main__':
    cli()


