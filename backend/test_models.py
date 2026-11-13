from app.models import PersonalInfo, Education, Skills, Project, CandidateProfile

# # Testing PersonalInfo
# person = PersonalInfo(
#     full_name="Nagesh Mali",
#     email="nagesh@example.com",
#     location="India"
# )

# print("PERSONAL INFORMATION:")
# print(person)
# print(person.model_dump())

# # Testing Education
# education = Education(
#     degree="M.Tech",
#     specialization="Computer Science and Engineering",
#     institution="VIT Vellore",
#     start_year=2024,
#     graduation_year=2026,
#     grade="6th Rank in Merit List"
# )

# print("\nEDUCATION:")
# print(education)
# print(education.model_dump())


# skills = Skills(
#     programming_languages=["Python", "C++", "Java"],
#     frameworks=["FastAPI", "React", "LangChain"]
# )

# print(skills)
# print(skills.model_dump())


# legal_summarizer = Project(
#     title="AI Legal Summarizer",
#     description="An AI-powered application that summarizes legal documents using LLMs and RAG.",
#     technologies=[
#         "Python",
#         "Flask",
#         "LangChain",
#         "Gemini",
#         "FAISS",
#         "SQLite"
#     ],
#     key_features=[
#         "PDF and DOCX document processing",
#         "Semantic search using FAISS",
#         "Executive, Standard, and Detailed summaries"
#     ],
#     github_url=None,
#     live_url=None
# )

# print(legal_summarizer.model_dump())


profile = CandidateProfile(
    personal_info=PersonalInfo(
        full_name="Nagesh Mali",
        email="nagesh@example.com"
    ),
    education=[
        Education(
            degree="M.Tech",
            institution="VIT Vellore"
        )
    ],
    skills=Skills(),
    projects=[
        Project(
            title="Project1",
            description="A demo project"
        )
    ]
)

print(profile.model_dump_json(indent=4))