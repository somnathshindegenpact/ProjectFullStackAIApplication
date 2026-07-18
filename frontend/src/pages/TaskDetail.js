import React, { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import api from '../api'

export default function TaskDetail(){
  const { id } = useParams()
  const [task, setTask] = useState(null)
  const [aiResp, setAiResp] = useState(null)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => { load() }, [id])

  async function load(){
    const res = await api.fetchTask(id)
    if (res.msg && res.msg.toLowerCase().includes('unauthorized')) {
      navigate('/login'); return
    }
    if (res.id) {
      setTask(res)
    } else {
      setError(res.msg || 'Unable to load task')
    }
  }

  async function askAI(){
    if (!task) return
    const q = `Give prioritization suggestions for task: ${task.title} - ${task.description || ''}`
    const r = await api.askAI(q)
    setAiResp(r)
  }

  async function markComplete(){
    await api.updateTask(id, { status: 'completed' })
    load()
  }

  if (!task) return <div className='text-slate-700'>Loading...</div>

  return (
    <div className='space-y-6'>
      <div className='rounded-3xl bg-white p-4 shadow-sm sm:p-6'>
        <div className='flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between'>
          <div>
            <h2 className='text-2xl font-semibold text-slate-900'>{task.title}</h2>
            <p className='text-sm text-slate-500'>Status: {task.status.replace('_', ' ')} · Priority: {task.priority === 1 ? 'High' : task.priority === 2 ? 'Medium' : 'Low'}</p>
          </div>
          <div className='flex flex-wrap gap-3'>
            {task.status !== 'completed' && <button onClick={markComplete} className='rounded-2xl bg-emerald-600 px-4 py-2 text-sm font-semibold text-white hover:bg-emerald-700'>Mark complete</button>}
            <button onClick={() => navigate('/')} className='rounded-2xl border border-slate-200 px-4 py-2 text-sm text-slate-700 hover:bg-slate-50'>Back</button>
          </div>
        </div>
      </div>

      <div className='grid gap-6 md:grid-cols-2'>
        <div className='rounded-3xl bg-white p-4 shadow-sm sm:p-6'>
          <h3 className='text-lg font-semibold text-slate-900 mb-4'>Description</h3>
          <p className='text-slate-600'>{task.description || 'No description provided.'}</p>
        </div>
        <div className='rounded-3xl bg-white p-6 shadow-sm'>
          <h3 className='text-lg font-semibold text-slate-900 mb-4'>Task details</h3>
          <dl className='space-y-3 text-sm text-slate-600'>
            <div><dt className='font-semibold text-slate-800'>Due date</dt><dd>{task.due_date || 'None'}</dd></div>
            <div><dt className='font-semibold text-slate-800'>Priority</dt><dd>{task.priority === 1 ? 'High' : task.priority === 2 ? 'Medium' : 'Low'}</dd></div>
            <div><dt className='font-semibold text-slate-800'>Status</dt><dd>{task.status.replace('_', ' ')}</dd></div>
          </dl>
        </div>
      </div>

      <div className='rounded-3xl bg-white p-6 shadow-sm'>
        <h3 className='text-lg font-semibold text-slate-900 mb-4'>AI recommendations</h3>
        {error && <div className='mb-4 rounded-2xl bg-rose-100 px-4 py-3 text-rose-700'>{error}</div>}
        <button onClick={askAI} className='rounded-2xl bg-sky-600 px-5 py-3 text-white font-semibold hover:bg-sky-700 transition'>Ask AI</button>
        {aiResp && (
          <div className='mt-6 rounded-3xl border border-slate-200 bg-slate-50 p-5'>
            <h4 className='text-lg font-semibold text-slate-900 mb-3'>AI answer</h4>
            <pre className='whitespace-pre-wrap text-sm text-slate-700'>{aiResp.answer}</pre>
            <h5 className='mt-4 text-sm font-semibold text-slate-900'>Sources</h5>
            <ul className='mt-2 space-y-2 text-sm text-slate-700'>
              {aiResp.sources && aiResp.sources.map(s => <li key={s.id}>{s.title} ({s.score?.toFixed(3)})</li>)}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}
