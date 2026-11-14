import os
import json

from groq import Groq
from dotenv import load_dotenv

from app.models import JobRequirements, JobMatchResult
from app.chat_service import load_candidate_profile

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=api_key)

MODEL = "qwen/qwen3.8-27b"

def evaluate_candidate(requirements: JobRequirements) -> JobMatchResult:

    if not requirements.requirements:
        raise ValueError("No job requirements were provided")

    candidate = load_candidate_profile()

    schema = JobMatchResult.model_json_schema()

    prompt = f"""
    You are an expert technical recruiter evaluating a candidate
    against structured job requirements.

    CANDIDATE PROFILE:
    {json.dumps(candidate, indent=4)}

    JOB REQUIREMENTS:
    {requirements.model_dump_json(indent=4)}

    YOUR TASK:
    Evaluate how well the candidate satisfies each job requirement.

    EVALUATION RULES:

    1. Evaluate every supplied requirement individually.

    2. Preserve the original requirement description, category,
       and importance exactly as provided.

    3. Use only evidence available in the candidate profile.

    4. A skill listed in the candidate's skills section indicates
       claimed knowledge of that skill.

    5. A technology used in a project provides practical
       project-based evidence.

    6. Do not assume professional work experience from academic
       projects.

    7. Do not treat a GitHub profile or repository link alone
       as proof of a particular technical skill.

    8. For education requirements, compare the actual degree,
       specialization, institution, and graduation year.

    9. For experience requirements, verify the required duration
       or type of experience. Do not assume duration from projects.
        9.1. Interpret graduation years using the current date.
         The current date is November 2026.

         If graduation_year is 2026 or earlier, treat the degree
         as completed unless the profile explicitly says otherwise.

         Do not describe a completed degree as currently pursuing.

    10. Use "Demonstrated" when sufficient evidence is available.

    11. Use "Partially Demonstrated" when some relevant evidence
        exists but does not fully satisfy the requirement.

    12. Use "Not Evident in Profile" when the profile does not
        contain supporting evidence.

    13. Do not interpret missing information as proof that the
        candidate lacks a skill or qualification.

    14. Place fully demonstrated requirements in
        matched_requirements.

    15. Place partially demonstrated and not evident requirements
        in gaps_or_unverified_requirements.

        16. TECHNICAL ASSESSMENT:
        Evaluate the candidate's technical suitability based on
        demonstrated skills, project implementation, and relevant
        technical knowledge.

        Use:
        - Strong: Most important technical requirements are demonstrated.
        - Moderate: Some important technical requirements are demonstrated.
        - Weak: Most important technical requirements are not demonstrated.
        - Insufficient Information: There is not enough evidence to evaluate.

    
    17. ELIGIBILITY ASSESSMENT:
        Evaluate only mandatory eligibility requirements.

        Use the following rules strictly:

        - Meets Requirements:
          All mandatory requirements are supported by sufficient
          evidence in the candidate profile.

        - Does Not Meet Requirements:
          The candidate profile contains explicit evidence that
          the candidate fails at least one mandatory requirement.
          Example: The job requires 2 years of experience, but
          the profile explicitly documents only 1 year.

        - Needs Verification:
          One or more mandatory requirements cannot be confirmed
          because the profile does not contain sufficient information.

        IMPORTANT:
        - Missing information is NOT proof that a requirement
          is not satisfied.
        - An empty experience list means professional experience
          is not documented. It does not prove zero experience.
        - Never infer that a candidate lacks experience simply
          because no employment is listed.
        - Never infer that a candidate is ineligible based only
          on missing evidence.
        - If evidence is insufficient, use Needs Verification.


    18. A missing preferred requirement must not cause the candidate
        to fail eligibility.

    19. Overall Assessment:
        Determine overall_assessment using both technical suitability
        and eligibility.

        A candidate with strong technical skills but an unmet mandatory
        eligibility requirement should not be classified as a Strong Match.

        Do not invent a match percentage.

    20. Provide a practical recommendation that considers both
        technical suitability and mandatory eligibility.

    Return valid JSON following this schema:
    {json.dumps(schema, indent=4)}
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict, fair and evidence-based "
                    "candidate evaluation assistant. "
                    "Return only valid JSON following the schema."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"},
        temperature=0,
        max_tokens=3500
    )

    response_text = response.choices[0].message.content

    result = JobMatchResult.model_validate_json(response_text)

    return result