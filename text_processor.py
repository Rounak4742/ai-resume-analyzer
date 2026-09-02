import re


def clean_text(text):
    # Replace multiple spaces/tabs with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove spaces at the beginning/end of lines
    lines = [line.strip() for line in text.splitlines()]

    # Remove empty lines at the beginning/end
    text = "\n".join(lines).strip()

    return text