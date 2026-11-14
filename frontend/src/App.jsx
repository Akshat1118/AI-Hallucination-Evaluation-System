import React, { useState } from 'react'
import EvaluationForm from './components/EvaluationForm'
import EvaluationResult from './components/EvaluationResult'

export default function App() {
  const [evaluationId, setEvaluationId] = useState(null)
  const [result, setResult] = useState(null)

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-800/50 backdrop-blur">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-purple-500 flex items-center justify-center text-lg">🧠</div>
          <div>
            <h1 className="text-lg font-bold text-white">AI Hallucination Evaluation System</h1>
            <p className="text-xs text-slate-400">Infosys Springboard — Multi-Agent LLM Evaluation</p>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-10 space-y-8">
        {/* Evaluation Input Module — M1.3 */}
        <EvaluationForm onResult={(id, res) => { setEvaluationId(id); setResult(res) }} />

        {/* Results Panel */}
        {result && <EvaluationResult result={result} evaluationId={evaluationId} />}
      </main>

      <footer className="border-t border-slate-700 mt-16 py-6 text-center text-slate-500 text-sm">
        AI Hallucination Evaluation System — Milestone 1 | Infosys Springboard 2026
      </footer>
    </div>
  )
}
