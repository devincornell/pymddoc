import typing
import tempfile
import pypandoc
from pathlib import Path
import json

class Metadata(dict[str,str|int|bool|float]):
    '''Store and manage document metadata. dict subtype.'''

    def from_markdown_text(markdown_text: str) -> dict[str,typing.Any]:
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

