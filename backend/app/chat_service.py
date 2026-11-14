import os
import json
from pathlib import Path

from groq import Groq
from dotenv import load_dotenv

from app.prompts import SYSTEM_PROMPT

load_dotenv()

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=api_key)

MODEL = "qwen/qwen3.8-27b"


def load_candidate_profile():

    backend_dir = Path(__file__).resolve().parent.parent
    candidate_path = backend_dir / "data" / "candidate.json"

    if not candidate_path.exists():
        raise FileNotFoundError(
            f"Candidate profile not found: {candidate_path}"
        )

    with open(candidate_path, "r", encoding="utf-8") as file:
        candidate = json.load(file)

    return candidate


def chat_with_candidate(question: str):

    candidate = load_candidate_profile()

    messages = [
        {
            "role": "system",
            "content": (
                SYSTEM_PROMPT
                + "\n\nCANDIDATE PROFILE:\n"
                + json.dumps(candidate, indent=4)
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3,
        max_tokens=1000
    )

    answer = response.choices[0].message.content

    return answer
