from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uuid

from pdf_extractor import extract_pdf_text
from docx_extractor import extract_docx_text
from text_processor import clean_text
from ai_analyzer import (
    analyze_resume,
    AIAnalysisError
)
from ats_analyzer import calculate_ats_score
from schemas import AnalysisResponse, ATSResult, Scores, Feedback


app = FastAPI(
    title="AI Powered Resume Analyzer",
    description="API for analyzing PDF and DOCX resumes using Groq AI and ATS matching.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Configuration
# -----------------------------

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


# -----------------------------
# Home endpoint
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "AI Resume Analyzer API is running"
    }


# -----------------------------
# Health check endpoint
# -----------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# -----------------------------
# Resume upload and analysis
# -----------------------------

@app.post("/upload", response_model=AnalysisResponse)
async def upload_document(
    file: UploadFile = File(...),
    job_description: str = Form("")
):

    # -----------------------------
    # 1. Validate filename
    # -----------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )

    # Get file extension
    extension = Path(file.filename).suffix.lower()

    # -----------------------------
    # 2. Validate file type
    # -----------------------------

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Only PDF and DOCX files are allowed."
        )

    # -----------------------------
    # 3. Read uploaded file
    # -----------------------------

    file_content = await file.read()

    # -----------------------------
    # 4. Validate file size
    # -----------------------------

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum file size is 5 MB."
        )

    if len(file_content) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # -----------------------------
    # 5. Generate safe filename
    # -----------------------------

    safe_filename = f"{uuid.uuid4()}{extension}"

    file_path = UPLOAD_DIR / safe_filename

    try:

        # -----------------------------
        # 6. Save temporary file
        # -----------------------------

        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

        # -----------------------------
        # 7. Extract text
        # -----------------------------

        if extension == ".pdf":

            text = extract_pdf_text(
                str(file_path)
            )

        elif extension == ".docx":

            text = extract_docx_text(
                str(file_path)
            )

        # -----------------------------
        # 8. Validate extracted text
        # -----------------------------

        if not text or not text.strip():

            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the document."
            )

        # -----------------------------
        # 9. Clean extracted text
        # -----------------------------

        cleaned_text = clean_text(text)

        if not cleaned_text.strip():

            raise HTTPException(
                status_code=400,
                detail="Document contains no usable text."
            )

        # -----------------------------
        # 10. Analyze resume with Groq AI
        # -----------------------------

        analysis = analyze_resume(
            cleaned_text,
            job_description
        )

        # -----------------------------
        # 11. Default ATS result
        # -----------------------------

        ats_result = {
            "ats_match_score": 0,
            "matching_keywords": [],
            "missing_keywords": []
        }

        # -----------------------------
        # 12. Perform ATS analysis
        #     only when JD is provided
        #
        #     job_keywords now comes from the SAME Groq call as the
        #     resume analysis (see analysis.job_keywords) instead of a
        #     separate extract_job_keywords() call — this reduces Groq
        #     API usage per request.
        # -----------------------------

        if job_description.strip():

            # Calculate deterministic ATS score
            ats_result = calculate_ats_score(
                cleaned_text,
                job_description,
                analysis.job_keywords
            )

        # -----------------------------
        # 13. Build final response
        # -----------------------------

        return AnalysisResponse(
            filename=file.filename,

            resume=analysis,

            ats=ATSResult(
                ats_match_score=ats_result["ats_match_score"],
                matching_keywords=ats_result["matching_keywords"],
                missing_keywords=ats_result["missing_keywords"]
            ),

            scores=Scores(
                resume_score=analysis.resume_score,
                ats_match_score=ats_result["ats_match_score"]
            ),

            feedback=Feedback(
                strengths=analysis.strengths,
                weaknesses=analysis.weaknesses,
                suggestions=analysis.suggestions
            )
        )

    except HTTPException:
        raise

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except AIAnalysisError as e:
        print("GROQ ERROR:", repr(e))
        raise HTTPException(
            status_code=503,
            detail="AI analysis service is currently unavailable. Please try again later."
        )

    except Exception as e:
        print("INTERNAL ERROR:", repr(e))
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while analyzing the document."
        )

    finally:

        # -----------------------------
        # 14. Delete temporary file
        # -----------------------------

        if file_path.exists():

            try:
                file_path.unlink()
                print(f"Temporary file deleted: {file_path}")

            except Exception as e:
                print(f"Could not delete temporary file: {e}")