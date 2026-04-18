import React from 'react'

function scoreColor(s) {
  if (s >= 75) return '#16a34a'
  if (s >= 50) return '#ea580c'
  return '#dc2626'
}

function rankClass(r) {
  const classes = ['rank-1', 'rank-2', 'rank-3', 'rank-4']
  return classes[Math.min(r - 1, 3)]
}

function UrgencyBadge({ urgency, days }) {
  const dayText = days && days < 999 ? ` · ${days}d left` : ''
  if (urgency === 'URGENT') return <span className="badge b-urgent">⚡ Urgent{dayText}</span>
  if (urgency === 'SOON')   return <span className="badge b-soon">⏳ Soon{dayText}</span>
  return <span className="badge b-normal">📅 Normal</span>
}

export default function ResultsPanel({ results, loading, error }) {
  if (loading) {
    return (
      <div className="loading">
        <div className="spinner" />
        <div className="loading-text">Scanning your inbox...</div>
        <div className="loading-sub">Detecting opportunities · Extracting details · Ranking by fit</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error-box">
        <strong>Error:</strong> {error}
        <br /><small>Make sure the backend is running at http://localhost:8000</small>
      </div>
    )
  }

  if (!results) {
    return <p style={{ fontSize: '14px', color: '#888' }}>Complete the steps above and click Analyze to see your results here.</p>
  }

  const { opportunities = [], not_opportunities = [], summary } = results

  return (
    <div>
      {/* Stats */}
      <div className="stats-row">
        <div className="stat-box">
          <div className="stat-num">{opportunities.length}</div>
          <div className="stat-lbl">Opportunities</div>
        </div>
        <div className="stat-box">
          <div className="stat-num" style={{ color: '#dc2626' }}>
            {opportunities.filter(o => o.urgency === 'URGENT').length}
          </div>
          <div className="stat-lbl">Urgent</div>
        </div>
        <div className="stat-box">
          <div className="stat-num" style={{ color: '#ea580c' }}>
            {opportunities.filter(o => o.urgency === 'SOON').length}
          </div>
          <div className="stat-lbl">Act Soon</div>
        </div>
        <div className="stat-box">
          <div className="stat-num" style={{ color: '#9ca3af' }}>
            {not_opportunities.length}
          </div>
          <div className="stat-lbl">Filtered Out</div>
        </div>
      </div>

      {/* AI Summary */}
      {summary && <div className="summary-box">💡 {summary}</div>}

      {/* Ranked Opportunity Cards */}
      {opportunities.map(opp => (
        <div key={opp.rank} className={`opp-card ${rankClass(opp.rank)}`}>

          {/* Header */}
          <div className="opp-header">
            <div className="rank-num">#{opp.rank}</div>
            <div style={{ flex: 1 }}>
              <div className="opp-title">{opp.title}</div>
              {opp.organization && <div className="opp-org">{opp.organization}</div>}
              <div className="badges">
                <span className="badge b-type">{opp.type}</span>
                <UrgencyBadge urgency={opp.urgency} days={opp.deadline_days} />
                <span className={`badge ${opp.eligible ? 'b-eligible' : 'b-ineligible'}`}>
                  {opp.eligible ? '✓ Eligible' : '✗ Check Eligibility'}
                </span>
              </div>
            </div>
          </div>

          {/* Score Bar */}
          <div className="score-wrap">
            <div className="score-meta">
              <span className="score-label">Overall Match Score</span>
              <span style={{ fontWeight: 700, color: scoreColor(opp.overall_score) }}>
                {opp.overall_score}/100
              </span>
            </div>
            <div className="score-bg">
              <div
                className="score-fill"
                style={{ width: `${opp.overall_score}%`, background: scoreColor(opp.overall_score) }}
              />
            </div>
            <div className="sub-scores">
              <span className="sub-score">Fit: {opp.fit_score}</span>
              <span className="sub-score">Urgency: {opp.urgency_score}</span>
              <span className="sub-score">Value: {opp.value_score}</span>
            </div>
          </div>

          {/* Details */}
          <div className="detail-grid">
            <span className="dk">Deadline</span>
            <span className="dv">{opp.deadline}</span>

            <span className="dk">Benefits</span>
            <span className="dv">{opp.benefits}</span>

            <span className="dk">Eligibility</span>
            <span className="dv">{opp.eligibility_note}</span>

            {opp.apply_link && opp.apply_link !== 'Not provided' && (
              <>
                <span className="dk">Apply Link</span>
                <span className="dv" style={{ color: '#2563eb', wordBreak: 'break-all' }}>
                  {opp.apply_link}
                </span>
              </>
            )}
          </div>

          {/* AI Reasoning */}
          {opp.reasoning && (
            <div className="reasoning">{opp.reasoning}</div>
          )}

          {/* Requirements */}
          {opp.requirements?.length > 0 && (
            <div style={{ fontSize: '13px', margin: '10px 0' }}>
              <span style={{ fontWeight: 700, color: '#555' }}>Documents needed: </span>
              <span style={{ color: '#333' }}>{opp.requirements.join(' · ')}</span>
            </div>
          )}

          {/* Action Checklist */}
          {opp.action_checklist?.length > 0 && (
            <div className="checklist">
              <div className="checklist-title">Your Action Checklist</div>
              {opp.action_checklist.map((step, i) => (
                <div key={i} className="cl-item">
                  <span className="cl-check">✓</span>
                  <span>{step}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      ))}

      {/* Filtered Out Section */}
      {not_opportunities.length > 0 && (
        <div className="filtered-section">
          <div className="filtered-title">
            Filtered Out — Not Opportunities ({not_opportunities.length})
          </div>
          {not_opportunities.map((n, i) => (
            <div key={i} className="filtered-item">
              <strong>{n.subject}</strong> — {n.reason}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}