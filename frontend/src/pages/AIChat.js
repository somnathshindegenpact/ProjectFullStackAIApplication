import React, { useState } from 'react'
import api from '../api'

export default function AIChat(){
  const [query, setQuery] = useState('')
  const [resp, setResp] = useState(null)
  const [message, setMessage] = useState('')

  async function submit(e){
    e.preventDefault()
    if (!query.trim()) {
      setMessage('Please enter a question before asking AI.')
      return
    }
    setMessage('')
    const r = await api.askAI(query)
    setResp(r)
  }

  return (
    <div className='space-y-6'>
      <div className='rounded-3xl bg-white p-4 shadow-sm sm:p-6'>
        <h2 className='text-2xl font-semibold text-slate-900'>AI Chat & RAG</h2>
        <p className='mt-2 text-sm text-slate-500'>Ask the AI for task prioritization advice using your task data and document context.</p>
      </div>

      <div className='rounded-3xl bg-white p-4 shadow-sm sm:p-6'>
        {message && <div className='mb-4 rounded-2xl bg-rose-100 px-4 py-3 text-rose-700'>{message}</div>}
        <form onSubmit={submit} className='space-y-4'>
          <textarea rows={6} value={query} onChange={e => setQuery(e.target.value)} className='min-h-[180px] w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-4 text-slate-900 focus:border-sky-500 focus:outline-none sm:min-h-[220px]' placeholder='Ask the AI how to prioritize tasks, finish work faster, or plan your day.' />
          <button className='w-full rounded-2xl bg-sky-600 px-6 py-3 text-white font-semibold hover:bg-sky-700 transition sm:w-auto'>Ask AI</button>
        </form>
      </div>

      {resp && (
        <div className='rounded-3xl bg-white p-4 shadow-sm sm:p-6'>
          <h3 className='text-xl font-semibold text-slate-900 mb-4'>Answer</h3>
          <div className='rounded-3xl bg-slate-50 p-4 text-slate-700 whitespace-pre-wrap'>{resp.answer}</div>

          {resp.sources && resp.sources.length > 0 && (
            <div className='mt-6'>
              <h4 className='text-lg font-semibold text-slate-900 mb-3'>Sources</h4>
              <ul className='space-y-3 text-slate-700'>
                {resp.sources.map(s => (
                  <li key={s.id} className='rounded-2xl border border-slate-200 bg-white p-4'>
                    <div className='font-semibold text-slate-900'>{s.title || 'Untitled document'}</div>
                    <div className='text-sm text-slate-500 mt-1'>Score: {s.score?.toFixed(3)}</div>
                    <div className='mt-2 text-sm text-slate-600'>{s.content_snippet}</div>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
