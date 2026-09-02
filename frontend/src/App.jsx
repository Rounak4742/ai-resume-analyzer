import { useState } from "react";
import UploadForm from "./components/UploadForm";
import ResultsDashboard from "./components/ResultsDashboard";
import "./App.css";

const API_BASE = "http://127.0.0.1:8000";
const API_URL = `${API_BASE}/upload`;
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ALLOWED_EXTENSIONS = [".pdf", ".docx"];

function getExtension(filename) {
  const idx = filename.lastIndexOf(".");
  return idx === -1 ? "" : filename.slice(idx).toLowerCase();
}

function validateFile(selected) {
  if (!selected) {
    return "Please select a PDF or DOCX resume.";
  }
  if (!ALLOWED_EXTENSIONS.includes(getExtension(selected.name))) {
    return "Unsupported file type. Please upload a PDF or DOCX file.";
  }
  if (selected.size === 0) {
    return "This file appears to be empty. Please choose a valid resume file.";
  }
  if (selected.size > MAX_FILE_SIZE) {
    return "File is too large. Please upload a resume under 5MB.";
  }
  return "";
}

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const selected = event.target.files[0] || null;
    setError("");
    setResult(null);
    setFile(selected);
  };

  const handleAnalyze = async () => {
    const validationError = validateFile(file);
    if (validationError) {
      setError(validationError);
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", jobDescription);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });

      let data = null;
      try {
        data = await response.json();
      } catch {
        throw new Error("The server sent back an unreadable response. Please try again.");
      }

      if (!response.ok) {
        throw new Error(
          data?.detail ||
            "Analysis failed. The AI analysis service may be temporarily unavailable — please try again shortly."
        );
      }

      setResult(data);
    } catch (err) {
      if (err instanceof TypeError) {
        setError(
          `Can't reach the server. Make sure the backend is running at ${API_BASE}.`
        );
      } else {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setJobDescription("");
    setResult(null);
    setError("");
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Resume Analyzer</h1>
        <p>Upload a resume to get an instant score, ATS match, and improvement suggestions.</p>
      </header>

      <main className="app-main">
        {!result ? (
          <UploadForm
            file={file}
            jobDescription={jobDescription}
            loading={loading}
            error={error}
            onFileChange={handleFileChange}
            onJobDescriptionChange={(event) => setJobDescription(event.target.value)}
            onAnalyze={handleAnalyze}
          />
        ) : (
          <ResultsDashboard result={result} onReset={handleReset} />
        )}
      </main>
    </div>
  );
}

export default App;
