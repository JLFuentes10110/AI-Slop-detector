from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TextAnalysisRequest(BaseModel):
    user_id: Optional[str] = None
    text: str = Field(..., min_length=10)


class ImageAnalysisRequest(BaseModel):
    user_id: Optional[str] = None


class BehaviorAnalysisRequest(BaseModel):
    user_id: Optional[str] = None
    typingTime: float = Field(..., ge=0)
    postsPerDay: int = Field(..., ge=0)


class ScoreBreakdown(BaseModel):
    text_score: Optional[float] = None
    image_score: Optional[float] = None
    behavior_score: Optional[float] = None
    unified_slop_score: float
    grade: str
    issues: List[str]
    suggestions: List[str]


class AnalysisResponse(BaseModel):
    submission_id: str
    user_id: Optional[str]
    score_breakdown: ScoreBreakdown
    analyzed_at: datetime
