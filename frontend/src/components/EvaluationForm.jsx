import React, { useState } from 'react'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api/v1'

export default function EvaluationForm({ onResult }) {
  const [form, setForm] = useState({
    question: '',
    ai_response: '',
    reference_answer: '',
    source_document: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const pollForResult = async (evalId, maxAttempts = 15) => {
    for (let i = 0; i < maxAttempts; i++) {
      await new Promise(r => setTimeout(r, 2000))
      const res = await axios.get(`${API_BASE}/evaluate/${evalId}`)
      if (res.data.status === 'completed') return res.data
      if (res.data.status === 'failed') throw new Error('Evaluation failed on server.')
    }
    throw new Error('Evaluation timed out.')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      // Submit evaluation
      const submitRes = await axios.post(`${API_BASE}/evaluate`, {
        question: form.question,
        ai_response: form.ai_response,
        reference_answer: form.reference_answer || undefined,
        source_document: form.source_document || undefined,
      })
      const evalId = submitRes.data.evaluation_id

      // Poll for result
      const result = await pollForResult(evalId)
      onResult(evalId, result)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-slate-800 rounded-2xl border border-slate-700 p-8">
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-white">Evaluation Input</h2>
        <p className="text-slate-400 text-sm mt-1">
          Submit an AI-generated response for multi-dimensional hallucination evaluation.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-5">
        {/* Question */}
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-1.5">
            Question <span className="text-red-400">*</span>
          </label>
          <textarea
            name="question"
            value={form.question}
            onChange={handleChange}
            required
            rows={2}
            placeholder="Enter the question that was asked to the AI..."
            className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
          />
        </div>

        {/* AI Response */}
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-1.5">
            AI Response <span className="text-red-400">*</span>
          </label>
          <textarea
            name="ai_response"
            value={form.ai_response}
            onChange={handleChange}
            required
            rows={5}
            placeholder="Paste the AI-generated response to evaluate..."
            className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
          />
        </div>

        {/* Reference Answer (optional) */}
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-1.5">
            Reference Answer <span className="text-slate-500 font-normal">(optional)</span>
          </label>
          <textarea
            name="reference_answer"
            value={form.reference_answer}
            onChange={handleChange}
            rows={2}
            placeholder="Provide a ground-truth reference answer for comparison..."
            className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
          />
        </div>

        {/* Source Document (optional) */}
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-1.5">
            Source Document / Reference Material <span className="text-slate-500 font-normal">(optional)</span>
          </label>
          <textarea
            name="source_document"
            value={form.source_document}
            onChange={handleChange}
            rows={3}
            placeholder="Paste source material or reference document for grounding evaluation..."
            className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
          />
        </div>

        {error && (
          <div className="bg-red-900/30 border border-red-700 text-red-300 px-4 py-3 rounded-lg text-sm">
            ⚠️ {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !form.question.trim() || !form.ai_response.trim()}
          className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
              </svg>
              Evaluating...
            </>
          ) : (
            '🔍 Evaluate Response'
          )}
        </button>
      </form>
    </div>
  )
}
