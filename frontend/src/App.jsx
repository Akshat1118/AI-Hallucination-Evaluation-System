import React, { useState } from 'react'
import EvaluationForm from './components/EvaluationForm'
import EvaluationResult from './components/EvaluationResult'
import ResearchDocumentation from './components/ResearchDocumentation'
import TechStackView from './components/TechStackView'

export default function App() {
  const [activeTab, setActiveTab] = useState('evaluator') // 'evaluator' | 'research' | 'techstack'
  const [evaluationId, setEvaluationId] = useState(null)
  const [result, setResult] = useState(null)

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 flex flex-col font-sans">
      {/* Top Navigation Bar */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-xs">
        <div className="max-w-6xl mx-auto px-6 py-3.5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-indigo-600 text-white flex items-center justify-center font-bold text-lg shadow-sm">
              🧠
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-base font-extrabold text-slate-900 tracking-tight">
                  AI Hallucination Evaluation System
                </h1>
                <span className="text-xs bg-indigo-50 border border-indigo-200 text-indigo-700 font-semibold px-2 py-0.5 rounded-full">
                  Milestone 1
                </span>
              </div>
              <p className="text-xs text-slate-500 font-medium">
                Infosys Springboard Internship • Multi-Agent LLM-as-a-Judge with RAG
              </p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs font-semibold">
            <button
              onClick={() => setActiveTab('evaluator')}
              className={`px-3.5 py-1.5 rounded-lg transition ${
                activeTab === 'evaluator'
                  ? 'bg-white text-indigo-600 shadow-xs font-bold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              🔍 Live Evaluator
            </button>
            <button
              onClick={() => setActiveTab('research')}
              className={`px-3.5 py-1.5 rounded-lg transition ${
                activeTab === 'research'
                  ? 'bg-white text-indigo-600 shadow-xs font-bold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              📖 M1.1 Research & Scoring
            </button>
            <button
              onClick={() => setActiveTab('techstack')}
              className={`px-3.5 py-1.5 rounded-lg transition ${
                activeTab === 'techstack'
                  ? 'bg-white text-indigo-600 shadow-xs font-bold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              🛠️ Tech Stack & Arch
            </button>
          </nav>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-6xl w-full mx-auto px-6 py-8 flex-1 space-y-8">
        {activeTab === 'evaluator' && (
          <div className="space-y-8">
            <EvaluationForm
              onResult={(id, res) => {
                setEvaluationId(id)
                setResult(res)
              }}
            />

            {result && (
              <EvaluationResult result={result} evaluationId={evaluationId} />
            )}
          </div>
        )}

        {activeTab === 'research' && <ResearchDocumentation />}

        {activeTab === 'techstack' && <TechStackView />}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-500">
        <p className="font-medium text-slate-700 mb-0.5">
          AI Hallucination Evaluation System — Infosys Springboard 2026
        </p>
        <p>
          Powered by FastAPI • Google Gemini API • ChromaDB • Sentence Transformers • React
        </p>
      </footer>
    </div>
  )
}
