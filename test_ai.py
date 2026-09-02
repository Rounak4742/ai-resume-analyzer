from ai_analyzer import analyze_resume


sample_resume = """
Rounak Kumar

EDUCATION
B.Tech in Computer Science and Engineering
Jharkhand University of Technology
Expected Graduation: 2027

SKILLS
Python, Java, HTML, CSS, FastAPI, Computer Networking

PROJECTS
AI Powered Resume Analyzer
Built a web-based application using Python and FastAPI.

CERTIFICATIONS
Tata Group Data Analytics Job Simulation
Deloitte Australia Technology Job Simulation
"""


sample_job_description = """
We are looking for a Junior Backend Developer.

Requirements:
- Python
- FastAPI
- REST APIs
- SQL
- PostgreSQL
- Git
- Docker
- Basic knowledge of cloud platforms
"""


result = analyze_resume(
    sample_resume,
    sample_job_description
)

print(result.model_dump_json(indent=2))