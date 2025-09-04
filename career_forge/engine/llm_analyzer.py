# career_forge/engine/llm_analyzer.py

import os
import json
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

try:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
except TypeError:
    print("GOOGLE_API_KEY environment variable not set. LLM Analyzer will not work.")


class ExperienceDetail(BaseModel):
    category: str = Field(description="The type of experience (e.g., 'Leadership Role', 'Project', 'Achievement').")
    title: str = Field(
        description="The title or name of the experience (e.g., 'ICT Prefect', 'AI-Based Resume Ranker').")
    organization: str = Field(description="The organization or school where the experience occurred, if mentioned.")
    description: str = Field(description="A brief, one-sentence summary of the experience.")


class LLMAnalysis(BaseModel):
    user_name: str = Field(description="The full name of the candidate as listed on the resume.")
    job_title: str = Field(description="The candidate's current job title or professional headline.")
    summary: str = Field(description="A 2-3 sentence professional summary of the candidate's profile.")
    suggested_rank: str = Field(description="A suggested rank (E, D, C, B, A, S) based on overall experience.")
    suggested_level: int = Field(description="A suggested starting level (1-99) within that rank.")
    skills: Dict[str, List[str]] = Field(description="Skills categorized into Technical, Soft, and Intelligence.")
    experiences: List[ExperienceDetail] = Field(description="A list of detailed experiences extracted from the resume.")
    inferred_strengths: List[str] = Field(
        description="A list of 2-3 key strengths inferred from projects and experience.")


def analyze_resume_with_llm(resume_text: str) -> LLMAnalysis:
    """
    Analyzes resume text using Google's Gemini model to extract structured data and insights.
    """
    if not os.environ.get("GOOGLE_API_KEY"):
        raise ConnectionError("Google AI client is not configured. Please set your GOOGLE_API_KEY.")

    model = genai.GenerativeModel('gemini-1.5-pro-latest')

    master_prompt = f"""
    You are an expert tech recruiter analyzing a resume. Provide a structured analysis in a valid JSON format.

    Analyze the following resume text:
    ---
    {resume_text}
    ---

    Based on the text, provide a JSON object with the following structure:
    {{
      "user_name": "Extract the candidate's full name, which is usually at the very top. If no name is found, default to 'User'.",
      "job_title": "Extract the candidate's current job title or professional headline (e.g., 'Software Engineer' or 'B.E. Computer Science Student').",
      "summary": "A 2-3 sentence professional summary of the candidate's profile.",
      "suggested_rank": "Suggest a starting rank from E, D, C, B, A, or S.",
      "suggested_level": "Suggest a starting level between 1 and 99.",
      "skills": {{
        "TechnicalSkills": ["List all specific software, tools, programming languages, and methodologies like Agile or Scrum."],
        "SoftSkills": ["List interpersonal abilities like Communication, Teamwork, or Leadership."],
        "Intelligence": ["List cognitive skills like Problem Solving, Critical Thinking, or Data Analysis."]
      }},
      "experiences": [
        {{
          "category": "Identify the type of experience. Look for sections like 'Experience', 'Projects', 'Achievements', or 'Leadership Roles'. A school role like 'Prefect' is a 'Leadership Role'.",
          "title": "Extract the title or name of the experience (e.g., 'ICT Prefect', 'AI-Based Resume Ranker').",
          "organization": "Extract the organization or school, if mentioned. Otherwise, use 'N/A'.",
          "description": "Write a brief, one-sentence summary of what the person did or achieved in this experience."
        }}
      ],
      "inferred_strengths": ["List 2-3 key strengths you inferred from the content."]
    }}
    """

    generation_config = genai.types.GenerationConfig(
        response_mime_type="application/json",
        temperature=0.0
    )

    response = model.generate_content(
        master_prompt,
        generation_config=generation_config
    )

    try:
        analysis_json = json.loads(response.text)
        return LLMAnalysis(**analysis_json)
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error parsing LLM response: {e}")
        return None