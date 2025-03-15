


# Command-line Interface

The command-line interface is sufficient for cases where you do not need to include custom functions in your code. Docs for the ipynb conversion commands can be seen in the section on that topic, and here I will cover `render` and `metadata` commands.

Like most command line interfaces, you can use the `--help` flag to get a list of available commands.

``` bash
python -m pymddoc --help
```

output:
``` plaintext
Usage: python -m pymddoc [OPTIONS] COMMAND [ARGS]...

Options:
--help  Show this message and exit.

Commands:
metadata        Extract metadata from a markdown file as json.
render          Render and compile a markdown file.
ipynb2md        Convert a Jupyter notebook (json file) to a markdown file.
ipynb2md-multi  Convert multiple Jupyter notebooks (json files) to markdown files.
```


## Extract YAML header metadata from markdown files: `metadata`

This command will output formatted JSON that includes the yaml header information from the markdown file. This is useful for debugging and taking a quick look at markdown files.

``` bash
python -m pymddoc metadata --help
```

## Render markdown files: `render`

This command will render the markdown file using jinja and compile the rendered file to the desired format (html, pdf, or docx). This allows you to use all of the built-in functions and features of `pymddoc` without writing any code.

``` bash
python -m pymddoc render --help
```

output:
``` plaintext
Usage: python -m pymddoc render [OPTIONS] MD_FILE OUT_FILE

  Render and compile a markdown file.

Options:
  --out_format [html|pdf|docx]
  --strict_render BOOLEAN
  --help                        Show this message and exit.
```

 