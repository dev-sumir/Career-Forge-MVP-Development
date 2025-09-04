# career_forge/api/endpoints/profile.py

from fastapi import APIRouter, UploadFile, File, HTTPException

from career_forge.engine.parser import parse_resume
from career_forge.engine.llm_analyzer import analyze_resume_with_llm

from career_forge.gamification.profile_generator import generate_profile_from_llm_analysis
from career_forge.gamification.quest_generator import generate_quests_with_llm

from career_forge.schemas.analysis import AnalysisResult

router = APIRouter()


@router.post("/hackrx/run", response_model=AnalysisResult)
async def run_resume_analysis(file: UploadFile = File(...)):
    """
    This is the main endpoint for the LLM-powered AI engine.
    It orchestrates the full analysis workflow.
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
        parsed_resume = parse_resume(file_content, file.content_type)
        if not parsed_resume.raw_text:
            raise HTTPException(status_code=422, detail="Failed to extract text from the document.")

        llm_analysis = analyze_resume_with_llm(parsed_resume.raw_text)
        if not llm_analysis:
            raise HTTPException(status_code=500, detail="Failed to get a valid analysis from the LLM.")

        user_profile = generate_profile_from_llm_analysis(llm_analysis)

        quests = generate_quests_with_llm(llm_analysis)

        # --- KEY CHANGE IS HERE ---
        # We now include the experiences list in the final result.
        analysis_result = AnalysisResult(
            profile=user_profile,
            quests=quests,
            experiences=llm_analysis.experiences
        )

        return analysis_result

    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during analysis: {e}")