
import os
import json

from groq import Groq
from dotenv import load_dotenv

from app.models import JobRequirements

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=api_key)

MODEL = "qwen/qwen3.8-27b"


def extract_job_requirements(job_description: str) -> JobRequirements:

    schema = JobRequirements.model_json_schema()

    prompt = f"""
    You are an expert job description analysis assistant.

    Your task is to extract structured requirements from the
    supplied job description.

    JOB DESCRIPTION:
    {job_description}

    EXTRACTION RULES:

    1. Extract the job title if available.
    2. Write a concise summary of the role.
    3. Identify individual skills, education, experience,
       certification, and other requirements.
    4. Classify each requirement into its appropriate category.
    5. Identify whether each requirement is mandatory,
       preferred, or unspecified.
    6. Only classify a requirement as mandatory when the
       job description explicitly makes it mandatory.
    7. Words such as "must", "required", and "essential"
       generally indicate mandatory requirements.
    8. Words such as "preferred", "nice to have", and
       "beneficial" generally indicate preferred requirements.
    9. If importance is unclear, use "unspecified".
    10. Do not invent requirements that are not in the
        supplied job description.
    11. Keep different requirements separate.
    12. Do not evaluate or recommend any candidate.
    13. When a requirement mentions multiple independent
        skills, technologies, tools, or qualifications,
        extract each as a separate requirement.

        Example:
        "Experience with Docker and Git"

        Should become:
        - Experience with Docker
        - Experience with Git

    14. Do not combine independent requirements into
        one requirement merely because they appear in
        the same bullet point.

    
    15. Classify a requirement as "skill" when it describes
        a technical ability, technology, tool, or practical
        capability, even if it uses the phrase "experience with"
        or "experience building".

    16. Classify a requirement as "experience" when it explicitly
        specifies professional work experience, employment,
        years of experience, or a required duration of experience.

    Examples:
    - "Experience building REST APIs" -> skill
    - "Experience with Docker" -> skill
    - "Minimum 2 years of software development experience" -> experience
    - "3 years of professional Python development" -> experience


    Return JSON strictly following this schema:

    {json.dumps(schema, indent=4)}
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract job requirements accurately. "
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
        max_tokens=800
    )

    response_text = response.choices[0].message.content

    requirements = JobRequirements.model_validate_json(
        response_text
    )

    return requirements
