from app.requirement_extractor import extract_job_requirements
from app.candidate_evaluator import evaluate_candidate
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.chat_service import chat_with_candidate
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="NageshAI",
    description="An AI assistant representing Nagesh professionally",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    question: str
    history: list[ChatMessage] = Field(default_factory=list)

class JobMatchRequest(BaseModel):
    job_description: str


@app.get("/")
def home():
    return {
        "message": "Welcome to NageshAI!",
        "status": "running"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    history = [
        message.model_dump()
        for message in request.history
    ]

    answer = chat_with_candidate(
        question=request.question,
        history=history
    )

    return {
        "answer": answer
    }


@app.post("/match-job")
def match_job(request: JobMatchRequest):

    requirements = extract_job_requirements(
        request.job_description
    )

    result = evaluate_candidate(requirements)

    return result