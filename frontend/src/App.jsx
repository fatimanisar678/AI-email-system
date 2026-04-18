import React, { useState } from 'react'
import EmailInput from './components/EmailInput'
import ProfileForm from './components/ProfileForm'
import ResultsPanel from './components/ResultsPanel'
import { analyzeEmails } from './api'

const DEFAULT_PROFILE = {
  degree: 'BS Computer Science',
  semester: 7,
  cgpa: 3.2,
  financial_need: 'Yes',
  location_pref: 'Pakistan',
  skills: 'Python, Machine Learning, Web Development, Data Analysis',
  preferred_types: 'All types',
  experience: '1 startup internship, 2 hackathons'
}

export default function App() {
  const [activeTab, setActiveTab] = useState('emails')
  const [emails, setEmails] = useState('')
  const [profile, setProfile] = useState(DEFAULT_PROFILE)
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleAnalyze = async () => {
    if (!emails.trim()) {
      alert('Please paste your emails first!')
      setActiveTab('emails')
      return
    }
    setLoading(true)
    setError(null)
    setResults(null)
    setActiveTab('results')
    try {
      const data = await analyzeEmails(emails, profile)
      setResults(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-wrapper">
      <div className="topbar">
        <div className="logo">Inbox<span>Copilot</span></div>
        <div className="tagline">AI-Powered Opportunity Ranker · SOFTEC 2026</div>
      </div>

      <div className="tabs">
        {[
          { id: 'emails',  label: '① Paste Emails' },
          { id: 'profile', label: '② Your Profile'  },
          { id: 'results', label: '③ Results'        }
        ].map(t => (
          <button
            key={t.id}
            className={`tab ${activeTab === t.id ? 'active' : ''}`}
            onClick={() => setActiveTab(t.id)}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div className="card">
        <div className={`panel ${activeTab === 'emails'  ? 'active' : ''}`}>
          <EmailInput value={emails} onChange={setEmails} onNext={() => setActiveTab('profile')} />
        </div>
        <div className={`panel ${activeTab === 'profile' ? 'active' : ''}`}>
          <ProfileForm profile={profile} onChange={setProfile} onAnalyze={handleAnalyze} loading={loading} />
        </div>
        <div className={`panel ${activeTab === 'results' ? 'active' : ''}`}>
          <ResultsPanel results={results} loading={loading} error={error} />
        </div>
      </div>
    </div>
  )
}