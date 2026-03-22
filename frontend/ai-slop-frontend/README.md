# AI Slop & Fatigue Detection System

A web-based system that detects low-quality AI-generated content ("AI slop") and user over-reliance on AI ("AI fatigue") across text and images.

---

## What It Does

| Module | What It Analyzes | Output |
|---|---|---|
| Text Analysis | Vocabulary diversity, repeated phrases, AI filler language, sentence uniformity | Slop Score (0–100) |
| Image Analysis | Blur, noise, color uniformity, edge patterns, AI-generation detection | Image Quality Score (0–100) |
| Behavior Analysis | Typing speed, posts per day | Fatigue Score (0–100) |
| Dashboard | Combines all three scores | Unified overview |

---

## Tech Stack

**Backend**
- Python + FastAPI
- spaCy (NLP / text analysis)
- OpenCV + NumPy (image processing)
- HuggingFace Transformers (AI image detection)
- Supabase (PostgreSQL database)

**Frontend**
- React (Vite)
- Chart.js (dashboard bar chart)
- Space Mono + Syne (Google Fonts)

---

## Project Structure

```
ai-slop-detector/
├── backend/
│   └── app/
│       ├── analyzers/
│       │   ├── __init__.py
│       │   ├── text_analyzer.py
│       │   ├── image_analyzer.py
│       │   └── behavior_analyzer.py
│       ├── routers/
│       │   ├── __init__.py
│       │   ├── text.py
│       │   ├── image.py
│       │   └── behavior.py
│       ├── .env
│       ├── database.py
│       ├── main.py
│       ├── models.py
│       ├── scorer.py
│       ├── run.py
│       └── requirements.txt
└── frontend/
    └── src/
        ├── components/
        │   ├── Header.jsx
        │   ├── TextAnalysis.jsx
        │   ├── ImageAnalysis.jsx
        │   ├── BehaviorAnalysis.jsx
        │   ├── ScoreResult.jsx
        │   └── Dashboard.jsx
        ├── utils/
        │   └── anonymousId.js
        ├── App.jsx
        └── App.css
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- A [Supabase](https://supabase.com) account (free tier is fine)

---

### 1. Database Setup

In your Supabase project, go to **SQL Editor** and run:

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS text_analysis (
    id          UUID      PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id     TEXT,
    text        TEXT      NOT NULL,
    slop_score  FLOAT     CHECK (slop_score BETWEEN 0 AND 100),
    issues      TEXT[],
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS image_analysis (
    id          UUID      PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id     TEXT,
    filename    TEXT      NOT NULL,
    slop_score  FLOAT     CHECK (slop_score BETWEEN 0 AND 100),
    issues      TEXT[],
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS behavior_analysis (
    id              UUID      PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         TEXT,
    typing_time     FLOAT,
    posts_per_day   INT,
    fatigue_score   FLOAT     CHECK (fatigue_score BETWEEN 0 AND 100),
    issues          TEXT[],
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

### 2. Backend Setup

```bash
cd backend/app

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Download the spaCy language model
python -m spacy download en_core_web_sm
```

Fill in your Supabase credentials in `.env`:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-service-role-secret-key
```

> Find these in your Supabase dashboard under **Project Settings → API**.
> Use the **service_role** secret key for the backend.

Start the server:

```bash
python run.py
```

The API will be running at `http://127.0.0.1:8000`.
Interactive docs available at `http://127.0.0.1:8000/docs`.

---

### 3. Frontend Setup

```bash
cd frontend

npm install
npm run dev
```

The app will be running at `http://localhost:5173`.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/text/analyze` | Analyze text for slop patterns |
| `POST` | `/api/image/analyze` | Analyze an image file |
| `POST` | `/api/behavior/analyze` | Analyze user behavior patterns |
| `GET` | `/health` | Health check |
| `GET` | `/docs` | Swagger UI (auto-generated) |

### Example Request — Text Analysis

```bash
curl -X POST http://127.0.0.1:8000/api/text/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "optional-anonymous-id",
    "text": "In conclusion, it is important to note that AI is transforming many industries."
  }'
```

### Example Response

```json
{
  "submission_id": "9206-4d03-42cc...",
  "user_id": "optional-anonymous-id",
  "score_breakdown": {
    "text_score": 70.0,
    "image_score": null,
    "behavior_score": null,
    "unified_slop_score": 70.0,
    "grade": "High slop",
    "issues": [
      "AI filler phrase(s) detected: in conclusion, it is important to note"
    ],
    "suggestions": [
      "Remove generic transitional phrases typical of AI output."
    ]
  },
  "analyzed_at": "2026-03-22T19:31:38Z"
}
```

---

## Score Grades

| Score | Grade |
|---|---|
| 0 – 19 | Clean |
| 20 – 44 | Mild slop |
| 45 – 64 | Suspicious |
| 65 – 79 | High slop |
| 80 – 100 | AI slop |

---

## Anonymous User Tracking

This app requires no login. Each browser automatically gets a UUID on first visit, stored in `localStorage`. This ID is attached to every analysis request so behavior patterns (posting frequency, content similarity) can be tracked per user without any authentication.

```js
// src/utils/anonymousId.js
export function getAnonymousId() {
  const key = "slop_anon_id";
  let id = localStorage.getItem(key);
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem(key, id);
  }
  return id;
}
```

Clearing browser storage generates a new ID — this is expected behavior for an anonymous tool.

---

## Dependencies

### Backend

| Package | Purpose |
|---|---|
| `fastapi` | REST API framework |
| `uvicorn` | ASGI server |
| `supabase` | Supabase Python client |
| `python-dotenv` | Load `.env` variables |
| `spacy` | NLP text analysis |
| `opencv-python-headless` | Image processing |
| `numpy` | Numerical operations |
| `transformers` | HuggingFace AI image detection |
| `torch` | PyTorch backend for transformers |
| `Pillow` | Image format handling |
| `python-multipart` | File upload support |

### Frontend

| Package | Purpose |
|---|---|
| `react` | UI framework |
| `react-chartjs-2` | Chart.js wrapper for React |
| `chart.js` | Bar chart on dashboard |

---

## Notes

- On first startup after adding the `transformers` model, the server will download ~500MB for the AI image detection model. This only happens once — subsequent restarts use the local cache.
- The `.env` file is intentionally excluded from version control. Never commit your Supabase service role key to GitHub.
- The app is designed for deployment without user authentication. All analysis data is stored anonymously.