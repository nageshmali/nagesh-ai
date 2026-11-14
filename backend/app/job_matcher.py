import os
import json

from groq import Groq
from dotenv import load_dotenv

from app.models import JobMatchResult
from app.chat_service import load_candidate_profile

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=api_key)

MODEL = "qwen/qwen3.8-27b"


def evaluate_job_match(job_description: str) -> JobMatchResult:

    candidate = load_candidate_profile()

    schema = JobMatchResult.model_json_schema()

    prompt = f"""
    You are an expert technical recruiter.

    Evaluate the candidate against the supplied job description.

    CANDIDATE PROFILE:
    {json.dumps(candidate, indent=4)}

    JOB DESCRIPTION:
    {job_description}

    EVALUATION RULES:

    1. Evaluate every important requirement in the job description.
    2. Use only evidence available in the candidate profile.
    3. Demonstrated means there is clear supporting evidence.
    4. Partially Demonstrated means there is related or incomplete evidence.
    5. Not Evident in Profile means the profile does not establish the requirement.
    6. Never assume that an unlisted skill is a skill the candidate does not possess.
    7. Distinguish mandatory requirements from preferred requirements.
    8. Evaluate education, experience, and years of experience when relevant.
    9. Do not invent experience, skills, or qualifications.
    10. Provide a balanced and evidence-based recommendation.
    11. Do not calculate an arbitrary match percentage.
    12. Never attribute technologies to projects unless explicitly mentioned in that project's description or technologies.
    13. Distinguish between skills listed in the candidate's skills section and skills demonstrated through projects.
    14. Do not claim that a candidate has professional experience unless it is explicitly present in the experience section.
    15. Do not describe a graduate as a current student if their graduation year has already passed.
    16. A skill listed in the skills section is evidence of claimed knowledge, but not necessarily practical experience.
    17. Never infer hands-on experience from a technology merely appearing in a related project.
    18. Use the exact graduation status and graduation year provided in the candidate profile.
    19. Never describe a completed degree as currently ongoing.
    20. Never describe a completed graduation year as an expected graduation year.
    21. When evaluating education requirements, compare the actual degree and specialization against the job requirements.

    Return JSON strictly following this schema:

    {json.dumps(schema, indent=4)}


    ###important
    M.Tech status: COMPLETED IN 2026
    Python project attribution KEEP ONLY IN THOSE PROJECTS WHERE ACTUALLY PYTHON IS USED DONT ATTRIBUTE IT TO ALL PROJECTS
    Treats GitHub project URLs as evidence of version-control usage - DONT DO IT
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an accurate job matching assistant. "
                    "Return only valid JSON following the supplied schema."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"},
        temperature=0,
        max_tokens=3000
    )

    response_text = response.choices[0].message.content

    result = JobMatchResult.model_validate_json(response_text)

    return result
