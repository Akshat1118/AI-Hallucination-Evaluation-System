import React from 'react'

export default function TechStackView() {
  const stack = [
    {
      category: 'API & Backend Framework',
      tech: 'FastAPI + Uvicorn',
      version: '0.163 / 0.42',
      badge: 'Python 3.13',
      desc: 'Asynchronous, high-throughput REST API with automated OpenAPI / Swagger documentation and background task workers.',
      icon: '⚡'
    },
    {
      category: 'LLM-as-a-Judge Engine',
      tech: 'Google Gemini API',
      version: 'gemini-2.5-flash / gemini-3.5',
      badge: 'google-genai SDK',
      desc: 'Powers the 4 specialized judge agents with calibrated prompt engineering, deterministic temperature (0.0), and JSON schemas.',
      icon: '🤖'
    },
    {
      category: 'Dense Vector Embeddings',
      tech: 'Sentence-Transformers',
      version: 'all-MiniLM-L6-v2',
      badge: '384-dimensional',
      desc: 'Local neural embedding model generating dense semantic representations for question context matching and similarity scoring.',
      icon: '🧬'
    },
    {
      category: 'Vector Database & Search',
      tech: 'ChromaDB (Persistent)',
      version: '1.5.5',
      badge: 'Cosine HNSW',
      desc: 'Embedded local vector store indexing reference chunks with metadata filtering for fast k-nearest-neighbors RAG retrieval.',
      icon: '🗄️'
    },
    {
      category: 'Database & ORM',
      tech: 'SQLite + SQLAlchemy 2.0',
      version: 'aiosqlite async driver',
      badge: 'Relational Store',
      desc: 'Stores input submissions, agent trace outputs, execution timestamps, and structured evaluation results.',
      icon: '💾'
    },
    {
      category: 'Benchmark Knowledge Base',
      tech: 'Hugging Face Datasets',
      version: 'TruthfulQA + SQuAD',
      badge: 'Ground Truth',
      desc: 'Standardized QA corpora ingested, chunked (512 chars with 50-char overlap), and indexed to provide factual evidence for judges.',
      icon: '📚'
    },
    {
      category: 'Frontend Client',
      tech: 'React 18 + Vite + TailwindCSS',
      version: 'Vite 6 / React 18.3',
      badge: 'Light Theme UI',
      desc: 'Interactive evaluation dashboard featuring real-time polling, preset samples, animated score breakdowns, and research views.',
      icon: '💻'
    },
    {
      category: 'Validation & Schemas',
      tech: 'Pydantic v2',
      version: '2.12.5',
      badge: 'Data Contracts',
      desc: 'Strict request payload validation, input sanitization, and typing guarantees across API boundaries.',
      icon: '🛡️'
    }
  ]

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-8 space-y-6">
      <div>
        <span className="text-xs font-bold text-teal-600 uppercase tracking-wider bg-teal-50 border border-teal-200 px-2.5 py-1 rounded-full">
          System Infrastructure
        </span>
        <h2 className="text-2xl font-extrabold text-slate-900 mt-2">
          Technology Stack Architecture
        </h2>
        <p className="text-slate-500 text-sm mt-1">
          Detailed overview of libraries, frameworks, models, and databases powering Milestone 1.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {stack.map((item, idx) => (
          <div key={idx} className="border border-slate-200 rounded-xl p-5 bg-slate-50/50 hover:bg-slate-50 transition">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-2.5">
                <span className="text-2xl">{item.icon}</span>
                <div>
                  <h4 className="font-bold text-slate-900 text-sm">{item.tech}</h4>
                  <p className="text-xs text-slate-500 font-medium">{item.category}</p>
                </div>
              </div>
              <span className="text-xs font-mono font-semibold bg-white border border-slate-200 text-slate-700 px-2 py-0.5 rounded shadow-2xs">
                {item.badge}
              </span>
            </div>
            <p className="text-xs text-slate-600 mt-3 leading-relaxed">
              {item.desc}
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}
