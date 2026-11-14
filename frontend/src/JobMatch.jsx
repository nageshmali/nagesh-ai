
import { useState } from 'react'
import './JobMatch.css'

function JobMatch() {
  const [jobDescription, setJobDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  async function handleAnalyze() {
    if (!jobDescription.trim() || loading) return

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await fetch('http://127.0.0.1:8000/match-job', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          job_description: jobDescription,
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to analyze the job description.')
      }

      const data = await response.json()
      setResult(data)

    } catch (err) {
      setError(err.message || 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="job-match-container">

      <div className="job-match-heading">
        <h1>Job Match Analyzer</h1>
        <p>
          Evaluate how well a job opportunity matches
          Nagesh's technical profile.
        </p>
      </div>

      {/* Job Description Input */}
      <div className="job-input-card">
        <label htmlFor="job-description">
          Job Description
        </label>

        <textarea
          id="job-description"
          value={jobDescription}
          onChange={(event) => setJobDescription(event.target.value)}
          placeholder="Paste the complete job description here..."
          rows={12}
        />

        <div className="job-input-footer">
          <span>{jobDescription.length} characters</span>

          <button
            onClick={handleAnalyze}
            disabled={!jobDescription.trim() || loading}
          >
            {loading ? 'Analyzing...' : 'Analyze Job →'}
          </button>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="job-error">{error}</div>
      )}

      {/* Loading */}
      {loading && (
        <div className="job-loading">
          Analyzing the job description against Nagesh's profile...
        </div>
      )}

      {/* Evaluation Results */}
      {result && (
        <div className="job-result">

          {/* Overall Assessment */}
          <div className="result-header">
            <span className="result-label">OVERALL ASSESSMENT</span>
            <h2>{result.overall_assessment}</h2>
            <p>{result.role_title || 'Job Role'}</p>
          </div>

          {/* Summary */}
          <div className="result-summary">
            <h3>Evaluation Summary</h3>
            <p>{result.summary}</p>
          </div>

          {/* Technical and Eligibility */}
          <div className="result-assessments">
            <div className="assessment-card">
              <span>Technical Assessment</span>
              <h3>{result.technical_assessment}</h3>
            </div>

            <div className="assessment-card">
              <span>Eligibility Assessment</span>
              <h3>{result.eligibility_assessment}</h3>
            </div>
          </div>

          {/* Recommendation */}
          <div className="recommendation-card">
            <h3>AI Recommendation</h3>
            <p>{result.recommendation}</p>
          </div>

          {/* Matched Requirements */}
          <div className="requirements-section">
            <div className="requirements-heading">
              <h3>Matched Requirements</h3>
              <span>{result.matched_requirements.length}</span>
            </div>

            {result.matched_requirements.length > 0 ? (
              result.matched_requirements.map((item, index) => (
                <div className="requirement-card matched" key={index}>
                  <div className="requirement-top">
                    <h4>{item.requirement}</h4>
                    <span>{item.status}</span>
                  </div>

                  <div className="requirement-meta">
                    <span>{item.category}</span>
                    <span>{item.importance}</span>
                  </div>

                  <p>{item.evidence}</p>
                </div>
              ))
            ) : (
              <p className="no-requirements">
                No fully matched requirements found.
              </p>
            )}
          </div>

          {/* Gaps and Unverified Requirements */}
          <div className="requirements-section">
            <div className="requirements-heading">
              <h3>Gaps &amp; Unverified Requirements</h3>
              <span>{result.gaps_or_unverified_requirements.length}</span>
            </div>

            {result.gaps_or_unverified_requirements.length > 0 ? (
              result.gaps_or_unverified_requirements.map((item, index) => (
                <div className="requirement-card gap" key={index}>
                  <div className="requirement-top">
                    <h4>{item.requirement}</h4>
                    <span>{item.status}</span>
                  </div>

                  <div className="requirement-meta">
                    <span>{item.category}</span>
                    <span>{item.importance}</span>
                  </div>

                  <p>{item.evidence}</p>
                </div>
              ))
            ) : (
              <p className="no-requirements">
                No gaps or unverified requirements found.
              </p>
            )}
          </div>

        </div>
      )}
    </div>
  )
}

export default JobMatch
