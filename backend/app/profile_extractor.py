
import os
from groq import Groq
from dotenv import load_dotenv

from app.models import CandidateProfile

load_dotenv()

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=api_key)

MODEL = "qwen/qwen3.8-27b"


def extract_candidate_profile(resume_text: str) -> CandidateProfile:

    schema = CandidateProfile.model_json_schema()

    prompt = f"""
    You are an accurate resume information extraction assistant.

    Your task is to extract structured information from Nagesh Mali's resume.

    Follow every instruction carefully.

    GENERAL RULES:
    1. Extract all relevant information from the entire resume.
    2. Never invent or assume information.
    3. Use null for unavailable optional values.
    4. Use empty lists when no information is available for a list field.
    5. Follow the supplied Pydantic JSON schema strictly.
    6. Preserve important technical details, metrics, and project descriptions.
    7. Do not confuse academic projects with professional employment.
    8. Do not create additional fields outside the schema.

    PERSONAL INFORMATION:
    - Full name: Nagesh Mali
    - Location: Chennai, India
    - LinkedIn: https://www.linkedin.com/in/nagesh-mali/
    - GitHub: https://github.com/nageshmali
    - Portfolio URL: null unless explicitly available in the resume.
    - Extract email and phone from the resume without modification.
    - Use the verified location above instead of inferring location from educational institutions.

    EDUCATION:
    Extract exactly four education entries:

    1. M.Tech in Computer Science and Engineering
    Institution: Vellore Institute of Technology
    Start year: 2024
    Graduation year: 2026
    Grade: 9.31

    2. B.Tech in Computer Science and Engineering
    Institution: N.K. Orchid College of Engineering
    Start year: 2020
    Graduation year: 2024
    Grade: 8.71

    3. Higher Secondary
    Institution: Sinhgad Public School
    Graduation year: 2020
    Grade: 76.40%

    4. Secondary
    Institution: S.R. Chandak English Highschool
    Graduation year: 2018
    Grade: 88.20%

    For school education, use null for start_year if it is not explicitly stated.

    TECHNICAL SKILLS:

    Extract skills into the following categories:

    - programming_languages
    - frameworks
    - libraries
    - databases
    - tools_and_platforms
    - core_concepts

    Categorization rules:
    1. Programming languages: Python, C++, JavaScript, etc.
    2. Frameworks: React.js, Flask, Node.js, Express, Streamlit, etc.
    3. Libraries: NumPy, Pandas, LangChain, FAISS, Axios, Puppeteer, Cheerio, etc.
    4. Databases: MySQL, MongoDB, etc.
    5. Tools and platforms: Git, GitHub, Linux, AWS, APIs, cloud platforms, etc.
    6. Core concepts: Machine Learning, AI, NLP, RAG, REST APIs, SDLC, SOLID, etc.
    7. HTML and CSS should be treated as web technologies.
    8. Do not classify datasets as tools or technologies.
    9. Avoid duplicate skills.
    10. Include relevant technical skills explicitly mentioned in project descriptions and coursework.

    EXPERIENCE:
    - Extract only actual employment or internship experience.
    - Do not classify academic projects, coursework, or independent projects as employment.
    - If no professional experience is mentioned, return an empty list.

    PROJECTS:

    Extract exactly three projects.

    1. AI Legal Document Summarizer
    Technologies include Python, Flask, LangChain, Google Gemini API, and FAISS.

    2. QuantumRecSys - Hybrid Quantum-Classical Movie Recommendation System
    Technologies include Python, Variational QPCA, TF-IDF, Streamlit, IBM Kingston processor, TMDB API, and MovieLens 1M.

    3. AI-Powered Article Scraper & Enhancer
    Technologies include ReactJS, Groq LLM API, MongoDB, Node.js, Express, Puppeteer, Cheerio, Mongoose, Tailwind CSS, and Axios.

    For every project:
    - Extract its description accurately.
    - Preserve important implementation details and measurable results.
    - Extract key features as individual list items.
    - Extract technologies used.
    - Populate GitHub and live URLs only when actual project-specific URLs are explicitly available.
    - Never reuse the personal GitHub profile URL as a project URL.
    - Do not invent missing implementation details.

    COURSES:
    - Extract relevant courses only if the supplied schema supports them.
    - Do not add unsupported fields.

    ACHIEVEMENTS AND CERTIFICATIONS:
    - Extract only explicitly mentioned achievements and certifications.
    - Do not classify ordinary coursework as certifications.
    - Return empty lists if none are mentioned.

    INTERESTS:
    - Extract interests only if the supplied schema supports them.
    - Do not add unsupported fields.

    FINAL VALIDATION:
    Before generating the response, verify:
    1. Personal information is accurate.
    2. Exactly four education entries are present.
    3. Technical skills are categorized correctly.
    4. No academic project is classified as employment.
    5. Exactly three projects are present.
    6. Project descriptions and technologies are preserved.
    7. No URLs have been invented.
    8. Achievements and certifications are not fabricated.
    9. Output follows the supplied schema.

    VERIFIED PROJECT URLS:

    1. AI Legal Document Summarizer
       GitHub: https://github.com/nageshmali/
       Live URL: null

    2. QuantumRecSys - Hybrid Quantum-Classical Movie Recommendation System
       GitHub: https://github.com/nageshmali/hybrid-recsys
       Live URL: https://hybrid-recsys.streamlit.app/

    3. AI-Powered Article Scraper & Enhancer
       GitHub: https://github.com/nageshmali/ScrapeAndEnhance
       Live URL: null

    IMPORTANT:
    - Use these verified URLs for their corresponding projects.
    - Never interchange URLs between projects.
    - Do not invent additional URLs.

    PYDANTIC JSON SCHEMA:
    {schema}

    RESUME TEXT:
    {resume_text}

    Return only valid JSON. Do not include Markdown or explanations.
    """

    messages = [
        {
            "role": "system",
            "content": (
                "You are an accurate resume information extraction assistant. "
                "Return only valid JSON following the supplied schema."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0,
        max_tokens=4000
    )

    response_text = response.choices[0].message.content

    profile = CandidateProfile.model_validate_json(response_text)

    return profile
