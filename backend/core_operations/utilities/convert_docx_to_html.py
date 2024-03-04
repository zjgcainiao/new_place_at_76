from docx import Document


def convert_docx_to_html(path):
    doc = Document(path)
    html_content = ''

    for para in doc.paragraphs:
        # Simple conversion: wrap paragraphs in <p> tags
        html_content += f'<p>{para.text}</p>'

    return html_content
