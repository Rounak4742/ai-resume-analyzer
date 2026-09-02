from docx import Document
from docx.opc.exceptions import PackageNotFoundError


def extract_docx_text(docx_path):
    try:
        document = Document(docx_path)

        text = ""

        for paragraph in document.paragraphs:
            if paragraph.text:
                text += paragraph.text + "\n"

        return text

    except PackageNotFoundError:
        raise ValueError(
            "The uploaded DOCX file is corrupted or is not a valid DOCX document."
        )

    except Exception as e:
        raise ValueError(
            f"Could not read the DOCX file: {str(e)}"
        )