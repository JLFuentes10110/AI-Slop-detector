import { useState } from "react";
import ScoreResult from "./ScoreResult";
import { getAnonymousId } from "../utils/anonymousId";

export default function ImageAnalysis({ onResult }) {
  const [fileName, setFileName] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFile = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setFileName(file.name);
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_id", getAnonymousId());

    try {
      const res = await fetch("http://127.0.0.1:8000/api/image/analyze", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResult(data);
      onResult?.(data.score_breakdown?.image_score ?? 0);
    } catch {
      setResult({ score_breakdown: { image_score: 0, issues: ["Could not reach the API."] } });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <div className="card-title-group">
          <div className="card-icon">🖼️</div>
          <span className="card-title">Image Analysis</span>
        </div>
        <span className="card-tag">CV</span>
      </div>

      <div className={`file-drop${fileName && !loading ? " has-file" : ""}`}>
        <input type="file" accept="image/*" onChange={handleFile} />
        <span className="file-drop-icon">
          {loading ? "⏳" : fileName ? "✅" : "📂"}
        </span>
        <span className="file-drop-label">
          {loading
            ? "Processing…"
            : fileName
            ? "Image loaded — click to replace"
            : <><span>Click to upload</span> or drop an image</>}
        </span>
        {fileName && !loading && (
          <div className="file-name">↳ {fileName}</div>
        )}
      </div>

      {result && (
        <ScoreResult
          score={result.score_breakdown?.image_score ?? 0}
          issues={result.score_breakdown?.issues ?? []}
          label="Image Quality Score"
        />
      )}
    </div>
  );
}