from schemas import ResumeAnalysis


analysis = ResumeAnalysis(
    candidate_name="Rounak Kumar",
    email="test@example.com",
    phone="1234567890",
    linkedin="https://linkedin.com",
    github="https://github.com",

    skills=["Python", "Java", "HTML", "CSS"],

    education=[
        {
            "degree": "B.Tech",
            "field": "Computer Science",
            "institution": "Example University",
            "graduation_year": "2027"
        }
    ],

    experience=[],

    projects=[
        {
            "name": "AI Resume Analyzer",
            "description": "AI-powered resume analysis system",
            "technologies": ["Python", "FastAPI"]
        }
    ],

    certifications=["Python Certification"],

    resume_score=78,

    strengths=[
        "Good technical skills"
    ],

    weaknesses=[
        "Limited work experience"
    ],

    suggestions=[
        "Add measurable achievements"
    ],

    ats_keywords=[
        "Python",
        "FastAPI",
        "Machine Learning"
    ],

    job_keywords=[
        "Python",
        "FastAPI",
        "Docker"
    ]
)


print(analysis.model_dump_json(indent=2))