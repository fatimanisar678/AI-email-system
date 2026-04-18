const BASE_URL = "http://localhost:8000";

export async function analyzeEmails(emailsText, profile) {
  const response = await fetch(`${BASE_URL}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      emails_text: emailsText,
      profile: {
        degree: profile.degree,
        semester: parseInt(profile.semester),
        cgpa: parseFloat(profile.cgpa),
        financial_need: profile.financial_need,
        location_pref: profile.location_pref,
        skills: profile.skills,
        preferred_types: profile.preferred_types,
        experience: profile.experience
      }
    })
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || "Server error occurred");
  }

  return response.json();
}