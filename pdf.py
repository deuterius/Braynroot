from pdfminer.high_level import extract_text


def pdf_to_text(file):
    return extract_text(file)
