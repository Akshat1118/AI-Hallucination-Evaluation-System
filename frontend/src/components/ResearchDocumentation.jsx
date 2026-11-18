import React from 'react'

export default function ResearchDocumentation() {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-8 space-y-8">
      <div>
        <span className="text-xs font-bold text-indigo-600 uppercase tracking-wider bg-indigo-50 border border-indigo-200 px-2.5 py-1 rounded-full">
          Milestone 1.1 Deliverable
        </span>
        <h2 className="text-2xl font-extrabold text-slate-900 mt-2">
          Research & Technical Understanding Report
        </h2>
        <p className="text-slate-500 text-sm mt-1">
          Theoretical foundation, evaluation methodologies, hallucination taxonomies, and framework benchmarks.
        </p>
      </div>

      {/* 1. Evaluation Dimensions */}
      <section className="space-y-3">
        <h3 className="text-lg font-bold text-slate-800 flex items-center gap-2 border-b border-slate-100 pb-2">
          <span>1.</span> Evaluation Scoring Dimensions & Formula
        </h3>
        <p className="text-slate-600 text-sm leading-relaxed">
          The system evaluates responses across four independent dimensions on a standardized <strong>0 to 10</strong> scale, followed by a deterministic weighted verdict:
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
          <div className="border border-slate-200 rounded-xl p-4 bg-slate-50/50">
            <div className="flex justify-between items-center mb-1">
              <h4 className="font-bold text-slate-800 text-sm">🎯 Relevance (Weight: 25%)</h4>
              <span className="text-xs font-bold bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded">0 - 10</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Measures intent alignment. Checks whether the response answers the specific prompt asked without topic drift or evasiveness.
            </p>
          </div>

          <div className="border border-slate-200 rounded-xl p-4 bg-slate-50/50">
            <div className="flex justify-between items-center mb-1">
              <h4 className="font-bold text-slate-800 text-sm">⚖️ Accuracy & Factuality (Weight: 30%)</h4>
              <span className="text-xs font-bold bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded">0 - 10</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Verifies factual correctness against real-world knowledge and retrieved reference documents. Penalyzes wrong dates, names, or figures.
            </p>
          </div>

          <div className="border border-slate-200 rounded-xl p-4 bg-slate-50/50">
            <div className="flex justify-between items-center mb-1">
              <h4 className="font-bold text-slate-800 text-sm">🔍 Hallucination Freedom (Weight: 30%)</h4>
              <span className="text-xs font-bold bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded">0 - 10</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Directly flags fabricated entities, counterfeit citations, or unsupported statements. Scored inversely (10 = Zero Hallucinations, 0 = Fully Fabricated).
            </p>
          </div>

          <div className="border border-slate-200 rounded-xl p-4 bg-slate-50/50">
            <div className="flex justify-between items-center mb-1">
              <h4 className="font-bold text-slate-800 text-sm">📋 Completeness (Weight: 15%)</h4>
              <span className="text-xs font-bold bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded">0 - 10</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Evaluates coverage breadth. Checks if essential facets, caveats, or mandatory multi-part criteria of the question were answered.
            </p>
          </div>
        </div>

        <div className="bg-indigo-50/70 border border-indigo-200/80 rounded-xl p-4 mt-3">
          <p className="text-xs font-bold uppercase tracking-wider text-indigo-800 mb-1">Verdict Aggregation Formula</p>
          <code className="text-xs font-mono text-indigo-950 font-semibold block">
            Overall Score = (Relevance × 0.25) + (Accuracy × 0.30) + (Hallucination × 0.30) + (Completeness × 0.15)
          </code>
          <p className="text-xs text-slate-600 mt-2">
            Verdict Tiers: <strong>9.0–10.0 (EXCELLENT)</strong> | <strong>7.0–8.9 (GOOD)</strong> | <strong>5.0–6.9 (ACCEPTABLE)</strong> | <strong>3.0–4.9 (POOR)</strong> | <strong>0.0–2.9 (DANGEROUS)</strong>
          </p>
        </div>
      </section>

      {/* 2. Hallucination Taxonomies */}
      <section className="space-y-3">
        <h3 className="text-lg font-bold text-slate-800 flex items-center gap-2 border-b border-slate-100 pb-2">
          <span>2.</span> Hallucination Taxonomies & Detection Strategies
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div className="border border-slate-200 rounded-lg p-3.5 bg-white">
            <span className="text-xs font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded">Intrinsic Hallucination</span>
            <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">
              The AI output directly contradicts information provided in the input source context (e.g. source says $100, AI says $500).
            </p>
          </div>
          <div className="border border-slate-200 rounded-lg p-3.5 bg-white">
            <span className="text-xs font-bold text-rose-700 bg-rose-50 px-2 py-0.5 rounded">Extrinsic Hallucination</span>
            <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">
              The output introduces external facts not mentioned or provable by the given reference material, leading to unverifiable claims.
            </p>
          </div>
          <div className="border border-slate-200 rounded-lg p-3.5 bg-white">
            <span className="text-xs font-bold text-red-700 bg-red-50 px-2 py-0.5 rounded">Factual Inversion</span>
            <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">
              The model asserts false real-world entities or claims (e.g., claiming a non-elected politician is Prime Minister).
            </p>
          </div>
        </div>
      </section>

      {/* 3. Existing Frameworks Comparison */}
      <section className="space-y-3">
        <h3 className="text-lg font-bold text-slate-800 flex items-center gap-2 border-b border-slate-100 pb-2">
          <span>3.</span> Framework Benchmark Analysis: RAGAS vs TruLens
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border border-slate-200 rounded-lg overflow-hidden">
            <thead className="bg-slate-100 text-slate-700 font-bold border-b border-slate-200">
              <tr>
                <th className="p-3">Framework</th>
                <th className="p-3">Primary Evaluation Metric</th>
                <th className="p-3">Key Strengths</th>
                <th className="p-3">Application in Our System</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-600">
              <tr>
                <td className="p-3 font-semibold text-slate-800">RAGAS</td>
                <td className="p-3 font-mono">Faithfulness = (Supported Claims / Total Claims)</td>
                <td className="p-3">Strict claim-level mathematical breakdown of context alignment.</td>
                <td className="p-3">Adopted in our Hallucination Detection & Accuracy Judge prompts.</td>
              </tr>
              <tr>
                <td className="p-3 font-semibold text-slate-800">TruLens</td>
                <td className="p-3">RAG Triad (Groundedness + QA Relevance + Context Relevance)</td>
                <td className="p-3">End-to-end feedback functions and application tracing.</td>
                <td className="p-3">Influenced our multi-agent parallel orchestrator structure.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* 4. Benchmark Datasets */}
      <section className="space-y-3">
        <h3 className="text-lg font-bold text-slate-800 flex items-center gap-2 border-b border-slate-100 pb-2">
          <span>4.</span> Reference Benchmark Datasets (Hugging Face)
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="border border-slate-200 rounded-xl p-4 bg-slate-50">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-base">🧪</span>
              <h4 className="font-bold text-slate-800 text-sm">TruthfulQA (Hugging Face)</h4>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Designed specifically to evaluate whether language models mimic human falsehoods and popular conspiracies. Contains 817 questions spanning health, law, finance, and science.
            </p>
            <div className="mt-2 text-xs font-mono text-slate-500">
              Used in: Seeding common misconception ground truths.
            </div>
          </div>

          <div className="border border-slate-200 rounded-xl p-4 bg-slate-50">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-base">📖</span>
              <h4 className="font-bold text-slate-800 text-sm">SQuAD 1.1 (Stanford Question Answering)</h4>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              100,000+ question-answer pairs grounded on Wikipedia passages. Ideal for testing factual reading comprehension, context chunking, and dense vector semantic retrieval.
            </p>
            <div className="mt-2 text-xs font-mono text-slate-500">
              Used in: RAG context grounding and semantic chunk retrieval.
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
