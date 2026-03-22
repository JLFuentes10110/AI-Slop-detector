import { useState } from "react";
import ScoreResult from "./ScoreResult";
import { getAnonymousId } from "../utils/anonymousId";

export default function BehaviorAnalysis({ onResult }) {
  const [typingTime, setTypingTime] = useState(2);
  const [postsPerDay, setPostsPerDay] = useState(15);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyze = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/behavior/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: getAnonymousId(),
          typingTime: Number(typingTime),
          postsPerDay: Number(postsPerDay),
        }),
      });
      const data = await res.json();
      setResult(data);
      onResult?.(data.score_breakdown?.behavior_score ?? 0);
    } catch {
      setResult({ score_breakdown: { behavior_score: 0, issues: ["Could not reach the API."] } });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <div className="card-title-group">
          <div className="card-icon">📊</div>
          <span className="card-title">Behavior Analysis</span>
        </div>
        <span className="card-tag">Patterns</span>
      </div>

      <div className="behavior-inputs">
        <div className="input-group">
          <label>Avg. typing time (s)</label>
          <input
            type="number"
            min="0"
            step="0.5"
            value={typingTime}
            onChange={(e) => setTypingTime(e.target.value)}
          />
        </div>
        <div className="input-group">
          <label>Posts per day</label>
          <input
            type="number"
            min="0"
            value={postsPerDay}
            onChange={(e) => setPostsPerDay(e.target.value)}
          />
        </div>
      </div>

      <button className="btn" onClick={analyze} disabled={loading}>
        {loading ? (
          <><span className="btn-spinner" /> Analyzing…</>
        ) : (
          <>▶ Run Analysis</>
        )}
      </button>

      {result && (
        <ScoreResult
          score={result.score_breakdown?.behavior_score ?? 0}
          issues={result.score_breakdown?.issues ?? []}
          label="Fatigue Score"
        />
      )}
    </div>
  );
}