from pydantic import BaseModel
from typing import List, Optional

class StudentProfile(BaseModel):
    degree: str
    semester: int
    cgpa: float
    financial_need: str
    location_pref: str
    skills: str
    preferred_types: str
    experience: str

class Opportunity(BaseModel):
    rank: int
    title: str
    type: str
    organization: str
    deadline: str
    deadline_days: int
    urgency: str
    benefits: str
    requirements: List[str]
    apply_link: str
    eligibility_note: str
    eligible: bool
    fit_score: float
    urgency_score: float
    value_score: float
    overall_score: float
    reasoning: str
    action_checklist: List[str]

class NotOpportunity(BaseModel):
    subject: str
    reason: str

class AnalyzeRequest(BaseModel):
    emails_text: str
    profile: StudentProfile

class AnalyzeResponse(BaseModel):
    opportunities: List[Opportunity]
    not_opportunities: List[NotOpportunity]
    summary: str