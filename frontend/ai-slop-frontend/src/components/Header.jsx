export default function Header({ theme, onToggleTheme }) {
  const isDark = theme === "dark";

  return (
    <header className="header">
      <div className="header-left">
        <div className="header-eyebrow">
          AI Content Analysis System
        </div>
        <h1>
          Slop<span>Detector</span>
        </h1>
      </div>

      <div className="header-right">
        {/* Theme Toggle */}
        <label className="theme-toggle" aria-label="Toggle theme">
          <span className="theme-toggle-label">
            {isDark ? "Dark" : "Light"}
          </span>
          <div className="theme-toggle-track">
            <input
              type="checkbox"
              checked={!isDark}
              onChange={onToggleTheme}
            />
            <div className="theme-toggle-thumb">
              <span className="theme-toggle-icon">
                {isDark ? "🌙" : "☀️"}
              </span>
            </div>
          </div>
        </label>

        <div className="header-meta">
          <span className="status-dot" />
          API online · localhost:8000
          <br />
          v1.0.0 · {new Date().toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}
        </div>
      </div>
    </header>
  );
}