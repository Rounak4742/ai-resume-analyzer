from ai_analyzer import extract_job_keywords


job_description = """
We are looking for a Junior Backend Developer.

Requirements:
- Python
- FastAPI
- REST APIs
- SQL
- PostgreSQL
- Git
- Docker
- Basic knowledge of AWS
- Good communication skills
"""


keywords = extract_job_keywords(job_description)

print("Extracted keywords:")

for keyword in keywords:
    print("-", keyword)