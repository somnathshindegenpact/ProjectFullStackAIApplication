import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../api'

const priorityStyles = {
  1: 'bg-red-100 text-red-700',
  2: 'bg-orange-100 text-orange-700',
  3: 'bg-slate-100 text-slate-700'
}

const statusStyles = {
  todo: 'bg-sky-100 text-sky-700',
  in_progress: 'bg-amber-100 text-amber-700',
  completed: 'bg-emerald-100 text-emerald-700'
}

export default function Dashboard(){
  const [tasks, setTasks] = useState([])
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [dueDate, setDueDate] = useState('')
  const [priority, setPriority] = useState(2)
  const [status, setStatus] = useState('todo')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => { load() }, [])

  async function load(){
    const res = await api.fetchTasks()
    if (res.msg && res.msg.toLowerCase().includes('unauthorized')) { navigate('/login'); return }
    if (Array.isArray(res)) {
      setTasks(res)
      setError('')
    } else {
      setError(res.msg || 'Unable to load tasks')
    }
  }

  async function add(e){
    e.preventDefault()
    if (!title) return
    const payload = { title, description, due_date: dueDate, priority: Number(priority), status }
    const res = await api.createTask(payload)
    if (res.id) {
      setTitle('')
      setDescription('')
      setDueDate('')
      setPriority(2)
      setStatus('todo')
      load()
    } else {
      setError(res.msg || 'Task create failed')
    }
  }

  async function completeTask(id){
    await api.updateTask(id, { status: 'completed' })
    load()
  }

  async function deleteTask(id){
    await api.deleteTask(id)
    load()
  }

  return (
    <div className='space-y-6 sm:space-y-8'>
      <div className='rounded-3xl bg-white p-4 shadow-sm sm:p-6'>
        <div className='flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between'>
          <div>
            <h2 className='text-2xl font-semibold text-slate-900'>Task Pro</h2>
            <p className='text-sm text-slate-500'>Manage high/medium/low priority tasks, due dates, and AI support.</p>
          </div>
          <Link to='/ai' className='inline-flex items-center justify-center rounded-full bg-sky-600 px-5 py-3 text-white hover:bg-sky-700 transition'>AI Chat</Link>
        </div>
      </div>

      <div className='grid gap-6 lg:grid-cols-[1.2fr_0.8fr]'>
        <section className='rounded-3xl bg-white p-4 shadow-sm sm:p-6'>
          <h3 className='text-xl font-semibold text-slate-900 mb-4'>Create task</h3>
          {error && <div className='mb-4 rounded-2xl bg-rose-100 px-4 py-3 text-rose-700'>{error}</div>}
          <form className='space-y-4' onSubmit={add}>
            <div>
              <label className='block text-sm font-medium text-slate-700 mb-2'>Task name</label>
              <input value={title} onChange={e => setTitle(e.target.value)} className='w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 focus:border-sky-500 focus:outline-none' placeholder='Enter task name' />
            </div>
            <div>
              <label className='block text-sm font-medium text-slate-700 mb-2'>Description</label>
              <textarea value={description} onChange={e => setDescription(e.target.value)} rows={4} className='w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 focus:border-sky-500 focus:outline-none' placeholder='Optional task details' />
            </div>
            <div className='grid gap-4 sm:grid-cols-2'>
              <div>
                <label className='block text-sm font-medium text-slate-700 mb-2'>Priority</label>
                <select value={priority} onChange={e => setPriority(e.target.value)} className='w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 focus:border-sky-500 focus:outline-none'>
                  <option value={1}>High</option>
                  <option value={2}>Medium</option>
                  <option value={3}>Low</option>
                </select>
              </div>
              <div>
                <label className='block text-sm font-medium text-slate-700 mb-2'>Due date</label>
                <input type='date' value={dueDate} onChange={e => setDueDate(e.target.value)} className='w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 focus:border-sky-500 focus:outline-none' />
              </div>
            </div>
            <div>
              <label className='block text-sm font-medium text-slate-700 mb-2'>Status</label>
              <select value={status} onChange={e => setStatus(e.target.value)} className='w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 focus:border-sky-500 focus:outline-none'>
                <option value='todo'>Todo</option>
                <option value='in_progress'>In progress</option>
                <option value='completed'>Completed</option>
              </select>
            </div>
            <button type='submit' className='w-full rounded-2xl bg-emerald-600 px-5 py-3 text-white font-semibold hover:bg-emerald-700 transition sm:w-auto'>Create task</button>
          </form>
        </section>

        <section className='rounded-3xl bg-white p-4 shadow-sm sm:p-6'>
          <h3 className='text-xl font-semibold text-slate-900 mb-4'>Task tips</h3>
          <div className='space-y-3 text-sm text-slate-600'>
            <p>Use high priority for urgent tasks, medium for important but not urgent tasks, and low for backlog items.</p>
            <p>Update status when work begins, and mark complete once finished.</p>
            <p>AI chat can help you prioritize tasks and plan your day.</p>
          </div>
        </section>
      </div>

      <section className='rounded-3xl bg-white p-4 shadow-sm sm:p-6'>
        <h3 className='text-xl font-semibold text-slate-900 mb-4'>Task list</h3>
        <div className='hidden overflow-x-auto md:block'>
          <table className='min-w-full divide-y divide-slate-200'>
            <thead>
              <tr className='bg-slate-50'>
                <th className='px-4 py-3 text-left text-sm font-semibold text-slate-700'>Task</th>
                <th className='px-4 py-3 text-left text-sm font-semibold text-slate-700'>Priority</th>
                <th className='px-4 py-3 text-left text-sm font-semibold text-slate-700'>Due</th>
                <th className='px-4 py-3 text-left text-sm font-semibold text-slate-700'>Status</th>
                <th className='px-4 py-3 text-left text-sm font-semibold text-slate-700'>Actions</th>
              </tr>
            </thead>
            <tbody className='divide-y divide-slate-200'>
              {tasks.map(task => (
                <tr key={task.id}>
                  <td className='px-4 py-4'>
                    <div className='font-semibold text-slate-900'>{task.title}</div>
                    <div className='text-sm text-slate-500'>{task.description || 'No description'}</div>
                  </td>
                  <td className='px-4 py-4'>
                    <span className={`inline-flex rounded-full px-3 py-1 text-sm font-semibold ${priorityStyles[task.priority]}`}>
                      {task.priority === 1 ? 'High' : task.priority === 2 ? 'Medium' : 'Low'}
                    </span>
                  </td>
                  <td className='px-4 py-4 text-sm text-slate-600'>{task.due_date || 'No due date'}</td>
                  <td className='px-4 py-4'>
                    <span className={`inline-flex rounded-full px-3 py-1 text-sm font-semibold ${statusStyles[task.status] || 'bg-slate-100 text-slate-700'}`}>
                      {task.status.replace('_', ' ')}
                    </span>
                  </td>
                  <td className='px-4 py-4'>
                    <div className='flex flex-wrap gap-2'>
                      <Link to={`/tasks/${task.id}`} className='rounded-2xl border border-slate-200 px-3 py-2 text-sm text-slate-700 hover:bg-slate-50'>Details</Link>
                      {task.status !== 'completed' && <button onClick={() => completeTask(task.id)} className='rounded-2xl bg-emerald-600 px-3 py-2 text-sm font-semibold text-white hover:bg-emerald-700'>Complete</button>}
                      <button onClick={() => deleteTask(task.id)} className='rounded-2xl border border-rose-200 px-3 py-2 text-sm text-rose-700 hover:bg-rose-50'>Delete</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className='space-y-3 md:hidden'>
          {tasks.map(task => (
            <div key={task.id} className='rounded-2xl border border-slate-200 bg-slate-50 p-4'>
              <div className='flex items-start justify-between gap-2'>
                <div>
                  <div className='font-semibold text-slate-900'>{task.title}</div>
                  <div className='mt-1 text-sm text-slate-500'>{task.description || 'No description'}</div>
                </div>
                <span className={`inline-flex rounded-full px-3 py-1 text-sm font-semibold ${priorityStyles[task.priority]}`}>
                  {task.priority === 1 ? 'High' : task.priority === 2 ? 'Medium' : 'Low'}
                </span>
              </div>
              <div className='mt-3 flex flex-wrap items-center gap-2 text-sm text-slate-600'>
                <span className='rounded-full bg-white px-3 py-1'>Due: {task.due_date || 'None'}</span>
                <span className={`rounded-full px-3 py-1 ${statusStyles[task.status] || 'bg-slate-100 text-slate-700'}`}>
                  {task.status.replace('_', ' ')}
                </span>
              </div>
              <div className='mt-4 flex flex-wrap gap-2'>
                <Link to={`/tasks/${task.id}`} className='rounded-2xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700'>Details</Link>
                {task.status !== 'completed' && <button onClick={() => completeTask(task.id)} className='rounded-2xl bg-emerald-600 px-3 py-2 text-sm font-semibold text-white'>Complete</button>}
                <button onClick={() => deleteTask(task.id)} className='rounded-2xl border border-rose-200 bg-white px-3 py-2 text-sm text-rose-700'>Delete</button>
              </div>
            </div>
          ))}
        </div>

        {tasks.length === 0 && <div className='mt-6 rounded-2xl border border-slate-200 bg-slate-50 p-6 text-slate-600'>No tasks yet. Add your first task to begin.</div>}
      </section>
    </div>
  )
}
