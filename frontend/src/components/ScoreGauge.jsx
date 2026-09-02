function ScoreGauge({ label, value, tone = "primary" }) {
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const clamped = Math.max(0, Math.min(100, Number(value) || 0));
  const offset = circumference - (clamped / 100) * circumference;

  return (
    <div className="gauge">
      <svg viewBox="0 0 130 130" className="gauge-svg" role="img" aria-label={`${label}: ${clamped} out of 100`}>
        <circle cx="65" cy="65" r={radius} className="gauge-track" />
        <circle
          cx="65"
          cy="65"
          r={radius}
          className={`gauge-value gauge-value--${tone}`}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          transform="rotate(-90 65 65)"
        />
      </svg>
      <div className="gauge-center">
        <span className="gauge-number">{clamped}</span>
        <span className="gauge-max">/100</span>
      </div>
      <p className="gauge-label">{label}</p>
    </div>
  );
}

export default ScoreGauge;
