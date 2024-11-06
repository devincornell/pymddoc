'''
The goal of this file is to read in a template, run any requested code, and compile to html/etc using pandoc.

You should be able to write academic papers and everything else.
'''
from __future__ import annotations
import typing

import jinja2
import pandoc
import pypandoc
from pathlib import Path

import tempfile
import json

import testmod

def pandoc_extract_meta(markdown_text: str) -> dict[str,typing.Any]:
    '''Read metadata from pandoc yaml header.'''
    with tempfile.TemporaryDirectory() as tmp:
        tmp_template_path = Path(f'{tmp}/metadata.pandoc-tpl')
        #tmp_output_path = Path(f'{tmp}/output.txt')

        # write the template text to a file
        with tmp_template_path.open('w') as f:
            f.write('$meta-json$')
        
        # run conversion to the template
        converted = pypandoc.convert_text(
            str(markdown_text), 
            to='html',
            format='md',
            #outputfile=str(tmp_output_path),
            extra_args=[
                f'--template={tmp_template_path}'
            ],
        )
        #with tmp_output_path.open('r') as f:
        #    return json.load(f)
        return json.loads(converted)


if __name__ == '__main__':

    with Path('template.md').open('r') as f:
        text = f.read()
        doc = pandoc.read(text)
        #print(doc)
    
    with Path('template.md').open('r') as f:
        md_text = f.read()
    
    print(pandoc_extract_meta(md_text))
    converted = pypandoc.convert_text(
        str(md_text), 
        to='html',
        format='md',
        #outputfile=str(tmp_output_path),
        extra_args=[
        ],
    )
    print(converted)
