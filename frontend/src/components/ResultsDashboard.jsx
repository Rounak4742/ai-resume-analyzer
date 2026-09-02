import ScoreGauge from "./ScoreGauge";

function ResultsDashboard({ result, onReset }) {
  const resume = result.resume || {};
  const ats = result.ats || {};
  const scores = result.scores || {};
  const feedback = result.feedback || {};

  const resumeScore = scores.resume_score ?? resume.resume_score ?? 0;
  const atsScore = scores.ats_match_score ?? ats.ats_match_score ?? 0;

  const contactRows = [
    { label: "Email", value: resume.email },
    { label: "Phone", value: resume.phone },
    { label: "LinkedIn", value: resume.linkedin },
    { label: "GitHub", value: resume.github },
  ].filter((row) => row.value);

  return (
    <section className="dashboard">
      <div className="scan-header">
        <span className="scan-label">Analysis complete</span>
        {result.filename && <span className="scan-filename">{result.filename}</span>}
      </div>

      <div className="card candidate-card">
        <h2>{resume.candidate_name || "Candidate"}</h2>
        {contactRows.length > 0 && (
          <ul className="contact-list">
            {contactRows.map((row) => (
              <li key={row.label}>
                <span className="contact-label">{row.label}</span>
                <span>{row.value}</span>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="gauge-row">
        <ScoreGauge label="Resume score" value={resumeScore} tone="primary" />
        <ScoreGauge
          label="ATS match score"
          value={atsScore}
          tone={atsScore >= 60 ? "good" : "warn"}
        />
      </div>

      {resume.skills?.length > 0 && (
        <div className="card">
          <h3>Skills</h3>
          <div className="tags">
            {resume.skills.map((skill) => (
              <span className="tag" key={skill}>
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {(resume.education?.length > 0 || resume.experience?.length > 0) && (
        <div className="two-col">
          {resume.education?.length > 0 && (
            <div className="card">
              <h3>Education</h3>
              <ul className="stack-list">
                {resume.education.map((edu, i) => (
                  <li key={i}>
                    <strong>
                      {edu.degree}
                      {edu.field ? `, ${edu.field}` : ""}
                    </strong>
                    <p>
                      {edu.institution}
                      {edu.graduation_year ? ` · ${edu.graduation_year}` : ""}
                    </p>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {resume.experience?.length > 0 && (
            <div className="card">
              <h3>Experience</h3>
              <ul className="stack-list">
                {resume.experience.map((exp, i) => (
                  <li key={i}>
                    <strong>{exp.job_title}</strong>
                    <p>
                      {exp.company}
                      {exp.duration ? ` · ${exp.duration}` : ""}
                    </p>
                    {exp.description && <p>{exp.description}</p>}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {(resume.projects?.length > 0 || resume.certifications?.length > 0) && (
        <div className="two-col">
          {resume.projects?.length > 0 && (
            <div className="card">
              <h3>Projects</h3>
              <ul className="stack-list">
                {resume.projects.map((proj, i) => (
                  <li key={i}>
                    <strong>{proj.name}</strong>
                    {proj.description && <p>{proj.description}</p>}
                    {proj.technologies?.length > 0 && (
                      <div className="tags tags--compact">
                        {proj.technologies.map((tech) => (
                          <span className="tag" key={tech}>
                            {tech}
                          </span>
                        ))}
                      </div>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {resume.certifications?.length > 0 && (
            <div className="card">
              <h3>Certifications</h3>
              <ul className="stack-list">
                {resume.certifications.map((cert, i) => (
                  <li key={i}>{cert}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {(feedback.strengths?.length > 0 || feedback.weaknesses?.length > 0) && (
        <div className="two-col">
          {feedback.strengths?.length > 0 && (
            <div className="card">
              <h3>Strengths</h3>
              <ul className="stack-list">
                {feedback.strengths.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </div>
          )}

          {feedback.weaknesses?.length > 0 && (
            <div className="card">
              <h3>Weaknesses</h3>
              <ul className="stack-list">
                {feedback.weaknesses.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {feedback.suggestions?.length > 0 && (
        <div className="card">
          <h3>Suggestions</h3>
          <ul className="stack-list">
            {feedback.suggestions.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      {(ats.matching_keywords?.length > 0 || ats.missing_keywords?.length > 0) && (
        <div className="two-col">
          {ats.matching_keywords?.length > 0 && (
            <div className="card">
              <h3>Matching keywords</h3>
              <div className="tags">
                {ats.matching_keywords.map((kw) => (
                  <span className="tag tag--good" key={kw}>
                    {kw}
                  </span>
                ))}
              </div>
            </div>
          )}

          {ats.missing_keywords?.length > 0 && (
            <div className="card">
              <h3>Missing keywords</h3>
              <div className="tags">
                {ats.missing_keywords.map((kw) => (
                  <span className="tag tag--warn" key={kw}>
                    {kw}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      <button className="secondary-button" onClick={onReset}>
        Analyze another resume
      </button>
    </section>
  );
}

export default ResultsDashboard;
