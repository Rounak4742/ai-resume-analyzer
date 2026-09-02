function UploadForm({
  file,
  jobDescription,
  loading,
  error,
  onFileChange,
  onJobDescriptionChange,
  onAnalyze,
}) {
  return (
    <section className="card upload-card">
      <div className="card-eyebrow">Step 1</div>
      <h2>Upload your resume</h2>
      <p className="muted">
        PDF or DOCX, up to 5MB. Paste a job description below to also get an ATS match score.
      </p>

      <label className="dropzone" htmlFor="resume-file">
        <input id="resume-file" type="file" accept=".pdf,.docx" onChange={onFileChange} />
        {file ? (
          <span className="dropzone-filename">{file.name}</span>
        ) : (
          <span>Click to choose a resume file (PDF or DOCX)</span>
        )}
      </label>

      <label htmlFor="job-description">Job description (optional)</label>
      <textarea
        id="job-description"
        placeholder="Paste the job description here to get an ATS match score..."
        value={jobDescription}
        onChange={onJobDescriptionChange}
        rows={8}
      />

      <button onClick={onAnalyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze resume"}
      </button>

      {error && (
        <div className="error-box" role="alert">
          <strong>Couldn't complete analysis</strong>
          <p>{error}</p>
        </div>
      )}
    </section>
  );
}

export default UploadForm;
