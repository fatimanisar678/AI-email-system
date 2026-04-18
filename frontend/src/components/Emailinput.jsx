import React from 'react'

const SAMPLE_EMAILS = `Subject: Dawood Foundation Scholarship 2026
From: scholarships@dawoodfoundation.org

The Dawood Foundation announces merit-cum-need scholarships for CS and Engineering undergraduates.
Award: PKR 150,000 per year for up to 2 years.
Eligibility: Pakistani nationals, semester 5-8, minimum CGPA 3.0, financial need required.
Required Documents: CNIC copy, official transcript, family income certificate, 2 reference letters, personal statement 500 words.
Deadline: May 15, 2026
Apply at: www.dawoodfoundation.org/scholarship
Contact: scholarships@dawoodfoundation.org

---

Subject: Google Summer of Code 2026 - Contributor Applications
From: gsoc-announce@google.com

Google Summer of Code 2026 is now open for student contributors!
Work on open-source projects with mentorship from Google engineers.
Stipend: USD 1,500 to 3,300 depending on location.
Requirements: Must be an enrolled student, strong programming skills. No CGPA cutoff.
Application Deadline: April 2, 2026
Apply at: summerofcode.withgoogle.com

---

Subject: FREE Pizza Night - CS Society Event This Friday!
From: cs-society@fast.edu.pk

Hey everyone! Join us this Friday 7pm for free pizza, games, and a chill time in the cafeteria.
No registration needed, just show up and bring your friends!

---

Subject: HEC Indigenous Scholarship - LAST DATE APPROACHING
From: hec-scholarships@hec.gov.pk

URGENT REMINDER: HEC Indigenous Scholarship deadline is April 25, 2026.
Eligibility: Pakistani students only, CGPA 3.5 or above, enrolled full-time in BS or MS.
Benefits: Full tuition fee waiver plus PKR 8,000 monthly stipend.
Required Documents: Enrollment certificate, detailed marks sheet, CNIC, 2 passport photos.
Apply at: hec.gov.pk/scholarships/indigenous
Helpline: 051-111-119-432

---

Subject: Meta University Internship Program - Summer 2026
From: university-programs@meta.com

Meta invites applications for the Summer 2026 University Internship in Software Engineering, ML, and Data Science.
Duration: 12 weeks from June to August 2026.
Location: Remote or US office with visa sponsorship for exceptional candidates.
Stipend: Competitive market rate.
Requirements: Enrolled student, experience in Python or C++ or Java, algorithms coursework, preferably penultimate year.
Deadline: Rolling basis, apply before May 1, 2026.
Apply at: metacareers.com/students

---

Subject: Library Book Return Reminder
From: library@fast.edu.pk

Dear Student, please return all borrowed books before April 30, 2026.
A fine of PKR 10 per day applies after the due date.
Library hours: Monday to Saturday, 9am to 6pm.

---

Subject: SOFTEC 2026 AI Hackathon - Register Now!
From: softec@fast.edu.pk

SOFTEC 2026 presents the AI Hackathon open to all FAST-NU students!
Form a team of 2 to 4 members and build an AI-powered solution in 6 hours.
Prizes: PKR 50,000 first place, PKR 25,000 second place, PKR 10,000 third place.
Themes: AI for Education, Health, or Productivity.
No CGPA requirement. All semesters welcome.
Registration Deadline: April 20, 2026
Register at: softecnu.org/hackathon
Email: softec@fast.edu.pk`

export default function EmailInput({ value, onChange, onNext }) {
  return (
    <div>
      <div className="hint">
        Paste your opportunity emails below, separating each email with <strong>---</strong>.
        You can paste 5 to 15 emails at once.
      </div>

      <div className="sec">
        <label>
          Your Emails
          <button className="sample-btn" onClick={() => onChange(SAMPLE_EMAILS)}>
            load 7 sample emails
          </button>
        </label>
        <textarea
          rows={18}
          value={value}
          onChange={e => onChange(e.target.value)}
          placeholder={`Subject: Scholarship Open\nFrom: org@example.com\n\nEmail body here...\n\n---\n\nSubject: Next Email\nFrom: another@org.com\n\nAnother email body...`}
        />
      </div>

      <button className="btn-primary" onClick={onNext}>
        Next: Fill Your Profile →
      </button>
    </div>
  )
}