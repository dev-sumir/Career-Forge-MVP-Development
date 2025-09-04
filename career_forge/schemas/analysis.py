# career_forge/schemas/analysis.py

from pydantic import BaseModel, Field
from typing import List
from .user import UserProfile
from .quest import Quest

class AnalysisResult(BaseModel):
    """The final, combined response object for the main API endpoint."""
    profile: UserProfile = Field(description="The generated gamified user profile.")
    quests: List[Quest] = Field(description="A list of personalized quests for the user.")