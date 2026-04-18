import React from 'react'

export default function ProfileForm({ profile, onChange, onAnalyze, loading }) {
  const set = (field, val) => onChange({ ...profile, [field]: val })

  return (
    <div>
      <div className="hint">
        Fill in your student profile so the AI can rank opportunities by how well they match you personally.
      </div>

      <div className="grid-2">
        <div className="sec">
          <label>Degree / Program</label>
          <select value={profile.degree} onChange={e => set('degree', e.target.value)}>
            <option>BS Computer Science</option>
            <option>BS Software Engineering</option>
            <option>BS Data Science</option>
            <option>BS Electrical Engineering</option>
            <option>BS Artificial Intelligence</option>
            <option>MS Computer Science</option>
            <option>MBA</option>
            <option>Other</option>
          </select>
        </div>
        <div className="sec">
          <label>Current Semester</label>
          <select value={profile.semester} onChange={e => set('semester', parseInt(e.target.value))}>
            {[1,2,3,4,5,6,7,8].map(s => (
              <option key={s} value={s}>Semester {s}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid-3">
        <div className="sec">
          <label>CGPA (out of 4.0)</label>
          <input
            type="number" min="0" max="4" step="0.01"
            value={profile.cgpa}
            onChange={e => set('cgpa', parseFloat(e.target.value))}
          />
        </div>
        <div className="sec">
          <label>Financial Need</label>
          <select value={profile.financial_need} onChange={e => set('financial_need', e.target.value)}>
            <option>Yes</option>
            <option>Somewhat</option>
            <option>No</option>
          </select>
        </div>
        <div className="sec">
          <label>Location Preference</label>
          <select value={profile.location_pref} onChange={e => set('location_pref', e.target.value)}>
            <option>Pakistan</option>
            <option>Remote / Online</option>
            <option>International</option>
            <option>Any</option>
          </select>
        </div>
      </div>

      <div className="sec">
        <label>Skills & Interests (comma separated)</label>
        <input
          type="text"
          value={profile.skills}
          onChange={e => set('skills', e.target.value)}
          placeholder="Python, Machine Learning, React, Data Analysis, NLP..."
        />
      </div>

      <div className="grid-2">
        <div className="sec">
          <label>Preferred Opportunity Types</label>
          <select value={profile.preferred_types} onChange={e => set('preferred_types', e.target.value)}>
            <option>All types</option>
            <option>Internships & Competitions</option>
            <option>Scholarships only</option>
            <option>Internships only</option>
            <option>Competitions only</option>
            <option>Fellowships only</option>
          </select>
        </div>
        <div className="sec">
          <label>Past Experience</label>
          <input
            type="text"
            value={profile.experience}
            onChange={e => set('experience', e.target.value)}
            placeholder="1 internship, 2 hackathons, research assistant..."
          />
        </div>
      </div>

      <button className="btn-primary" onClick={onAnalyze} disabled={loading}>
        {loading ? 'Analyzing your inbox...' : 'Analyze My Inbox →'}
      </button>
    </div>
  )
}