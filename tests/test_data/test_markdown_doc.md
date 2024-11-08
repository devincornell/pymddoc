---
title: "Hello World"
bibliography: ["data/references.bib"]
---

Note about the headers: the bibliography is only for auto-complete. You must compile using citeproc or some other engine.


{# this is a comment with jinja! It will not be shown to pandoc. comment_test_flag #}

# Jinja Tests

This should be replaced: {{ test_variable }}


{# comment_should_not_appear #}

## Citations

Pro tip: see the [pandoc citer](https://marketplace.visualstudio.com/items?itemName=notZaki.pandocciter) VSCode plugin for citation auto-complete.

You can insert citations like this  [@Welch2006; @Pedersen2008]. Cite direct references to authors using the following syntax: Pedersen et al. [-@Pedersen2008] noted that eigenvectors are the best way to determine the principal components.


# Pandoc Testing
::: { #this_id_should_appear .this_class_should_appear}
This is the last warning!
:::

```python
def main():
    print(f'Why the heck would you go there?')
```

{# embed the pdf as a png #}

![]({{svg_to_png("https://storage.googleapis.com/public_data_09324832787/static_factory_methods.svg")}}){ #hello .myclass size="80%" }

![]({{svg_to_png("test_data/drawing.svg")}}){ #hello .myclass size="80%" }


{# embed the pdf as a png #}

![]({{pdf_to_png("test_data/drawing.pdf")}}){ .myclass size="80%" }

{# embed the pdf directly #}
![](test_data/drawing.pdf){ .myclass size="80%" }


::: {.mytestclass}
{{ csv_to_markdown('test_data/testtable.csv') }}
:::

{# this is a comment! #}
