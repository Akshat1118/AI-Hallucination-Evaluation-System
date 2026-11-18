import React from 'react'

const VERDICT_STYLES = {
  EXCELLENT: {
    color: 'text-emerald-700',
    bg: 'bg-emerald-50 border-emerald-200',
    badge: 'bg-emerald-100 text-emerald-800 border-emerald-300',
    emoji: '✅',
    summary: 'High factual precision with no unsupported claims detected. Safe for deployment.'
  },
  GOOD: {
    color: 'text-teal-700',
    bg: 'bg-teal-50 border-teal-200',
    badge: 'bg-teal-100 text-teal-800 border-teal-300',
    emoji: '✅',
    summary: 'Response is mostly accurate with only minor stylistic or peripheral omissions.'
  },
  ACCEPTABLE: {
    color: 'text-amber-700',
    bg: 'bg-amber-50 border-amber-200',
    badge: 'bg-amber-100 text-amber-800 border-amber-300',
    emoji: '⚠️',
    summary: 'Partial correctness with noticeable gaps or borderline unsupported statements.'
  },
  POOR: {
    color: 'text-orange-700',
    bg: 'bg-orange-50 border-orange-200',
    badge: 'bg-orange-100 text-orange-800 border-orange-300',
    emoji: '❌',
    summary: 'High hallucination rate or major factual inaccuracies. Requires human review.'
  },
  DANGEROUS: {
    color: 'text-rose-700',
    bg: 'bg-rose-50 border-rose-200',
    badge: 'bg-rose-100 text-rose-800 border-rose-300',
    emoji: '🚫',
    summary: 'Critical hallucination or completely fabricated facts. Should not be used.'
  },
}

const SEVERITY_BADGES = {
  NONE: 'bg-emerald-100 text-emerald-800 border-emerald-200',
  MINOR: 'bg-blue-100 text-blue-800 border-blue-200',
  MODERATE: 'bg-amber-100 text-amber-800 border-amber-200',
  SEVERE: 'bg-orange-100 text-orange-800 border-orange-200',
  CRITICAL: 'bg-rose-100 text-rose-800 border-rose-200',
}

function ScoreProgressBar({ score, label, weight }) {
  const safeScore = score ?? 0
  const pct = Math.min(Math.max((safeScore / 10) * 100, 0), 100)
  const barColor = pct >= 70 ? 'bg-emerald-500' : pct >= 40 ? 'bg-amber-500' : 'bg-rose-500'

  return (
    <div>
      <div className="flex justify-between items-center text-sm mb-1.5">
        <span className="font-medium text-slate-700 flex items-center gap-1.5">
          {label}
          {weight && <span className="text-xs text-slate-400 font-normal">({weight} weight)</span>}
        </span>
        <span className="font-bold text-slate-900">{safeScore.toFixed(1)} <span className="text-slate-400 font-normal text-xs">/ 10</span></span>
      </div>
      <div className="h-2.5 bg-slate-100 rounded-full overflow-hidden border border-slate-200/60">
        <div className={`h-full ${barColor} rounded-full transition-all duration-700`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  )
}

export default function EvaluationResult({ result, evaluationId }) {
  if (!result) return null

  const { scores, overall_score, verdict, retrieved_context } = result
  const style = VERDICT_STYLES[verdict] || VERDICT_STYLES.ACCEPTABLE

  return (
    <div className="space-y-6">
      {/* Verdict Header Banner */}
      <div className={`rounded-2xl border p-6 shadow-sm ${style.bg}`}>
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <span className={`text-xs px-2.5 py-0.5 rounded-full font-semibold border ${style.badge}`}>
                Verdict Outcome
              </span>
              <span className="text-xs text-slate-500 font-mono">ID: {evaluationId?.slice(0, 8)}...</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-3xl">{style.emoji}</span>
              <h3 className={`text-3xl font-extrabold ${style.color}`}>{verdict}</h3>
            </div>
            <p className="text-slate-600 text-sm mt-2 max-w-xl leading-relaxed">
              {style.summary}
            </p>
          </div>

          <div className="bg-white/80 backdrop-blur rounded-xl p-4 border border-slate-200/70 text-center min-w-[140px] shadow-sm">
            <p className="text-slate-500 text-xs font-semibold uppercase tracking-wider mb-0.5">Overall Score</p>
            <p className={`text-4xl font-extrabold ${style.color}`}>{(overall_score ?? 0).toFixed(1)}</p>
            <p className="text-slate-400 text-xs font-medium mt-0.5">out of 10.0</p>
          </div>
        </div>
      </div>

      {/* Dimension Progress Bars */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
        <h3 className="text-slate-900 font-bold text-base mb-5 pb-3 border-b border-slate-100 flex items-center justify-between">
          <span>Scoring Dimensions Breakdown</span>
          <span className="text-xs text-slate-400 font-normal">Formula: Acc(30%) + Halluc(30%) + Rel(25%) + Comp(15%)</span>
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-5">
          <ScoreProgressBar score={scores?.relevance?.score} label="Relevance" weight="25%" />
          <ScoreProgressBar score={scores?.accuracy?.score} label="Factuality & Accuracy" weight="30%" />
          <ScoreProgressBar score={scores?.hallucination?.score} label="Hallucination Freedom" weight="30%" />
          <ScoreProgressBar score={scores?.completeness?.score} label="Completeness" weight="15%" />
        </div>
      </div>

      {/* Agent Analysis Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Relevance Agent */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5">
          <div className="flex items-center justify-between mb-2 pb-2 border-b border-slate-100">
            <h4 className="font-bold text-slate-800 text-sm">🎯 Relevance Judge Agent</h4>
            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-700">
              {scores?.relevance?.score ?? 'N/A'}/10
            </span>
          </div>
          <p className="text-slate-600 text-sm leading-relaxed">{scores?.relevance?.reasoning || 'No details.'}</p>
        </div>

        {/* Accuracy Agent */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5">
          <div className="flex items-center justify-between mb-2 pb-2 border-b border-slate-100">
            <h4 className="font-bold text-slate-800 text-sm">⚖️ Accuracy Judge Agent</h4>
            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-700">
              {scores?.accuracy?.score ?? 'N/A'}/10
            </span>
          </div>
          <p className="text-slate-600 text-sm leading-relaxed">{scores?.accuracy?.reasoning || 'No details.'}</p>
        </div>

        {/* Hallucination Agent */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5">
          <div className="flex items-center justify-between mb-2 pb-2 border-b border-slate-100">
            <h4 className="font-bold text-slate-800 text-sm">🔍 Hallucination Detection Agent</h4>
            <span className={`text-xs font-bold px-2 py-0.5 rounded border ${SEVERITY_BADGES[scores?.hallucination?.severity] || 'bg-slate-100 text-slate-700'}`}>
              Severity: {scores?.hallucination?.severity || 'N/A'}
            </span>
          </div>
          <p className="text-slate-600 text-sm leading-relaxed mb-3">{scores?.hallucination?.reasoning || 'No details.'}</p>
          {scores?.hallucination?.hallucinated_segments?.length > 0 && (
            <div className="bg-rose-50 border border-rose-200 rounded-lg p-3">
              <p className="text-xs font-bold text-rose-800 mb-1.5">Flagged Hallucinated Segments:</p>
              <div className="space-y-1">
                {scores.hallucination.hallucinated_segments.map((seg, i) => (
                  <span key={i} className="inline-block bg-white text-rose-700 border border-rose-300 text-xs px-2 py-1 rounded font-mono mr-1 mb-1">
                    "{seg}"
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Completeness Agent */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5">
          <div className="flex items-center justify-between mb-2 pb-2 border-b border-slate-100">
            <h4 className="font-bold text-slate-800 text-sm">📋 Completeness Judge Agent</h4>
            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-700">
              {scores?.completeness?.score ?? 'N/A'}/10
            </span>
          </div>
          <p className="text-slate-600 text-sm leading-relaxed">{scores?.completeness?.reasoning || 'No details.'}</p>
        </div>
      </div>

      {/* Retrieved RAG Context */}
      {retrieved_context && retrieved_context.length > 0 && (
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
          <h3 className="text-slate-900 font-bold text-base mb-3 pb-2 border-b border-slate-100 flex items-center justify-between">
            <span>📚 Grounding Reference Context (RAG Knowledge Base)</span>
            <span className="text-xs text-slate-400 font-normal">ChromaDB semantic retrieval</span>
          </h3>
          <div className="space-y-2.5">
            {retrieved_context.map((ctx, i) => (
              <div key={i} className="bg-slate-50 rounded-lg p-3.5 border border-slate-200 text-sm text-slate-700 leading-relaxed font-sans">
                <span className="text-xs font-bold text-indigo-600 uppercase block mb-1">Source Snippet {i + 1}</span>
                {ctx}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
