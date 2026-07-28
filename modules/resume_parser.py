import pymupdf as fitz

def parse_resume(file_path):
    """
    Extract text from a PDF resume.
    """

    document = fitz.open(file_path)

    text = ""

    for page in document:

        text += page.get_text()

    document.close()

    return text
if __name__ == "__main__":

    text = parse_resume("resumes/Student_1.pdf")

    print(text)