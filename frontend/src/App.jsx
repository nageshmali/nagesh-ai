
import { useState } from 'react'
import './App.css'
import Chat from './Chat.jsx'
import JobMatch from './JobMatch.jsx'

function App() {
  const [activePage, setActivePage] = useState('home')
  const [darkMode, setDarkMode] = useState(false)

  return (
    <div className={`app-container ${darkMode ? 'dark-mode' : ''}`}>

      {/* Sidebar */}
      <aside className="sidebar">

        <div className="brand">
          <div className="brand-icon">N</div>
          <h2>NageshAI</h2>
        </div>

        <div className="sidebar-menu">
          <p className="menu-label">WORKSPACE</p>

          <button
            className={activePage === 'home' ? 'nav-item active' : 'nav-item'}
            onClick={() => setActivePage('home')}
          >
            <span>⌂</span> Home
          </button>

          <button
            className={activePage === 'chat' ? 'nav-item active' : 'nav-item'}
            onClick={() => setActivePage('chat')}
          >
            <span>◉</span> Chat with NageshAI
          </button>

          <button
            className={activePage === 'match' ? 'nav-item active' : 'nav-item'}
            onClick={() => setActivePage('match')}
          >
            <span>⌕</span> Job Match Analyzer
          </button>
        </div>

        <div className="sidebar-footer">
          <p>AI-powered professional portfolio</p>
          <span>Version 1.0</span>
        </div>

      </aside>

      {/* Main Content */}
      <main className="main-content">

        {/* Top Navigation */}
        <header className="topbar">

          <span>Personal AI Portfolio</span>

          <div className="header-actions">

            <div className="status">
              <span className="status-dot"></span>
              AI Assistant
            </div>

            <button
              className="theme-toggle"
              onClick={() => setDarkMode(!darkMode)}
            >
              {darkMode ? '☀️ Light Mode' : '🌙 Dark Mode'}
            </button>

          </div>

        </header>

        {/* Page Content */}
        <section className="content-area">

          {/* Home Page */}
          {activePage === 'home' && (
            <div className="welcome-section">

              <span className="welcome-tag">
                WELCOME TO NAGESHAI
              </span>

              <h1>
                Your next conversation
                <br />
                starts here.
              </h1>

              <p className="welcome-description">
                Explore Nagesh's technical background, projects,
                skills and professional profile through an
                AI-powered assistant.
              </p>

              {/* Feature Cards */}
              <div className="feature-cards">

                <div className="feature-card">

                  <div className="feature-icon">💬</div>

                  <h3>Chat with NageshAI</h3>

                  <p>
                    Ask questions about technical skills,
                    education, projects and experience.
                  </p>

                  <button
                    onClick={() => setActivePage('chat')}
                  >
                    Start Conversation →
                  </button>

                </div>

                <div className="feature-card">

                  <div className="feature-icon">📄</div>

                  <h3>Job Match Analyzer</h3>

                  <p>
                    Submit a job description and evaluate
                    how well the candidate matches the requirements.
                  </p>

                  <button
                    onClick={() => setActivePage('match')}
                  >
                    Analyze Job →
                  </button>

                </div>

              </div>

            </div>
          )}

          {/* Chat Page */}
          {activePage === 'chat' && <Chat />}

          {/* Job Match Page */}
          {activePage === 'match' && <JobMatch />}

        </section>

      </main>

    </div>
  )
}

export default App
