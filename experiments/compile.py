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

import sys
sys.path.append('..')
import pymddoc

if __name__ == '__main__':
    doc = pymddoc.MarkdownDoc.from_file('template.md')
    print(doc)

    print(doc.extract_metadata())

    #print(doc.convert_file('myfile.docx'))
    print(doc.get_jinja_variables())

    print(doc.pandoc_convert_text(to_format='html'))
    print(doc.render_html(vars={'image_base_url': 'https://storage.googleapis.com/public_data_09324832787'}))
