import { useState } from "react";
import ScoreResult from "./ScoreResult";
import { getAnonymousId } from "../utils/anonymousId";

export default function TextAnalysis({ onResult }) {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/text/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, user_id: getAnonymousId() }),
      });
      const data = await res.json();
      setResult(data);
      onResult?.(data.score_breakdown?.text_score ?? 0);
    } catch {
      setResult({ score_breakdown: { text_score: 0 }, issues: ["Could not reach the API."] });
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="card">
      <div className="card-header">
        <div className="card-icon">📝</div>
        <h2>Text Analysis</h2>
        <span className="card-tag">NLP</span>
      </div>

      <div className="textarea-wrap">
        <textarea
          placeholder="Paste your text here to check for AI slop patterns…"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <span className="char-count">{text.length} chars</span>
      </div>

      <button
        className="btn"
        onClick={analyze}
        disabled={loading || !text.trim()}
      >
        <span className="btn-icon">{loading ? "⟳" : "→"}</span>
        {loading ? "Analyzing…" : "Run Analysis"}
      </button>

      {result && (
        <ScoreResult
          score={result.score_breakdown?.text_score ?? 0}
          issues={result.score_breakdown?.issues ?? []}
          label="Slop Score"
        />
      )}
    </section>
  );
}