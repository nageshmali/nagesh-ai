from pydantic import BaseModel, Field

class PersonalInfo(BaseModel):
    full_name:str = Field(description="Candidate's full name")
    email:str| None = None
    phone:str| None = None
    location:str| None = None
    linkedin_url:str| None = None
    github_url:str| None = None
    portfolio_url:str| None = None

class Education(BaseModel):
    degree:str = Field(description="Candidate's degree")
    specialization:str| None = None
    institution:str = Field(description="Name of the educational institution")
    start_year:int| None = None
    graduation_year:int| None = None
    grade:str| None = None

class Skills(BaseModel):
    programming_languages:list[str] = Field(default_factory=list) 
    frameworks:list[str] = Field(default_factory=list)
    libraries: list[str] = Field(default_factory=list)
    databases:list[str] = Field(default_factory=list)
    tools_and_platforms:list[str] = Field(default_factory=list)
    core_concepts:list[str] =Field(default_factory=list)

class Experience(BaseModel):
    company:str| None = None
    role:str| None = None
    location: str | None = None
    employment_type:str| None = None
    is_current:bool| None = None
    responsibilities:list[str]=Field(default_factory=list)

class Project(BaseModel):
    title: str
    description: str
    technologies: list[str] = Field(default_factory=list)
    key_features: list[str] = Field(default_factory=list)
    github_url: str | None = None
    live_url: str | None = None

class CandidateProfile(BaseModel):
    personal_info:PersonalInfo
    education: list[Education] = Field(default_factory=list)
    skills: Skills
    experience: list[Experience] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)