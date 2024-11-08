from .snippet import SnippetCtx, SnippetFormatter, SnippetTemplateType, SnippetInfo, templates

from .depricated import Document, DocMaker

from .markdown_doc import MarkdownDoc
from .metadata import Metadata

from .template_methods import get_builtin_methods, csv_to_md, excel_to_md, svg_to_png, pdf_to_png

import inspect
gcf = inspect.currentframe
