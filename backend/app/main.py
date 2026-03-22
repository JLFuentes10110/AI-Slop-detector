from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import text, image, behavior

app = FastAPI(
    title="AI Slop & Fatigue Detection System",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # tighten to your frontend URL before deploying
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(text.router)
app.include_router(image.router)
app.include_router(behavior.router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "AI Slop & Fatigue Detection API", "docs": "/docs"}
