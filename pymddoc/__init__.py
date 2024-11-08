from .snippet import SnippetCtx, SnippetFormatter, SnippetTemplateType, SnippetInfo, templates

from .depricated import Document, DocMaker

from .markdown_doc import MarkdownDoc
from .metadata import Metadata

from .template_methods import TEMPLATE_METHODS, csv_to_md, excel_to_md

import inspect
gcf = inspect.currentframe
