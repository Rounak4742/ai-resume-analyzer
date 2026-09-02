import re


def normalize_text(text):
    text = text.lower()

    # Replace common separators with spaces
    text = re.sub(r"[/|,;:()\[\]{}]", " ", text)

    # Keep +, # and . because of skills like C++, C#, .NET
    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def keyword_exists(keyword, resume_text):
    keyword = normalize_text(keyword)
    resume_text = normalize_text(resume_text)

    # Escape keyword so special characters are handled safely
    pattern = r"(?<![a-z0-9])" + re.escape(keyword) + r"(?![a-z0-9])"

    return re.search(pattern, resume_text) is not None


def calculate_ats_score(resume_text, job_description, keywords):

    matching_keywords = []
    missing_keywords = []

    for keyword in keywords:

        if keyword_exists(keyword, resume_text):
            matching_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    if not keywords:
        score = 0
    else:
        score = round(
            (len(matching_keywords) / len(keywords)) * 100
        )

    return {
        "ats_match_score": score,
        "matching_keywords": matching_keywords,
        "missing_keywords": missing_keywords
    }