import json
import os
import re
from datetime import date, datetime
from typing import Any, Dict, List, Tuple

from dotenv import load_dotenv

load_dotenv()

TODAY = date(2026, 4, 18)


def _build_prompt(emails_text: str, profile) -> str:
    return f"""You are an AI opportunity analyst for university students. Today is April 18, 2026.

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


def _clean_json(text: str) -> str:
    return text.replace("```json", "").replace("```", "").strip()


def _clamp(n: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, n))


def _parse_deadline_days(deadline_str: str) -> int:
    if not deadline_str:
        return 999
    s = deadline_str.strip()
    if s.lower() in {"rolling", "rolling basis", "open", "open until filled"}:
        return 999
    for fmt in ("%B %d, %Y", "%b %d, %Y", "%B %d %Y", "%b %d %Y"):
        try:
            dt = datetime.strptime(s, fmt).date()
            return (dt - TODAY).days
        except Exception:
            pass
    return 999


def _infer_urgency(deadline_days: int) -> str:
    if deadline_days != 999 and deadline_days <= 7:
        return "URGENT"
    if deadline_days != 999 and deadline_days <= 30:
        return "SOON"
    return "NORMAL"


def _split_emails(emails_text: str) -> List[str]:
    parts = [p.strip() for p in emails_text.split("---")]
    return [p for p in parts if p]


def _extract_subject(email_text: str) -> str:
    m = re.search(r"^Subject:\s*(.+)$", email_text, flags=re.IGNORECASE | re.MULTILINE)
    return (m.group(1).strip() if m else "Unknown")


def _extract_from_line(prefixes: Tuple[str, ...], email_text: str) -> str:
    for p in prefixes:
        m = re.search(rf"^{re.escape(p)}\s*(.+)$", email_text, flags=re.IGNORECASE | re.MULTILINE)
        if m:
            return m.group(1).strip()
    return ""


def _mock_parse(emails_text: str, profile) -> Dict[str, Any]:
    opportunities: List[Dict[str, Any]] = []
    not_opportunities: List[Dict[str, Any]] = []

    for em in _split_emails(emails_text):
        subject = _extract_subject(em)
        lower = em.lower()

        is_opp = any(k in lower for k in ["scholarship", "internship", "fellowship", "competition", "hackathon", "apply", "deadline"])
        is_noise = any(k in lower for k in ["pizza", "book return", "library hours", "reminder: return", "fine of"])

        if (not is_opp) or is_noise:
            not_opportunities.append({"subject": subject, "reason": "Looks like an event/reminder/announcement, not an application opportunity."})
            continue

        deadline = _extract_from_line(("Deadline:", "Application Deadline:", "Registration Deadline:"), em)
        if not deadline:
            deadline = "Rolling / Unknown"
        deadline_days = _parse_deadline_days(deadline)

        apply_link = _extract_from_line(("Apply at:", "Register at:"), em)
        if not apply_link:
            m = re.search(r"(https?://\S+|www\.\S+)", em, flags=re.IGNORECASE)
            apply_link = m.group(1) if m else "Not provided"

        org = _extract_from_line(("From:",), em)
        opp_type = "Other"
        if "scholarship" in lower:
            opp_type = "Scholarship"
        elif "internship" in lower:
            opp_type = "Internship"
        elif "fellowship" in lower:
            opp_type = "Fellowship"
        elif "competition" in lower or "hackathon" in lower:
            opp_type = "Competition"

        benefits = _extract_from_line(("Benefits:", "Award:", "Stipend:", "Prizes:"), em) or "See email"
        requirements_line = _extract_from_line(("Required Documents:", "Requirements:"), em)
        requirements = [r.strip() for r in re.split(r",|·|;|\n", requirements_line) if r.strip()] if requirements_line else []

        # crude eligibility/fit heuristic
        fit = 55.0
        if any(s.strip().lower() in lower for s in (profile.skills or "").split(",")):
            fit += 10
        if profile.location_pref and profile.location_pref.lower() != "any" and profile.location_pref.lower() in lower:
            fit += 5

        opportunities.append({
            "title": subject,
            "type": opp_type,
            "organization": org,
            "deadline": deadline,
            "deadline_days": deadline_days,
            "urgency": _infer_urgency(deadline_days),
            "benefits": benefits,
            "requirements": requirements,
            "apply_link": apply_link,
            "eligibility_note": "Auto-extracted locally (no API key set). Verify eligibility in the email.",
            "eligible": True,
            "fit_score": round(_clamp(fit, 0, 100), 1),
            "reasoning": "Ranked using deterministic scoring with a lightweight local extractor. Add an LLM key for deeper parsing.",
            "action_checklist": [
                "Open the email and confirm eligibility criteria",
                "Collect required documents (if any)",
                "Open the apply link / contact address",
                "Submit before the deadline",
            ],
        })

    summary = f"Found {len(opportunities)} likely opportunities and filtered {len(not_opportunities)} non-opportunity emails."
    return {"opportunities": opportunities, "not_opportunities": not_opportunities, "summary": summary}


def _parse_with_claude(prompt: str) -> Dict[str, Any]:
    import anthropic

    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing ANTHROPIC_API_KEY")

    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model=model,
        max_tokens=int(os.getenv("ANTHROPIC_MAX_TOKENS", "4000")),
        messages=[{"role": "user", "content": prompt}],
    )
    raw = message.content[0].text
    return json.loads(_clean_json(raw))


def _parse_with_gemini(prompt: str) -> Dict[str, Any]:
    import google.generativeai as genai

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY")

    genai.configure(api_key=api_key)
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    model = genai.GenerativeModel(model_name)

    resp = model.generate_content(
        prompt,
        generation_config={
            "temperature": float(os.getenv("GEMINI_TEMPERATURE", "0.2")),
        },
    )
    text = getattr(resp, "text", "") or ""
    return json.loads(_clean_json(text))


def parse_emails(emails_text: str, profile) -> dict:
    provider = (os.getenv("LLM_PROVIDER") or "").strip().lower()
    prompt = _build_prompt(emails_text, profile)

    if provider in {"claude", "anthropic"}:
        return _parse_with_claude(prompt)
    if provider in {"gemini", "google"}:
        return _parse_with_gemini(prompt)

    # Auto-pick if user didn't set provider
    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            return _parse_with_claude(prompt)
        except Exception:
            pass
    if os.getenv("GEMINI_API_KEY"):
        try:
            return _parse_with_gemini(prompt)
        except Exception:
            pass

    return _mock_parse(emails_text, profile)