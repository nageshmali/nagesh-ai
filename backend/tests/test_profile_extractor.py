
from pathlib import Path

from app.extractor import extract_resume_text
from app.profile_extractor import extract_candidate_profile


def main():
    # Step 1: Extract text from resume PDF
    resume_path = Path("app/resume.pdf")
    resume_text = extract_resume_text(str(resume_path))

    # Step 2: Extract structured candidate profile using LLM
    profile = extract_candidate_profile(resume_text)

    # Step 3: Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

    # Step 4: Save candidate profile as JSON
    candidate_path = data_dir / "candidate.json"

    candidate_path.write_text(
        profile.model_dump_json(indent=4),
        encoding="utf-8"
    )

    print(f"Candidate profile saved successfully: {candidate_path.resolve()}")


if __name__ == "__main__":
    main()
