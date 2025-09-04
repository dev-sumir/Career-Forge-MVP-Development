# career_forge/schemas/quest.py

from pydantic import BaseModel, Field
from typing import List

class Quest(BaseModel):
    """Represents a single, actionable task for the user."""
    title: str = Field(description="The short, clear name of the quest.")
    description: str = Field(description="A brief explanation of what the user needs to do.")
    category: str = Field(description="The skill category this quest belongs to (e.g., PROGRAMMING).")
    rewards: List[str] = Field(description="A list of rewards for completing the quest (e.g., '+50 XP Python').")