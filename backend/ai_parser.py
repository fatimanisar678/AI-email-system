import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def parse_emails(emails_text: str, profile) -> dict:
    prompt = f"""You are an AI opportunity analyst for university students. Today is April 18, 2026.

STUDENT PROFILE:
- Degree: {profile.degree}
- Semester: {profile.semester}
- CGPA: {profile.cgpa}
- Financial Need: {profile.financial_need}
- Location Preference: {profile.location_pref}
- Skills: {profile.skills}
- Preferred Types: {profile.preferred_types}
- Experience: {profile.experience}

EMAILS (each separated by ---):
{emails_text}

YOUR TASKS:
1. Classify each email: is it a real opportunity or not?
2. For each real opportunity, extract all structured fields
3. Give a raw fit_score based on profile match

Return ONLY valid JSON, no markdown, no backticks, no explanation:
{{
  "opportunities": [
    {{
      "title": "short name of opportunity",
      "type": "Scholarship|Internship|Competition|Fellowship|Other",
      "organization": "organization name",
      "deadline": "human readable deadline",
      "deadline_days": <integer days from April 18 2026, use 999 if unknown>,
      "urgency": "URGENT|SOON|NORMAL",
      "benefits": "what student receives - stipend, prize, etc",
      "requirements": ["document1", "document2", "document3"],
      "apply_link": "URL or email or Not provided",
      "eligibility_note": "one sentence on eligibility for this student",
      "eligible": true or false,
      "fit_score": <0 to 100 based on skills/cgpa/semester/location match>,
      "reasoning": "2 sentences: why ranked here and how it fits this specific student",
      "action_checklist": ["Step 1: ...", "Step 2: ...", "Step 3: ...", "Step 4: ..."]
    }}
  ],
  "not_opportunities": [
    {{
      "subject": "email subject line",
      "reason": "why this is not an opportunity"
    }}
  ],
  "summary": "2 sentence personalized summary for this student about their inbox"
}}

RULES:
- URGENT = deadline within 7 days from today
- SOON = deadline 8 to 30 days from today  
- NORMAL = deadline 30+ days or rolling
- fit_score: check CGPA meets threshold, semester in range, skills match, location matches preference, financial need aligns
- eligible = false if CGPA is below stated requirement or student does not meet stated criteria
- Be strict and honest about eligibility"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)