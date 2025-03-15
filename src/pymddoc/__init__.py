from .snippet import SnippetCtx, SnippetFormatter, SnippetTemplateType, SnippetInfo, templates

from .depricated import Document, DocMaker

from .notebooks import (
    convert_ipynb2md, 
)
from .templates import (
    templates, 
    ipynb2md_default_template
)

from .markdown_doc import MarkdownDoc
from .metadata import Metadata
from .compile import PandocArgs

from .builtin_methods import (
    get_builtin_methods, 
    builtin_methods_str,
    csv_to_markdown, 
    excel_to_markdown, 
    svg_to_png, 
    pdf_to_png
)


import inspect
gcf = inspect.currentframe
