from pdf_extractor import extract_pdf_text
from text_processor import clean_text
from ai_analyzer import analyze_resume

resume_text = extract_pdf_text("Rounak_Kumar_Resume_SDE.pdf")
cleaned_text = clean_text(resume_text)

job_description = """
We are looking for a Software Development Engineer (SDE) intern.

Requirements:
- Strong programming skills in Python, Java, or C++
- Knowledge of Data Structures and Algorithms
- Understanding of Object-Oriented Programming
- Basic knowledge of SQL and databases
- Experience with Git and GitHub
- Understanding of REST APIs and backend development
- Problem-solving and debugging skills
- Good communication and teamwork
- Knowledge of FastAPI or Flask is a plus
- Basic understanding of cloud platforms is a plus
"""

try:
    result = analyze_resume(cleaned_text, job_description)

    print("\n========== AI ANALYSIS ==========\n")
    print(result)

except Exception as e:
    print("\n========== ERROR ==========\n")
    print(repr(e))