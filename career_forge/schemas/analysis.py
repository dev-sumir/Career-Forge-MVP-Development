# career_forge/schemas/analysis.py

from pydantic import BaseModel, Field
from typing import List
from .user import UserProfile
from .quest import Quest
# Import the ExperienceDetail model from the analyzer
from ..engine.llm_analyzer import ExperienceDetail

class AnalysisResult(BaseModel):
    """The final, combined response object for the main API endpoint."""
    profile: UserProfile = Field(description="The generated gamified user profile.")
    quests: List[Quest] = Field(description="A list of personalized quests for the user.")
    experiences: List[ExperienceDetail] = Field(description="A detailed list of experiences from the resume.")