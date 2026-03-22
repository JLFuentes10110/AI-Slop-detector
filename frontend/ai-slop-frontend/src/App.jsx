import { useState, useEffect } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
} from "chart.js";

import Header from "./components/Header";
import TextAnalysis from "./components/TextAnalysis";
import ImageAnalysis from "./components/ImageAnalysis";
import BehaviorAnalysis from "./components/BehaviorAnalysis";
import Dashboard from "./components/Dashboard";
import "./App.css";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip);

export default function App() {
  const [theme, setTheme] = useState(() =>
    localStorage.getItem("theme") || "dark"
  );
  const [textScore,     setTextScore]     = useState(0);
  const [imageScore,    setImageScore]    = useState(0);
  const [behaviorScore, setBehaviorScore] = useState(0);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () =>
    setTheme((t) => (t === "dark" ? "light" : "dark"));

  return (
    <div className="app">
      <div className="grid-overlay" aria-hidden="true" />
      <div className="app-inner">
        <Header theme={theme} onToggleTheme={toggleTheme} />
        <main className="main-grid">
          <TextAnalysis     onResult={setTextScore} />
          <ImageAnalysis    onResult={setImageScore} />
          <BehaviorAnalysis onResult={setBehaviorScore} />
          <Dashboard
            textScore={textScore}
            imageScore={imageScore}
            behaviorScore={behaviorScore}
          />
        </main>
      </div>
    </div>
  );
}