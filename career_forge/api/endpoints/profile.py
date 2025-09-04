# career_forge/api/endpoints/profile.py

from fastapi import APIRouter, UploadFile, File, HTTPException

# Import our AI engine components
from career_forge.engine.parser import parse_resume
from career_forge.engine.feature_extractor import extract_features

# Import our gamification components
from career_forge.gamification.profile_generator import generate_profile_from_features
from career_forge.gamification.quest_generator import generate_initial_quests

# Import our final response model
from career_forge.schemas.analysis import AnalysisResult

router = APIRouter()


@router.post("/hackrx/run", response_model=AnalysisResult)  # <-- Use the final response model
async def run_resume_analysis(file: UploadFile = File(...)):
    """
    This is the main endpoint for the AI engine.

    It accepts a resume file, orchestrates the parsing, feature extraction,
    profile generation, and quest generation, returning a combined result.
    """
    if file.content_type not in [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Please upload a PDF or DOCX."
        )

    file_content = await file.read()

    try:
        # Step 1: Parse the resume
        parsed_resume = parse_resume(file_content, file.content_type)
        if not parsed_resume.raw_text:
            raise HTTPException(status_code=422, detail="Failed to extract text from the document.")

        # Step 2: Extract features with the AI engine
        features = extract_features(parsed_resume)

        # Step 3: Generate the gamified profile from the features
        user_profile = generate_profile_from_features(features)

        # Step 4 (NEW): Generate initial quests based on the new profile
        quests = generate_initial_quests(user_profile)

        # Step 5 (NEW): Combine into the final result object
        analysis_result = AnalysisResult(profile=user_profile, quests=quests)

        return analysis_result

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred during analysis.")