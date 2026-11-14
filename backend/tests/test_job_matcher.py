
from app.requirement_extractor import extract_job_requirements
from app.candidate_evaluator import evaluate_candidate


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


def main():

    # Stage 1: Extract structured requirements from the JD
    print("\n========== STAGE 1: REQUIREMENT EXTRACTION ==========\n")

    requirements = extract_job_requirements(job_description)

    print("Role:", requirements.role_title)
    print("\nExtracted Requirements:")

    for req in requirements.requirements:
        print(
            f"- {req.description} | "
            f"Category: {req.category} | "
            f"Importance: {req.importance}"
        )

    # Stage 2: Evaluate candidate against extracted requirements
    print("\n========== STAGE 2: CANDIDATE EVALUATION ==========\n")

    result = evaluate_candidate(requirements)

    print("Role:", result.role_title)
    print("Overall Assessment:", result.overall_assessment)
    print("Technical Assessment:", result.technical_assessment)
    print("Eligibility Assessment:", result.eligibility_assessment)

    print("\nSummary:")
    print(result.summary)

    print("\nMatched Requirements:")

    for item in result.matched_requirements:
        print(f"\nRequirement: {item.requirement}")
        print(f"Category: {item.category}")
        print(f"Importance: {item.importance}")
        print(f"Status: {item.status}")
        print(f"Evidence: {item.evidence}")

    print("\nGaps or Unverified Requirements:")

    for item in result.gaps_or_unverified_requirements:
        print(f"\nRequirement: {item.requirement}")
        print(f"Category: {item.category}")
        print(f"Importance: {item.importance}")
        print(f"Status: {item.status}")
        print(f"Evidence: {item.evidence}")

    print("\nRecommendation:")
    print(result.recommendation)


if __name__ == "__main__":
    main()
