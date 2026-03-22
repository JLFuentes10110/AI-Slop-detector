from fastapi import APIRouter

from database import supabase
from models import TextAnalysisRequest, AnalysisResponse
from analyzers.text_analyzer import analyze_text
from scorer import build_score_breakdown

router = APIRouter(prefix="/api/text", tags=["Text"])


@router.post("/analyze", response_model=AnalysisResponse)
def analyze_text_endpoint(request: TextAnalysisRequest):
    text_score, text_issues, text_suggestions = analyze_text(request.text)

    breakdown = build_score_breakdown(
        text_score=text_score,
        image_score=None,
        behavior_score=None,
        all_issues=text_issues,
        all_suggestions=text_suggestions,
    )

    response = supabase.table("text_analysis").insert({
        "user_id":    request.user_id,
        "text":       request.text,
        "slop_score": text_score,
        "issues":     text_issues,
    }).execute()

    row = response.data[0]

    return AnalysisResponse(
        submission_id=row["id"],
        user_id=request.user_id,
        score_breakdown=breakdown,
        analyzed_at=row["created_at"],
    )
