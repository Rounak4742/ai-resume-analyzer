from fastapi.testclient import TestClient
from unittest.mock import patch
from pathlib import Path

from main import app
from schemas import ResumeAnalysis


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "AI Resume Analyzer API is running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_unsupported_file_type():
    response = client.post(
        "/upload",
        files={
            "file": (
                "test.txt",
                b"This is a test file.",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert "Unsupported file type" in data["detail"]


def test_empty_file():
    response = client.post(
        "/upload",
        files={
            "file": (
                "empty.pdf",
                b"",
                "application/pdf"
            )
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Uploaded file is empty."

def test_corrupted_pdf():
    response = client.post(
        "/upload",
        files={
            "file": (
                "corrupted.pdf",
                b"This is not a real PDF file.",
                "application/pdf"
            )
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == (
        "The uploaded PDF file is corrupted or is not a valid PDF document."
    )


def test_corrupted_docx():
    response = client.post(
        "/upload",
        files={
            "file": (
                "corrupted.docx",
                b"This is not a real DOCX file.",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == (
        "The uploaded DOCX file is corrupted or is not a valid DOCX document."
    )

def test_file_too_large():
    large_file = b"x" * (5 * 1024 * 1024 + 1)

    response = client.post(
        "/upload",
        files={
            "file": (
                "large.pdf",
                large_file,
                "application/pdf"
            )
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == (
        "File too large. Maximum file size is 5 MB."
    )

def test_successful_pdf_upload():

    fake_analysis = ResumeAnalysis(
        candidate_name="Test Candidate",
        email="test@example.com",
        phone="1234567890",
        linkedin="",
        github="",
        skills=["Python", "FastAPI"],
        education=[],
        experience=[],
        projects=[],
        certifications=[],
        resume_score=80,
        strengths=["Good technical skills"],
        weaknesses=["Limited experience"],
        suggestions=["Add more projects"],
        ats_keywords=["Python", "FastAPI"],
        job_keywords=["Python", "FastAPI", "Docker"],
    )

    fake_ats = {
        "ats_match_score": 66,
        "matching_keywords": ["Python", "FastAPI"],
        "missing_keywords": ["Docker"]
    }

    valid_pdf = (
        b"%PDF-1.4\n"
        b"1 0 obj\n"
        b"<< /Type /Catalog /Pages 2 0 R >>\n"
        b"endobj\n"
        b"2 0 obj\n"
        b"<< /Type /Pages /Kids [] /Count 0 >>\n"
        b"endobj\n"
        b"trailer\n"
        b"<< /Root 1 0 R >>\n"
        b"%%EOF"
    )

    with patch(
        "main.analyze_resume",
        return_value=fake_analysis
    ), patch(
        "main.calculate_ats_score",
        return_value=fake_ats
    ), patch(
        "main.extract_pdf_text",
        return_value="Test Candidate Python FastAPI resume"
    ):

        response = client.post(
            "/upload",
            data={
                "job_description": (
                    "Looking for a Python FastAPI developer "
                    "with Docker experience."
                )
            },
            files={
                "file": (
                    "test_resume.pdf",
                    valid_pdf,
                    "application/pdf"
                )
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "test_resume.pdf"

    assert data["resume"]["candidate_name"] == "Test Candidate"
    assert data["resume"]["resume_score"] == 80
    assert "Python" in data["resume"]["skills"]

    assert data["ats"]["ats_match_score"] == 66
    assert "Python" in data["ats"]["matching_keywords"]
    assert "Docker" in data["ats"]["missing_keywords"]

def test_successful_docx_upload():

    fake_analysis = ResumeAnalysis(
        candidate_name="Test Candidate",
        email="test@example.com",
        phone="1234567890",
        linkedin="",
        github="",
        skills=["Python", "Django"],
        education=[],
        experience=[],
        projects=[],
        certifications=[],
        resume_score=85,
        strengths=["Strong Python skills"],
        weaknesses=["Limited experience"],
        suggestions=["Add more projects"],
        ats_keywords=["Python", "Django"],
        job_keywords=["Python", "Django", "PostgreSQL"],
    )

    fake_ats = {
        "ats_match_score": 75,
        "matching_keywords": ["Python", "Django"],
        "missing_keywords": ["PostgreSQL"]
    }

    # Minimal valid DOCX ZIP structure
    valid_docx = (
        b"PK\x03\x04"
    )

    with patch(
        "main.analyze_resume",
        return_value=fake_analysis
    ), patch(
        "main.calculate_ats_score",
        return_value=fake_ats
    ), patch(
        "main.extract_docx_text",
        return_value="Test Candidate Python Django resume"
    ):

        response = client.post(
            "/upload",
            data={
                "job_description": (
                    "Looking for a Python Django developer "
                    "with PostgreSQL experience."
                )
            },
            files={
                "file": (
                    "test_resume.docx",
                    valid_docx,
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "test_resume.docx"

    assert data["resume"]["candidate_name"] == "Test Candidate"
    assert data["resume"]["resume_score"] == 85
    assert "Python" in data["resume"]["skills"]

    assert data["ats"]["ats_match_score"] == 75
    assert "Python" in data["ats"]["matching_keywords"]
    assert "PostgreSQL" in data["ats"]["missing_keywords"]

def test_successful_pdf_upload_without_job_description():

    fake_analysis = ResumeAnalysis(
        candidate_name="Test Candidate",
        email="test@example.com",
        phone="1234567890",
        linkedin="",
        github="",
        skills=["Python", "FastAPI"],
        education=[],
        experience=[],
        projects=[],
        certifications=[],
        resume_score=80,
        strengths=["Good technical skills"],
        weaknesses=["Limited experience"],
        suggestions=["Add more projects"],
        ats_keywords=["Python", "FastAPI"],
    )

    valid_pdf = (
        b"%PDF-1.4\n"
        b"1 0 obj\n"
        b"<< /Type /Catalog /Pages 2 0 R >>\n"
        b"endobj\n"
        b"2 0 obj\n"
        b"<< /Type /Pages /Kids [] /Count 0 >>\n"
        b"endobj\n"
        b"trailer\n"
        b"<< /Root 1 0 R >>\n"
        b"%%EOF"
    )

    with patch(
        "main.analyze_resume",
        return_value=fake_analysis
    ), patch(
        "main.extract_pdf_text",
        return_value="Test Candidate Python FastAPI resume"
    ):

        response = client.post(
            "/upload",
            files={
                "file": (
                    "resume.pdf",
                    valid_pdf,
                    "application/pdf"
                )
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "resume.pdf"

    assert data["resume"]["candidate_name"] == "Test Candidate"
    assert data["resume"]["resume_score"] == 80
    assert "Python" in data["resume"]["skills"]

    assert data["ats"]["ats_match_score"] == 0
    assert data["ats"]["matching_keywords"] == []
    assert data["ats"]["missing_keywords"] == []

def test_internal_processing_error():

    valid_pdf = (
        b"%PDF-1.4\n"
        b"1 0 obj\n"
        b"<< /Type /Catalog /Pages 2 0 R >>\n"
        b"endobj\n"
        b"2 0 obj\n"
        b"<< /Type /Pages /Kids [] /Count 0 >>\n"
        b"endobj\n"
        b"trailer\n"
        b"<< /Root 1 0 R >>\n"
        b"%%EOF"
    )

    with patch(
        "main.extract_pdf_text",
        return_value="Test resume text"
    ), patch(
        "main.analyze_resume",
        side_effect=Exception("Groq API failed")
    ):

        response = client.post(
            "/upload",
            files={
                "file": (
                    "resume.pdf",
                    valid_pdf,
                    "application/pdf"
                )
            }
        )

    assert response.status_code == 500

    data = response.json()

    assert data["detail"] == (
        "An internal error occurred while analyzing the document."
    )

def test_uploaded_file_is_deleted():

    valid_pdf = (
        b"%PDF-1.4\n"
        b"1 0 obj\n"
        b"<< /Type /Catalog /Pages 2 0 R >>\n"
        b"endobj\n"
        b"2 0 obj\n"
        b"<< /Type /Pages /Kids [] /Count 0 >>\n"
        b"endobj\n"
        b"trailer\n"
        b"<< /Root 1 0 R >>\n"
        b"%%EOF"
    )

    with patch(
        "main.extract_pdf_text",
        return_value="Test resume text"
    ), patch(
        "main.analyze_resume",
        return_value=ResumeAnalysis(
            candidate_name="Test Candidate",
            email="test@example.com",
            phone="1234567890",
            linkedin="",
            github="",
            skills=["Python"],
            education=[],
            experience=[],
            projects=[],
            certifications=[],
            resume_score=80,
            strengths=[],
            weaknesses=[],
            suggestions=[],
            ats_keywords=["Python"],
        )
    ):

        response = client.post(
            "/upload",
            files={
                "file": (
                    "cleanup_test.pdf",
                    valid_pdf,
                    "application/pdf"
                )
            }
        )

    assert response.status_code == 200

    # Check that no temporary UUID PDF remains
    remaining_temp_files = [
        file for file in Path("uploads").glob("*.pdf")
        if len(file.stem) == 36 and file.stem.count("-") == 4
    ]

    assert remaining_temp_files == []