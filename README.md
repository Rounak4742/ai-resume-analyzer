# AI Powered Resume Analyzer

An AI-powered web application that analyzes PDF and DOCX resumes, extracts structured candidate information, evaluates resume quality, and calculates an ATS match score against a job description.

## Features

* Upload PDF and DOCX resumes
* Maximum upload size of 5 MB
* Automatic resume text extraction
* Text cleaning and preprocessing
* AI-powered resume analysis using Groq
* Structured extraction of:

  * Candidate information
  * Skills
  * Education
  * Experience
  * Projects
  * Certifications
* Extracts all education records, including B.Tech, Class XII, Class X, and other formal education when present
* Resume quality score
* Strengths and weaknesses
* Practical improvement suggestions
* Optional job description analysis
* ATS keyword extraction
* ATS match score
* Matching and missing keyword detection
* Temporary uploaded files are automatically deleted after processing
* FastAPI REST API
* React frontend
* Automated backend tests with pytest

## Tech Stack

### Backend

* Python
* FastAPI
* Groq API
* Pydantic
* pdfplumber
* python-docx
* python-multipart
* python-dotenv
* pytest
* httpx

### Frontend

* React
* Vite
* JavaScript
* CSS

## Architecture

```text
User
  |
  v
React Frontend
  |
  | PDF/DOCX + Job Description
  v
FastAPI Backend
  |
  +--> File Validation
  |
  +--> PDF/DOCX Text Extraction
  |
  +--> Text Cleaning
  |
  +--> Groq AI Resume Analysis
  |
  +--> ATS Keyword Matching
  |
  v
Structured API Response
  |
  v
React Results Dashboard
```

## Project Structure

```text
ai-resume-analyzer-two/
│
├── ai_analyzer.py
├── ats_analyzer.py
├── docx_extractor.py
├── pdf_extractor.py
├── text_processor.py
├── schemas.py
├── main.py
│
├── test_ai.py
├── test_api.py
├── test_ats.py
├── test_docx.py
├── test_full_analysis.py
├── test_jd.py
├── test_pdf.py
├── test_processor.py
├── test_schema.py
├── test_groq.py
│
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
└── frontend/
    ├── package.json
    ├── src/
    │   ├── App.jsx
    │   ├── App.css
    │   └── components/
    │       ├── UploadForm.jsx
    │       ├── ResultsDashboard.jsx
    │       └── ScoreGauge.jsx
    └── ...
```

## Requirements

Before running the project, make sure you have:

* Python 3.14 or a compatible Python version
* Node.js and npm
* A Groq API key

## Backend Setup

Clone the repository:

```bash
git clone https://github.com/Rounak4742/ai-resume-analyzer.git
cd ai-resume-analyzer
```

Create a virtual environment:

### Windows

```bat
python -m venv venv
```

Activate it:

```bat
venv\Scripts\activate
```

Install dependencies:

```bat
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Do not commit the `.env` file or expose your API key publicly.

## Run the Backend

From the project root:

```bat
venv\Scripts\python.exe -m uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

## Frontend Setup

Open another terminal and navigate to the frontend:

```bat
cd frontend
```

Install dependencies:

```bat
npm install
```

Start the development server:

```bat
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

### API Configuration

The frontend supports configuring the backend URL through the Vite environment variable:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

If the variable is not provided, the frontend defaults to:

```text
http://127.0.0.1:8000
```

## Using the Application

1. Start the FastAPI backend.
2. Start the React frontend.
3. Open the frontend in your browser.
4. Upload a PDF or DOCX resume.
5. Optionally enter a job description.
6. Click **Analyze Resume**.
7. Review the resume score, ATS score, extracted information, keywords, strengths, weaknesses, and suggestions.

When a job description is provided, the application performs ATS matching against the extracted job-related keywords.

## API Endpoints

### `GET /`

Returns a basic API status message.

### `GET /health`

Returns the health status of the backend.

### `POST /upload`

Accepts:

* Resume file (`.pdf` or `.docx`)
* Optional job description

Returns structured resume analysis and ATS results.

## File Validation

The backend validates uploaded files before processing.

Current restrictions:

* Supported formats: PDF and DOCX
* Maximum file size: 5 MB
* Empty files are rejected
* Corrupted PDF and DOCX files are handled
* Temporary uploaded files are deleted after processing

## Testing

Run the complete backend test suite:

```bat
venv\Scripts\python.exe -m pytest -v
```

The project currently contains automated tests covering:

* API home endpoint
* Health endpoint
* Unsupported file types
* Empty files
* Corrupted PDFs
* Corrupted DOCX files
* File size validation
* Successful PDF uploads
* Successful DOCX uploads
* Uploads without job descriptions
* Internal processing errors
* Temporary file cleanup
* PDF extraction
* DOCX extraction

## Production Frontend Build

To verify that the React application can be built for production:

```bat
cd frontend
npm run build
```

The production files are generated in:

```text
frontend/dist/
```

## Security Notes

* API keys are stored in environment variables.
* `.env` is excluded from Git.
* Uploaded resumes are stored temporarily during processing and deleted afterward.
* PDF files are excluded from Git to prevent accidental commits of user resumes.

## Current Scope

The application currently supports:

* PDF resumes
* DOCX resumes
* Text-based document extraction
* AI-powered resume analysis
* ATS matching against job descriptions

Scanned/image-only PDF OCR processing is intentionally outside the current scope.

## Future Improvements

Potential future improvements include:

* OCR support for scanned resumes
* User authentication
* Resume history and saved analyses
* Database-backed analysis storage
* Deployment configuration
* Automated CI/CD
* More advanced ATS scoring
* Better resume section detection
* Exporting analysis results as PDF

## Author

**Rounak Kumar**

AI Powered Resume Analyzer built as a full-stack project using FastAPI, React, and Groq AI.
