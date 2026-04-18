def score_and_rank(opportunities: list, profile) -> list:
    """
    Deterministic scoring engine - built by team, not AI.
    Formula: Overall = 0.40 * fit + 0.35 * urgency + 0.25 * value
    """
    scored = []

    for opp in opportunities:
        u_score = calculate_urgency_score(opp.get("deadline_days", 999))
        f_score = calculate_fit_score(opp, profile)
        v_score = calculate_value_score(opp)

        overall = round(
            (0.40 * f_score) +
            (0.35 * u_score) +
            (0.25 * v_score),
            1
        )

        opp["urgency_score"] = round(u_score, 1)
        opp["fit_score"]     = round(f_score, 1)
        opp["value_score"]   = round(v_score, 1)
        opp["overall_score"] = overall
        scored.append(opp)

    # Sort by overall score descending
    scored.sort(key=lambda x: x["overall_score"], reverse=True)

    # Assign final ranks
    for i, opp in enumerate(scored):
        opp["rank"] = i + 1

    return scored


def calculate_urgency_score(deadline_days: int) -> float:
    """Score urgency: closer deadline = higher score"""
    if deadline_days <= 0:   return 0.0
    if deadline_days <= 3:   return 100.0
    if deadline_days <= 7:   return 90.0
    if deadline_days <= 14:  return 78.0
    if deadline_days <= 30:  return 62.0
    if deadline_days <= 60:  return 45.0
    if deadline_days <= 90:  return 35.0
    if deadline_days == 999: return 50.0   # rolling/unknown
    return 25.0


def calculate_fit_score(opp: dict, profile) -> float:
    """Score profile fit based on AI estimate + deterministic adjustments"""
    score = float(opp.get("fit_score", 50))

    # Heavy penalty if not eligible
    if not opp.get("eligible", True):
        score *= 0.35

    # Bonus: preferred type match
    preferred = profile.preferred_types.lower()
    opp_type  = opp.get("type", "").lower()
    if preferred != "all types":
        if opp_type in preferred:
            score = min(100, score + 12)
        else:
            score = max(0, score - 10)

    # Bonus: location preference match
    benefits = opp.get("benefits", "").lower()
    title    = opp.get("title", "").lower()
    org      = opp.get("organization", "").lower()
    combined = benefits + title + org

    if profile.location_pref == "Pakistan":
        if "pakistan" in combined or "pkr" in combined or "hec" in combined:
            score = min(100, score + 8)
    elif profile.location_pref == "Remote / Online":
        if "remote" in combined or "online" in combined:
            score = min(100, score + 8)

    # Bonus: financial need alignment
    if profile.financial_need == "Yes":
        if "stipend" in combined or "scholarship" in combined or "waiver" in combined:
            score = min(100, score + 5)

    return round(min(100, max(0, score)), 1)


def calculate_value_score(opp: dict) -> float:
    """Score opportunity value based on benefits keywords"""
    benefits = opp.get("benefits", "").lower()
    title    = opp.get("title", "").lower()
    combined = benefits + " " + title

    score = 40.0

    value_keywords = [
        ("full tuition", 25),
        ("tuition waiver", 22),
        ("fellowship", 18),
        ("stipend", 16),
        ("salary", 16),
        ("prize", 14),
        ("scholarship", 14),
        ("paid", 12),
        ("allowance", 10),
        ("mentorship", 8),
        ("google", 10),
        ("meta", 10),
        ("microsoft", 10),
        ("hec", 8),
        ("international", 7),
        ("certificate", 4),
        ("experience", 3),
    ]

    for keyword, bonus in value_keywords:
        if keyword in combined:
            score += bonus

    return round(min(100, score), 1)