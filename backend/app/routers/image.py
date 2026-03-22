from fastapi import APIRouter, UploadFile, File, Form

from database import supabase
from models import AnalysisResponse
from analyzers.image_analyzer import analyze_image
from scorer import build_score_breakdown

router = APIRouter(prefix="/api/image", tags=["Image"])


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_image_endpoint(
    user_id: str = Form(None),
    file: UploadFile = File(...),
):
    image_bytes = await file.read()
    image_score, img_issues, img_suggestions = analyze_image(image_bytes)

    breakdown = build_score_breakdown(
        text_score=None,
        image_score=image_score,
        behavior_score=None,
        all_issues=img_issues,
        all_suggestions=img_suggestions,
    )

    response = supabase.table("image_analysis").insert({
        "user_id":    user_id,
        "filename":   file.filename,
        "slop_score": image_score,
        "issues":     img_issues,
    }).execute()

    row = response.data[0]

    return AnalysisResponse(
        submission_id=row["id"],
        user_id=user_id,
        score_breakdown=breakdown,
        analyzed_at=row["created_at"],
    )
