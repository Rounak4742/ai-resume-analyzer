# AI Powered Resume Analyzer

An AI-powered resume analysis web application that analyzes PDF and DOCX resumes, extracts structured candidate information, evaluates resume quality, and calculates an ATS match score against a provided job description.

## Features

- Upload PDF and DOCX resumes
- Maximum upload size of 5 MB
- Automatic resume text extraction
- Text cleaning and preprocessing
- AI-powered resume analysis using Groq
- Structured resume information extraction
- Resume quality score
- Strengths, weaknesses, and improvement suggestions
- Optional job description analysis
- ATS keyword matching
- ATS match score
- Matching and missing keyword detection
- Temporary uploaded files are automatically deleted after processing
- REST API built with FastAPI
- React frontend
- Automated backend tests with pytest

## Tech Stack

### Backend

- Python
- FastAPI
- Groq API
- Pydantic
- pdfplumber
- python-docx
- python-multipart
- python-dotenv
- pytest
- httpx

### Frontend

- React
- Vite
- JavaScript
- CSS

## Architecture

The application follows this processing pipeline:

```text
User
  │
  ▼
React Frontend
  │
  │ PDF/DOCX + Job Description
  ▼
FastAPI Backend
  │
  ├── File Validation
  │
  ├── PDF/DOCX Text Extraction
  │
  ├── Text Cleaning
  │
  ├── Groq AI Resume Analysis
  │
  ├── ATS Keyword Matching
  │
  └── Structured API Response
  │
  ▼
React Results Dashboard
