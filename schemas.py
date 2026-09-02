from pydantic import BaseModel, Field
from typing import List


class Education(BaseModel):
    degree: str
    field: str
    institution: str
    graduation_year: str


class Experience(BaseModel):
    job_title: str
    company: str
    duration: str
    description: str


class Project(BaseModel):
    name: str
    description: str
    technologies: List[str]


class ResumeAnalysis(BaseModel):
    candidate_name: str
    email: str
    phone: str
    linkedin: str
    github: str

    skills: List[str]

    education: List[Education]
    experience: List[Experience]
    projects: List[Project]
    certifications: List[str]

    resume_score: int

    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]

    ats_keywords: List[str]

    job_keywords: List[str] = Field(
        default_factory=list,
        description=(
            "Important ATS-relevant keywords extracted from the job description "
            "(skills, tools, frameworks, certifications). Empty list if no job "
            "description was provided."
        ),
    )


class JobKeywords(BaseModel):
    keywords: List[str]


class ATSResult(BaseModel):
    ats_match_score: int
    matching_keywords: List[str]
    missing_keywords: List[str]


class Scores(BaseModel):
    resume_score: int
    ats_match_score: int


class Feedback(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]


class AnalysisResponse(BaseModel):
    filename: str
    resume: ResumeAnalysis
    ats: ATSResult
    scores: Scores
    feedback: Feedback