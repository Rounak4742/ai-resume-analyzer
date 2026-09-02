import pdfplumber
from pdfminer.pdfparser import PDFSyntaxError


def extract_pdf_text(pdf_path):
    try:
        text = ""

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    except Exception as e:
        error_message = str(e)

        if (
            "No /Root object" in error_message
            or "Is this really a PDF" in error_message
            or "PDF" in type(e).__name__
        ):
            raise ValueError(
                "The uploaded PDF file is corrupted or is not a valid PDF document."
            )

        raise ValueError(
            f"Could not read the PDF file: {error_message}"
        )