


# Inserting Table and Figure Data

Translating results of analyses to tables and figures in documents often involves multiple steps, and this package provides some functionality to streamline that process. This functionality is provided through functions that the Jinja templating engine has access to.

+ Translate table data in CSV or Excel format to Markdown for inclusion in the document.
+ Convert Vector graphic files to PNG format for inclusion in the document.




---

``` python linenums="1"
import sys
sys.path.append('..')
import pymddoc

import tempfile
```


---




## Useful Constants
First, it is worth mentioning some defined constants that can be helpful for composing documents. Use them as you would any other Jinja variable.

+ **OUTPUT_FORMAT**: the output format type of the document.
+ **HOME_DIR**: the home directory of the computer where you're rendering the document.




---

``` python linenums="1"
example_markdown = '''
Document format: {{OUTPUT_FORMAT}}

Home directory: {{HOME_DIR}}
'''.strip()

doc = pymddoc.MarkdownDoc.from_str(example_markdown)
print(doc.render_html())
```



stdout:
 

    <p>Document format: html</p>
    <p>Home directory: /home/devin</p>
    
    

 



---




While Pandoc supports a number of output formats, it is necessarily inconsistent in how it renders various elements of the document. Using the `OUTPUT_FORMAT` constant, you can conditionally render elements based on the output format. 




---

``` python linenums="1"
example_markdown = '''
{% if OUTPUT_FORMAT == 'html' %}
This is an HTML document.
{% else %}
This is not an HTML document.
{% endif %}
'''.strip()

doc = pymddoc.MarkdownDoc.from_str(example_markdown)
print(doc.render_html())
```



stdout:
 

    <p>This is an HTML document.</p>
    
    

 



---




## Insert Tables

There are two methods for inserting tables into your documents: `csv_to_markdown` and `excel_to_markdown`. Both methods read a file from disk and insert it into the document as markdown.




---

``` python linenums="1"
print(pymddoc.excel_to_markdown.__doc__)
```



stdout:
 

    Read an excel file from disk and insert it into the document as markdown.
        Args:
            fname: str: The file name to read.
            num_rows: int | None: The number of rows to read.
            read_kwargs: dict[str,typing.Any] | None: The keyword arguments to pass to the read
                function.
            to_markdown_kwargs: dict[str,typing.Any] | None: The keyword arguments to pass to the
        
    

 



---





---

``` python linenums="1"
print(pymddoc.csv_to_markdown.__doc__)
```



stdout:
 

    Read a csv file from disk and insert it into the document as markdown.
        Args:
            fname: str: The file name to read.
            num_rows: int | None: The number of rows to read.
            read_kwargs: dict[str,typing.Any] | None: The keyword arguments to pass to the read
                function.
            to_markdown_kwargs: dict[str,typing.Any] | None: The keyword arguments to pass to the
        
    

 



---




Call them from within the markdown document.




---

``` python linenums="1"
example_markdown = '''
{{csv_to_markdown('../tests/test_data/testtable.csv', num_rows=2)}}
'''.strip()

doc = pymddoc.MarkdownDoc.from_str(example_markdown)
print(doc.render_html())
```



stdout:
 

    <table>
    <thead>
    <tr class="header">
    <th style="text-align: left;">name</th>
    <th style="text-align: right;">number</th>
    </tr>
    </thead>
    <tbody>
    <tr class="odd">
    <td style="text-align: left;">one</td>
    <td style="text-align: right;">1</td>
    </tr>
    <tr class="even">
    <td style="text-align: left;">two</td>
    <td style="text-align: right;">2</td>
    </tr>
    </tbody>
    </table>
    
    

 



---




## Embed Vector Graphics
While it is possible to embed vector graphic types such as SVG and PDF into documents using additional software, the following built-in methods will convert these file types to PNG and embed them directly into the document when it is rendered. This is ideal for cases where you want to embed outputs from analyses for publication, and it is all controlled within the markdown document - even the DPI of the output image.




---

``` python linenums="1"
print(pymddoc.svg_to_png.__doc__)
```



stdout:
 

    Convert an svg file to a png file stored in /tmp for pandoc compilation.
        Args:
            url: str: The url of the svg file to convert.
            dpi: int: The dpi of the output image.
            kwargs: dict: Additional keyword arguments to pass to cairosvg.svg2png().
        
    

 



---





---

``` python linenums="1"
print(pymddoc.pdf_to_png.__doc__)
```



stdout:
 

    Convert a pdf file to a png file stored in /tmp for pandoc compilation.
        Args:
            filename: str: The filename of the pdf file to convert.
            pageno: int: The page number of the svg file to convert.
            dpi: int: The dpi of the output image.
            kwargs: dict: Additional keyword arguments to pass to page.get_pixmap().
        
    

 



---




Call them from within the markdown document.




---

``` python linenums="1"
example_markdown = '''
{# embed the pdf as a png. This one is on the web. #}
![]({{svg_to_png("https://storage.googleapis.com/public_data_09324832787/static_factory_methods.svg", dpi=150)}})

{# embed the pdf as a png #}
![]({{pdf_to_png("../tests/test_data/drawing.pdf", dpi=150)}})

{# embed the pdf directly. This also works. #}
![](../tests/test_data/drawing.pdf)
'''.strip()

doc = pymddoc.MarkdownDoc.from_str(example_markdown)

with tempfile.TemporaryDirectory() as tmpdirname:
    doc.render_to_pdf(f'{tmpdirname}/output.pdf')
```


---


 