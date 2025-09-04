# career_forge/gamification/profile_generator.py

from career_forge.schemas.user import UserProfile, Skill
from career_forge.engine.feature_extractor import ExtractedFeatures


def generate_profile_from_features(features: ExtractedFeatures) -> UserProfile:
    """
    Converts extracted resume features into a gamified UserProfile.
    This function contains the initial logic for assigning ranks and levels.
    """

    profile_skills = []
    total_skill_count = 0

    # Convert the dictionary of skills from the extractor into a list of Skill objects
    for category, skills_list in features.skills.items():
        for skill_name in skills_list:
            profile_skills.append(Skill(name=skill_name, category=category))
        total_skill_count += len(skills_list)

    # --- MVP Ranking Logic ---
    # This is a simple, rule-based system for assigning the initial rank.
    # It can be made much more sophisticated later.
    main_rank = "E"
    if total_skill_count > 30:
        main_rank = "C"
    elif total_skill_count > 15:
        main_rank = "D"

    # Create the final UserProfile object
    user_profile = UserProfile(
        main_rank=main_rank,
        level=1,
        xp=0,
        skills=profile_skills
    )

    return user_profile