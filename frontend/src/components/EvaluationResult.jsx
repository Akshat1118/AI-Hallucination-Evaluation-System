import React from 'react'

const VERDICT_STYLES = {
  EXCELLENT: { color: 'text-emerald-400', bg: 'bg-emerald-900/30 border-emerald-700', emoji: '✅' },
  GOOD: { color: 'text-green-400', bg: 'bg-green-900/30 border-green-700', emoji: '✅' },
  ACCEPTABLE: { color: 'text-yellow-400', bg: 'bg-yellow-900/30 border-yellow-700', emoji: '⚠️' },
  POOR: { color: 'text-orange-400', bg: 'bg-orange-900/30 border-orange-700', emoji: '❌' },
  DANGEROUS: { color: 'text-red-400', bg: 'bg-red-900/30 border-red-700', emoji: '🚫' },
}

const SEVERITY_COLORS = {
  NONE: 'text-emerald-400',
  MINOR: 'text-yellow-400',
  MODERATE: 'text-orange-400',
  SEVERE: 'text-red-400',
  CRITICAL: 'text-red-600',
}

function ScoreBar({ score, label }) {
  const pct = ((score || 0) / 10) * 100
  const color = pct >= 70 ? 'bg-emerald-500' : pct >= 40 ? 'bg-yellow-500' : 'bg-red-500'
  return (
    <div>
      <div className="flex justify-between text-sm mb-1">
        <span className="text-slate-300">{label}</span>
        <span className="font-semibold text-white">{score?.toFixed(1) ?? 'N/A'} / 10</span>
      </div>
      <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
        <div className={`h-full ${color} rounded-full transition-all duration-700`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  )
}

export default function EvaluationResult({ result, evaluationId }) {
  if (!result) return null

  const { scores, overall_score, verdict, retrieved_context } = result
  const verdictStyle = VERDICT_STYLES[verdict] || VERDICT_STYLES.ACCEPTABLE

  return (
    <div className="space-y-6">
      {/* Verdict Header */}
      <div className={`rounded-2xl border p-6 ${verdictStyle.bg}`}>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-slate-400 text-sm mb-1">Overall Verdict</p>
            <div className="flex items-center gap-3">
              <span className="text-3xl">{verdictStyle.emoji}</span>
              <span className={`text-3xl font-bold ${verdictStyle.color}`}>{verdict}</span>
            </div>
            <p className="text-slate-400 text-xs mt-1">ID: {evaluationId}</p>
          </div>
          <div className="text-right">
            <p className="text-slate-400 text-sm">Overall Score</p>
            <p className={`text-5xl font-bold ${verdictStyle.color}`}>{overall_score?.toFixed(1)}</p>
            <p className="text-slate-500 text-sm">/10</p>
          </div>
        </div>
      </div>

      {/* Score Bars */}
      <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
        <h3 className="text-white font-semibold mb-5">Dimension Scores</h3>
        <div className="space-y-5">
          <ScoreBar score={scores?.relevance?.score} label="Relevance" />
          <ScoreBar score={scores?.accuracy?.score} label="Accuracy" />
          <ScoreBar score={scores?.hallucination?.score} label="Hallucination (10 = clean)" />
          <ScoreBar score={scores?.completeness?.score} label="Completeness" />
        </div>
      </div>

      {/* Detailed Reasoning */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {['relevance', 'accuracy', 'completeness'].map(dim => (
          <div key={dim} className="bg-slate-800 rounded-xl border border-slate-700 p-5">
            <h4 className="text-white font-medium capitalize mb-2">{dim}</h4>
            <p className="text-slate-400 text-sm leading-relaxed">{scores?.[dim]?.reasoning || 'No reasoning available.'}</p>
          </div>
        ))}

        {/* Hallucination detail */}
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-5">
          <div className="flex items-center justify-between mb-2">
            <h4 className="text-white font-medium">Hallucination</h4>
            <span className={`text-sm font-semibold ${SEVERITY_COLORS[scores?.hallucination?.severity] || 'text-slate-400'}`}>
              {scores?.hallucination?.severity || 'N/A'}
            </span>
          </div>
          <p className="text-slate-400 text-sm leading-relaxed mb-2">{scores?.hallucination?.reasoning || 'No reasoning available.'}</p>
          {scores?.hallucination?.hallucinated_segments?.length > 0 && (
            <div className="mt-2">
              <p className="text-xs text-red-400 font-medium mb-1">Flagged Segments:</p>
              {scores.hallucination.hallucinated_segments.map((seg, i) => (
                <p key={i} className="text-xs bg-red-900/20 border border-red-800 rounded px-2 py-1 text-red-300 mt-1">{seg}</p>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Retrieved Context */}
      {retrieved_context && retrieved_context.length > 0 && (
        <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
          <h3 className="text-white font-semibold mb-4">Retrieved Reference Context (RAG)</h3>
          <div className="space-y-3">
            {retrieved_context.slice(0, 3).map((ctx, i) => (
              <div key={i} className="bg-slate-900 rounded-lg p-3 border border-slate-700">
                <p className="text-xs text-slate-500 mb-1">Context {i + 1}</p>
                <p className="text-slate-400 text-sm leading-relaxed">{ctx}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
