from pdfminer.high_level import extract_text
from pathlib import Path

def pdf_to_text(file):
    return extract_text(file)


if __name__ == "__main__":
    # Example usage
    pdf_file = Path("uploads/animal_kingdom_ch4.pdf")
    text = pdf_to_text(pdf_file)
    with open("animal_kingdom_ch4.txt", "w") as text_file:
        text_file.write(text)
    # print(text)