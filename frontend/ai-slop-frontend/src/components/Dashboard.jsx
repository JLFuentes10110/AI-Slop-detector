import { Bar } from "react-chartjs-2";

function getColor(score) {
  if (score >= 70) return "var(--green)";
  if (score >= 40) return "var(--yellow)";
  return "var(--red)";
}

function getTier(score) {
  if (score >= 70) return "green";
  if (score >= 40) return "yellow";
  return "red";
}

function StatTile({ label, score }) {
  const tier = getTier(score);
  return (
    <div className="dash-stat">
      <div className="dash-stat-label">{label}</div>
      <div className={`dash-stat-value score-${tier}`}>{score}</div>
      <div className="dash-stat-sub">/ 100</div>
    </div>
  );
}

export default function Dashboard({ textScore, imageScore, behaviorScore }) {
  const hasAny = textScore > 0 || imageScore > 0 || behaviorScore > 0;

  const chartData = {
    labels: ["Text", "Image", "Behavior"],
    datasets: [
      {
        data: [textScore, imageScore, behaviorScore],
        backgroundColor: [
          getColor(textScore),
          getColor(imageScore),
          getColor(behaviorScore),
        ],
        borderRadius: 4,
        borderSkipped: false,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: "#0d1117",
        borderColor: "#1e2d3d",
        borderWidth: 1,
        titleFont: { family: "'Space Mono', monospace", size: 11 },
        bodyFont:  { family: "'Space Mono', monospace", size: 11 },
        titleColor: "#c9d8e8",
        bodyColor:  "#c9d8e8",
        callbacks: {
          label: (ctx) => ` Score: ${ctx.raw}`,
        },
      },
    },
    scales: {
      x: {
        grid: { color: "#1e2d3d" },
        ticks: { color: "#4a6070", font: { family: "'Space Mono', monospace", size: 10 } },
        border: { color: "#1e2d3d" },
      },
      y: {
        min: 0,
        max: 100,
        grid: { color: "#1e2d3d" },
        ticks: { color: "#4a6070", font: { family: "'Space Mono', monospace", size: 10 } },
        border: { color: "#1e2d3d" },
      },
    },
  };

  return (
    <section className="card dashboard-section">
      <div className="card-header">
        <div className="card-icon">⚡</div>
        <h2>Overall Dashboard</h2>
        <span className="card-tag">Live</span>
      </div>

      {!hasAny ? (
        <p className="empty-state">Run at least one analysis to see scores here.</p>
      ) : (
        <div className="dashboard-inner">
          <StatTile label="Text Score"     score={textScore} />
          <StatTile label="Image Score"    score={imageScore} />
          <StatTile label="Fatigue Score"  score={behaviorScore} />
          <div className="chart-wrap">
            <div className="chart-label">Score comparison</div>
            <div style={{ height: 100 }}>
              <Bar data={chartData} options={chartOptions} />
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
