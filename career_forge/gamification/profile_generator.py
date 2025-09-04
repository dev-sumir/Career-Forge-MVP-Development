# career_forge/gamification/profile_generator.py

from career_forge.schemas.user import UserProfile, Skill
from career_forge.engine.llm_analyzer import LLMAnalysis


def generate_profile_from_llm_analysis(analysis: LLMAnalysis) -> UserProfile:
    """
    Converts the structured analysis from the LLM into a gamified UserProfile.
    """

    profile_skills = []

    if analysis.skills:
        for category, skills_list in analysis.skills.items():
            for skill_name in skills_list:
                profile_skills.append(Skill(name=skill_name, category=category))

    user_profile = UserProfile(
        user_name=getattr(analysis, 'user_name', 'User'),
        job_title=getattr(analysis, 'job_title', 'Aspiring Professional'),
        main_rank=analysis.suggested_rank,
        level=analysis.suggested_level,
        xp=0,
        skills=profile_skills
    )

    return user_profile