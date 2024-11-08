import sys
sys.path.append('..')

import pymddoc

def test_compile_basics():
    doc = pymddoc.MarkdownDoc.from_file('test_data/test_markdown_doc.md')
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

    html_str = doc.render_html(
        vars={'test_variable': 'replaced_variable_value'},
    )
    assert('test_variable' not in html_str) # variable replacement
    assert('replaced_variable_value' in html_str) # check if variable was replaced properly
    assert('comment_should_not_appear' not in html_str) # comment should not appear
    assert('class="this_class_should_appear"' in html_str) # add class to div
    assert('id="this_id_should_appear"' in html_str) # add id to div
    assert('static_factory_methods.svg.png' in html_str) # svg to png replacement
    assert('drawing.pdf.png' in html_str) # pdf to png replacement
    assert('test_data/drawing.pdf' in html_str) # raw pdf inclusion
    assert('two' in html_str) # table insertion
    assert('three' in html_str) # table insertion

    doc.render_to_pdf(
        output='test_outputs/test_output.pdf', 
        vars={'test_variable': 'replaced_variable_value'},
    )

    doc.render_to_docx(
        output='test_outputs/test_output.docx', 
        vars={'test_variable': 'replaced_variable_value'},
    )




if __name__ == '__main__':
    test_compile_basics()


