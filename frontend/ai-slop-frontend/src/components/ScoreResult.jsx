export default function ScoreResult({ score, issues = [], label = "Score" }) {
  const tier =
    score >= 70 ? "green" :
    score >= 40 ? "yellow" :
    "red";

  const grade =
    score >= 70 ? "Clean" :
    score >= 40 ? "Moderate" :
    "High Risk";

  const barColor =
    tier === "green"  ? "var(--green)"  :
    tier === "yellow" ? "var(--yellow)" :
    "var(--red)";

  return (
    <div className="result">
      <div className="result-score-row">
        <div>
          <div className="result-label">{label}</div>
          <div className={`result-score score-${tier}`}>{score}</div>
        </div>
        <span className={`result-badge badge-${tier}`}>{grade}</span>
      </div>

      <div className="progress-bar">
        <div
          className="progress"
          style={{ width: `${score}%`, background: barColor }}
        />
      </div>

      <div className="issues-label">Detected issues</div>
      {issues.length > 0 ? (
        <ul className="issues-list">
          {issues.map((issue, i) => (
            <li key={i}>{issue}</li>
          ))}
        </ul>
      ) : (
        <p className="no-issues">✓ No issues detected</p>
      )}
    </div>
  );
}