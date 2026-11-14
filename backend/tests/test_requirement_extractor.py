
from app.requirement_extractor import extract_job_requirements


job_description = """
We are looking for a Python Developer.

Mandatory Requirements:
- Strong knowledge of Python.
- Experience building REST APIs.
- Bachelor's degree in Computer Science or equivalent.
- Minimum 2 years of software development experience.

Preferred Requirements:
- Experience with FastAPI or Flask.
- Basic knowledge of Machine Learning.
- Experience with Docker and Git.
- Master's degree in Computer Science is preferred.
"""


result = extract_job_requirements(job_description)

print("\n========== EXTRACTED JOB REQUIREMENTS ==========\n")

print("Role:", result.role_title)

print("\nRole Summary:")
print(result.role_summary)

print("\nRequirements:")

for requirement in result.requirements:

    print(f"\nRequirement: {requirement.description}")
    print(f"Category: {requirement.category}")
    print(f"Importance: {requirement.importance}")
