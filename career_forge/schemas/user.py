# career_forge/schemas/user.py

from pydantic import BaseModel, Field
from typing import List

class Skill(BaseModel):
    """Represents a single, levelable skill in the user's profile."""
    name: str
    category: str
    level: int = 1
    xp: int = 0
    xp_to_next_level: int = 100

class UserProfile(BaseModel):
    """Represents the complete gamified user profile."""
    user_name: str = Field(description="The user's full name.")
    job_title: str = Field(description="The user's current job title or headline.")
    main_rank: str = Field(description="The user's overall career rank (e.g., E, D, C, B, A, S).")
    level: int = Field(description="The user's main level within their current rank.")
    xp: int = Field(description="The user's main experience points.")
    skills: List[Skill] = Field(description="A list of all skills identified for the user, each with its own level.")