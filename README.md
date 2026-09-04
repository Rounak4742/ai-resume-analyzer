# AI Powered Resume Analyzer

An AI-powered full-stack web application that analyzes **PDF and DOCX resumes**, extracts structured candidate information, evaluates resume quality, and calculates an **ATS match score** against a job description.

The application combines **FastAPI, React, Groq AI, deterministic keyword matching, and automated testing** to provide actionable resume feedback through a web interface.

## 🚀 Live Demo

**Try the application:**
https://ai-resume-analyzer-frontend-bdme.onrender.com

> The live application may take a short time to respond if the deployment has been idle.

## ✨ Features

* Upload PDF and DOCX resumes
* Maximum file size of 5 MB
* Automatic PDF and DOCX text extraction
* Text cleaning and preprocessing
* AI-powered resume analysis using Groq
* Structured extraction of:

  * Candidate information
  * Skills
  * Education
  * Experience
  * Projects
  * Certifications
* Detects multiple education records such as B.Tech, Class XII, Class X, and other formal education
* Resume quality scoring
* Strength and weakness analysis
* Practical improvement suggestions
* Optional job description analysis
* Automatic job-related keyword extraction
* ATS keyword matching
* ATS match score
* Detection of matching and missing keywords
* Temporary uploaded files are deleted after processing
* Input validation for unsupported, empty, corrupted, and oversized files
* REST API built with FastAPI
* React-based frontend
* Automated backend testing with pytest

## 📸 Screenshots

Screenshots of the application will be added here.

<!--
Add screenshots after creating them:

![Resume Upload](docs/screenshots/upload.png)

![Analysis Results](docs/screenshots/results.png)
-->

## 🏗️ Architecture

```text
                         User
                           |
                           v
                  React + Vite Frontend
                           |
                           | PDF/DOCX
                           | + Job Description
                           v
                    FastAPI Backend
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
       File Validation  Document      Text Cleaning
                         Extraction
                       PDF / DOCX
                           |
                           v
                    Groq AI Analysis
                           |
                           v
                  Structured Pydantic
                       Response
                           |
                           v
                  ATS Keyword Matching
                           |
                           v
                  JSON API Response
                           |
                           v
                  React Results UI
```

## 🧠 How It Works

### 1. Resume Upload

The user uploads a PDF or DOCX resume through the React frontend.

The application validates:

* File extension
* File size
* Empty files
* Supported document formats

The current maximum file size is **5 MB**.

### 2. Text Extraction

The backend extracts text using:

* `pdfplumber` for PDF files
* `python-docx` for DOCX files

The extracted text is then cleaned and normalized before analysis.

### 3. AI Resume Analysis

The cleaned resume text is sent to the Groq API.

The AI analyzes the resume and produces structured information including:

* Candidate details
* Skills
* Education
* Experience
* Projects
* Certifications
* Resume score
* Strengths
* Weaknesses
* Improvement suggestions
* Relevant job keywords

The response is validated using Pydantic schemas.

### 4. ATS Analysis

When a job description is provided, the application extracts relevant job keywords and compares them with the analyzed resume.

The result includes:

* ATS match score
* Matching keywords
* Missing keywords

This provides a deterministic keyword-based ATS comparison rather than relying entirely on an AI-generated score.

### 5. Temporary File Cleanup

Uploaded resumes are stored temporarily during processing.

The backend deletes the temporary uploaded file after processing, including after errors.

## 🛠️ Tech Stack

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

### AI Model

The application currently uses:

```text
openai/gpt-oss-20b
```

through the Groq API.

## 📁 Project Structure

```text
ai-resume-analyzer/
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

> The `.env`, `venv/`, uploaded resumes, Python cache files, and other local/generated files are intentionally excluded from version control.

## ⚙️ Requirements

Before running the project locally, install:

* Python 3.14 or a compatible Python version
* Node.js and npm
* A Groq API key

## 🚀 Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Rounak4742/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Create a Python virtual environment

#### Windows

```bat
python -m venv venv
```

Activate it:

```bat
venv\Scripts\activate
```

### 3. Install backend dependencies

```bat
pip install -r requirements.txt
```

### 4. Configure the Groq API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

**Never commit `.env` or expose the API key publicly.**

### 5. Start the backend

From the project root:

```bat
venv\Scripts\python.exe -m uvicorn main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## 💻 Frontend Setup

Open another terminal.

Navigate to the frontend:

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

### Frontend API Configuration

The frontend can be configured using the Vite environment variable:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

If the variable is not provided, the frontend defaults to:

```text
http://127.0.0.1:8000
```

## 📄 Using the Application

1. Start the FastAPI backend.
2. Start the React frontend.
3. Open the frontend in your browser.
4. Upload a PDF or DOCX resume.
5. Optionally enter a job description.
6. Click **Analyze Resume**.
7. Review the generated analysis.

The results can include:

* Resume score
* ATS match score
* Candidate information
* Skills
* Education
* Experience
* Projects
* Certifications
* Matching keywords
* Missing keywords
* Strengths
* Weaknesses
* Improvement suggestions

## 🔌 API Endpoints

### `GET /`

Returns the basic API status.

### `GET /health`

Returns the backend health status.

### `POST /upload`

Uploads a resume and optionally accepts a job description.

Supported files:

```text
.pdf
.docx
```

Maximum file size:

```text
5 MB
```

The endpoint returns structured resume analysis and ATS results when a job description is provided.

## 🛡️ File Validation & Error Handling

The backend handles several invalid input scenarios.

### Supported formats

```text
PDF
DOCX
```

### Maximum size

```text
5 MB
```

### Validation includes

* Unsupported file extensions
* Empty files
* Files exceeding the size limit
* Corrupted PDF files
* Corrupted DOCX files
* Document processing failures
* Temporary file cleanup

These cases are covered by the automated test suite.

## 🧪 Testing

The project includes automated backend tests using pytest.

Run the complete test suite:

```bat
venv\Scripts\python.exe -m pytest -v
```

### Current test coverage

The test suite covers:

* API home endpoint
* Health endpoint
* Unsupported file types
* Empty files
* Corrupted PDF files
* Corrupted DOCX files
* File size validation
* Successful PDF uploads
* Successful DOCX uploads
* Uploads without job descriptions
* Internal processing errors
* Temporary file cleanup
* PDF extraction
* DOCX extraction

### Test Result

Current backend test suite:

```text
14 passed
```

```text
====================== 14 passed in 73.06s ======================
```

## 📦 Production Build

To verify the React frontend production build:

```bat
cd frontend
npm run build
```

The production files are generated in:

```text
frontend/dist/
```

The production build currently completes successfully.

## ☁️ Deployment

The application is deployed using Render.

### Production Frontend

```text
https://ai-resume-analyzer-frontend-bdme.onrender.com
```

The frontend communicates with the deployed FastAPI backend through the configured production API URL.

The backend has been deployed separately and exposes the FastAPI REST API and health endpoint.

## 🔐 Security & Privacy

The project follows several basic security practices:

* API keys are stored in environment variables.
* `.env` is excluded from Git.
* Uploaded resume files are temporary.
* Uploaded files are deleted after processing.
* Resume PDF files are excluded from Git.
* File size and file type are validated before processing.

**Important:** Users should avoid uploading sensitive documents containing information they do not want processed by a third-party AI service.

## ⚠️ Current Limitations

The current implementation intentionally focuses on text-based PDF and DOCX resumes.

Currently not supported:

* OCR for scanned/image-only PDFs
* User authentication
* Persistent resume history
* Database-backed analysis storage
* Multiple-user accounts
* Advanced semantic ATS ranking
* Resume export functionality

## 🔮 Future Improvements

Possible future improvements include:

* OCR support for scanned resumes
* User authentication
* Resume history and saved analyses
* Database-backed analysis storage
* More advanced semantic ATS scoring
* Improved resume section detection
* Resume improvement/rewrite assistance
* Exporting analysis results as PDF
* Automated CI/CD
* More comprehensive frontend testing
* Better monitoring and observability

## 📌 Project Status

The current version provides a working end-to-end resume analysis pipeline:

```text
Resume Upload
      ↓
File Validation
      ↓
PDF/DOCX Extraction
      ↓
Text Cleaning
      ↓
Groq AI Analysis
      ↓
Structured Validation
      ↓
ATS Keyword Matching
      ↓
Results Dashboard
```

The application has been tested locally and deployed successfully.

## 👨‍💻 Author

**Rounak Kumar**

AI Powered Resume Analyzer built as a full-stack project using:

* FastAPI
* React
* Groq AI
* Python
* JavaScript

---

⭐ If you find this project useful, consider giving the repository a star.
