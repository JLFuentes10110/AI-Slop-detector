from fastapi import APIRouter

from database import supabase
from models import BehaviorAnalysisRequest, AnalysisResponse
from analyzers.behavior_analyzer import analyze_behavior
from scorer import build_score_breakdown

router = APIRouter(prefix="/api/behavior", tags=["Behavior"])


@router.post("/analyze", response_model=AnalysisResponse)
def analyze_behavior_endpoint(request: BehaviorAnalysisRequest):
    behavior_score, behavior_issues, behavior_suggestions = analyze_behavior(
        typing_time=request.typingTime,
        posts_per_day=request.postsPerDay,
    )

    breakdown = build_score_breakdown(
        text_score=None,
        image_score=None,
        behavior_score=behavior_score,
        all_issues=behavior_issues,
        all_suggestions=behavior_suggestions,
    )

    response = supabase.table("behavior_analysis").insert({
        "user_id":       request.user_id,
        "typing_time":   request.typingTime,
        "posts_per_day": request.postsPerDay,
        "fatigue_score": behavior_score,
        "issues":        behavior_issues,
    }).execute()

    row = response.data[0]

    return AnalysisResponse(
        submission_id=row["id"],
        user_id=request.user_id,
        score_breakdown=breakdown,
        analyzed_at=row["created_at"],
    )
