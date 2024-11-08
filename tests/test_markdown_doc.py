import sys
sys.path.append('..')

import pymddoc

def test_compile_basics():
    doc = pymddoc.MarkdownDoc.from_file('template.md')
    print(doc)

    print(doc.extract_metadata())

    #print(doc.convert_file('myfile.docx'))
    print(doc.get_jinja_variables())

    #print(doc.pandoc_convert_text(to_format='html'))
    #print(doc.render_html(vars={'image_base_url': 'https://storage.googleapis.com/public_data_09324832787'}))

    #with tempfile.TemporaryDirectory() as tmpdir:
    #    print(pymddoc.svg_to_png(tmpdir, "https://storage.googleapis.com/public_data_09324832787/static_factory_methods.svg"))
        #pymddoc.svg_to_png("https://storage.googleapis.com/public_data_09324832787/static_factory_methods.svg")

    #with pymddoc.SnippetCtx.new(gcf()):
    #    print('hello world')

    #print(doc.render_to_pdf('output.pdf', vars={'image_base_url': 'https://storage.googleapis.com/public_data_09324832787'}))
    #print(pymddoc.pdf_to_png('/tmp', 'data/hist_rt_comparison.pdf'))

    doc.render_html(
        vars={'image_base_url': 'https://storage.googleapis.com/public_data_09324832787'},
    )

    doc.render_to_pdf(
        output='outputs/output.pdf', 
        vars={'image_base_url': 'https://storage.googleapis.com/public_data_09324832787'},
    )

    doc.render_to_docx(
        output='outputs/output.docx', 
        vars={'image_base_url': 'https://storage.googleapis.com/public_data_09324832787'},
    )




if __name__ == '__main__':
    test_compile_basics()


