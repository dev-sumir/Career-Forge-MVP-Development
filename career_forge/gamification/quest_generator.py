# career_forge/gamification/quest_generator.py

import os
import json
import google.generativeai as genai
from typing import List
from ..schemas.quest import Quest
from ..engine.llm_analyzer import LLMAnalysis
from dotenv import load_dotenv

load_dotenv()


def generate_quests_with_llm(analysis: LLMAnalysis) -> List[Quest]:
    """
    Generates personalized quests using the Gemini LLM based on the user's full profile analysis.
    """
    if not os.environ.get("GOOGLE_API_KEY"):
        # If the API key isn't set, return an empty list instead of crashing.
        print("Warning: GOOGLE_API_KEY not set. Cannot generate LLM-based quests.")
        return []

    model = genai.GenerativeModel('gemini-1.5-flash')

    # Convert the analysis object to a string for the prompt
    analysis_context = analysis.model_dump_json(indent=2)

    # This is the "Quest Master" prompt. It provides the full user context
    # and asks the AI to create relevant, actionable quests.
    master_prompt = f"""
    You are a 'Quest Master' for a career development platform called 'Career Forge'.
    Your goal is to create personalized quests for a user based on their resume analysis.

    Here is the user's profile analysis:
    ---
    {analysis_context}
    ---

    Based on this analysis, generate a list of 3-4 quests. The quests should:
    1.  Be actionable and specific.
    2.  Help the user improve their existing skills or gain new, relevant ones.
    3.  Be personalized to their profile (mention their strengths or projects if relevant).
    4.  Include a mix of categories like 'Daily', 'Side Mission', and 'Weekly Challenge'.

    Return your response as a valid JSON object which is a list of quests, following this exact structure:
    [
      {{
        "title": "Quest Title (e.g., 'Daily Python Practice')",
        "description": "A specific and actionable description of the task.",
        "category": "The primary skill category this quest improves (e.g., 'TechnicalSkills', 'SoftSkills').",
        "rewards": ["A list of rewards, like '+50 XP Python', '+10 XP Problem Solving'"]
      }}
    ]
    """

    # A slightly higher temperature allows for more creative and varied quest suggestions.
    generation_config = genai.types.GenerationConfig(
        response_mime_type="application/json",
        temperature=0.5
    )

    try:
        response = model.generate_content(
            master_prompt,
            generation_config=generation_config
        )

        # The response should be a JSON string representing a list of quests
        quests_data = json.loads(response.text)

        # Validate the data using our Pydantic model
        validated_quests = [Quest(**q) for q in quests_data]
        return validated_quests

    except Exception as e:
        print(f"Error generating quests with LLM: {e}")
        # Return a fallback quest if the LLM fails
        return [
            Quest(
                title="Explore Your Profile",
                description="Review the skills and experiences identified in your profile. Think about which skill you'd like to improve first.",
                category="Intelligence",
                rewards=["+10 XP Self-Awareness"]
            )
        ]