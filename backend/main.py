from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import AnalyzeRequest, AnalyzeResponse, Opportunity, NotOpportunity
from ai_parser import parse_emails
from scorer import score_and_rank

app = FastAPI(title="Inbox Copilot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Inbox Copilot API is running!"}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    try:
        # Step 1: AI parses and extracts from emails
        parsed = parse_emails(req.emails_text, req.profile)

        # Step 2: Deterministic scorer ranks them
        ranked_raw = score_and_rank(parsed["opportunities"], req.profile)

        # Step 3: Convert to Opportunity models
        opportunities = []
        for opp in ranked_raw:
            opportunities.append(Opportunity(
                rank=opp["rank"],
                title=opp.get("title", "Unknown"),
                type=opp.get("type", "Other"),
                organization=opp.get("organization", ""),
                deadline=opp.get("deadline", "Unknown"),
                deadline_days=opp.get("deadline_days", 999),
                urgency=opp.get("urgency", "NORMAL"),
                benefits=opp.get("benefits", ""),
                requirements=opp.get("requirements", []),
                apply_link=opp.get("apply_link", "Not provided"),
                eligibility_note=opp.get("eligibility_note", ""),
                eligible=opp.get("eligible", True),
                fit_score=opp.get("fit_score", 50),
                urgency_score=opp.get("urgency_score", 50),
                value_score=opp.get("value_score", 50),
                overall_score=opp.get("overall_score", 50),
                reasoning=opp.get("reasoning", ""),
                action_checklist=opp.get("action_checklist", [])
            ))

        not_opps = [
            NotOpportunity(
                subject=n.get("subject", "Unknown"),
                reason=n.get("reason", "")
            )
            for n in parsed.get("not_opportunities", [])
        ]

        return AnalyzeResponse(
            opportunities=opportunities,
            not_opportunities=not_opps,
            summary=parsed.get("summary", "")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))