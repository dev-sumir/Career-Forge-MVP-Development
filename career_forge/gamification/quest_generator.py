# career_forge/gamification/quest_generator.py

import random
from typing import List
from career_forge.schemas.user import UserProfile
from career_forge.schemas.quest import Quest

# Quest templates make it easy to generate a variety of tasks.
QUEST_TEMPLATES = {
    "technical": [
        {
            "title": "Foundations of {skill_name}",
            "description": "Read a high-level overview article or watch a 10-minute introduction video about {skill_name} to understand its core concepts.",
        },
        {
            "title": "Beginner's Tutorial: {skill_name}",
            "description": "Find and complete a 'Hello, World!' or beginner-level tutorial for {skill_name}. The goal is hands-on practice.",
        },
    ],
    "soft_skill": [
        {
            "title": "Self-Assess: {skill_name}",
            "description": "Write down two examples of when you successfully used {skill_name} in a project or team setting. Reflect on what went well.",
        }
    ]
}


def generate_initial_quests(profile: UserProfile) -> List[Quest]:
    """
    Generates a list of starter quests based on the user's profile.

    For the MVP, it selects a few identified skills and creates quests for them.
    """
    generated_quests = []

    # Separate skills into technical and soft skills for different quest types
    technical_skills = [s for s in profile.skills if s.category != "SOFT_SKILL"]
    soft_skills = [s for s in profile.skills if s.category == "SOFT_SKILL"]

    # Generate 2 technical quests if possible
    if len(technical_skills) > 0:
        # random.sample ensures we don't pick the same skill twice
        skills_to_feature = random.sample(technical_skills, k=min(len(technical_skills), 2))
        for skill in skills_to_feature:
            template = random.choice(QUEST_TEMPLATES["technical"])
            quest = Quest(
                title=template["title"].format(skill_name=skill.name),
                description=template["description"].format(skill_name=skill.name),
                category=skill.category,
                rewards=[f"+50 XP ({skill.name})"]
            )
            generated_quests.append(quest)

    # Generate 1 soft skill quest if possible
    if len(soft_skills) > 0:
        skill = random.choice(soft_skills)
        template = random.choice(QUEST_TEMPLATES["soft_skill"])
        quest = Quest(
            title=template["title"].format(skill_name=skill.name),
            description=template["description"].format(skill_name=skill.name),
            category=skill.category,
            rewards=[f"+50 XP ({skill.name})"]
        )
        generated_quests.append(quest)

    return generated_quests