import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api'

export default function Login(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState('info')
  const [mode, setMode] = useState('login')
  const [token, setToken] = useState('')
  const [resetRequested, setResetRequested] = useState(false)
  const navigate = useNavigate()

  const submit = async (e) => {
    e.preventDefault()
    if (mode === 'forgot') {
      if (!email.trim()) {
        setMessageType('error')
        setMessage('Please enter your email address.')
        return
      }

      setMessageType('info')
      setMessage('Sending reset instructions...')

      try {
        const res = await api.forgotPassword(email)
        const success = Boolean(res && res.msg && res.msg.toLowerCase().includes('sent'))
        setMessageType(success ? 'success' : 'error')
        setMessage(success
          ? 'Reset instructions were sent. Please check your email and use the token shown there to continue.'
          : res?.msg || 'Unable to process your request right now.')
        setResetRequested(true)
        if (success) {
          setMode('reset')
        }
      } catch (error) {
        setMessageType('error')
        setMessage('Unable to reach the server right now. Please try again in a moment.')
      }
      return
    }

    if (mode === 'reset') {
      if (!token.trim() || !password.trim()) {
        setMessageType('error')
        setMessage('Please enter both a reset token and a new password.')
        return
      }
      try {
        const res = await api.resetPassword(token, password)
        const isSuccess = Boolean(res && res.msg && res.msg.toLowerCase().includes('success'))
        setMessageType(isSuccess ? 'success' : 'error')
        setMessage(isSuccess
          ? 'Password updated successfully. You can now log in with your new password.'
          : res?.msg || 'Unable to reset your password right now. Please check the token and try again.')
        if (isSuccess) {
          setMode('login')
          setPassword('')
          setToken('')
          setResetRequested(false)
        }
      } catch (error) {
        setMessageType('error')
        setMessage('Unable to reset your password right now. Please try again in a moment.')
      }
      return
    }

    if (!email.trim() || !password.trim()) {
      setMessageType('error')
      setMessage('Please enter both email and password.')
      return
    }

    const res = await api.login(email, password)
    if (res.access_token) {
      localStorage.setItem('access_token', res.access_token)
      navigate('/')
    } else {
      setMessageType('error')
      const detail = res._url ? `${res.msg || 'Login failed. Please try again.'} (${res._url})` : (res.msg || 'Login failed. Please try again.')
      setMessage(detail)
    }
  }

  const switchMode = (nextMode) => {
    setMode(nextMode)
    setMessage('')
    setMessageType('info')
    if (nextMode !== 'reset') {
      setResetRequested(false)
    }
  }

  return (
    <div className='flex min-h-screen items-center justify-center bg-slate-50 p-4 sm:p-6'>
      <div className='w-full max-w-md rounded-3xl bg-white p-6 shadow-xl sm:p-8'>
        <h1 className='text-3xl font-semibold text-slate-900 mb-3'>Welcome back</h1>
        <p className='text-sm text-slate-500 mb-6'>Log in to manage tasks, set priorities, and get AI recommendations.</p>

        {message && <div className={`mb-4 rounded-2xl px-4 py-3 ${messageType === 'success' ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'}`}>{message}</div>}

        <div className='mb-4 flex flex-wrap gap-2'>
          <button type='button' onClick={() => switchMode('login')} className={`rounded-full px-3 py-2 text-sm font-semibold ${mode === 'login' ? 'bg-sky-600 text-white' : 'bg-slate-100 text-slate-700'}`}>Login</button>
          <button type='button' onClick={() => switchMode('forgot')} className={`rounded-full px-3 py-2 text-sm font-semibold ${mode === 'forgot' ? 'bg-sky-600 text-white' : 'bg-slate-100 text-slate-700'}`}>Forgot password</button>
          <button type='button' onClick={() => switchMode('reset')} className={`rounded-full px-3 py-2 text-sm font-semibold ${mode === 'reset' ? 'bg-sky-600 text-white' : 'bg-slate-100 text-slate-700'}`}>Reset password</button>
        </div>

        {mode === 'forgot' && (
          <div className='mb-4 rounded-2xl border border-sky-100 bg-sky-50 px-4 py-3 text-sm text-sky-700'>Enter your email address. After the reset instructions are sent, return here and use the token from your email.</div>
        )}

        {mode === 'reset' && (
          <div className='mb-4 rounded-2xl border border-sky-100 bg-sky-50 px-4 py-3 text-sm text-sky-700'>Use the reset token from your email and choose a new password below.</div>
        )}

        <form onSubmit={submit} className='space-y-4'>
          <div>
            <label className='block text-sm font-medium text-slate-700 mb-2'>Email</label>
            <input type='email' value={email} onChange={e => setEmail(e.target.value)} className='w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 focus:border-sky-500 focus:outline-none' placeholder='you@example.com' />
          </div>

          {mode !== 'forgot' && (
            <div>
              <label className='block text-sm font-medium text-slate-700 mb-2'>{mode === 'reset' ? 'New password' : 'Password'}</label>
              <input type='password' value={password} onChange={e => setPassword(e.target.value)} className='w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 focus:border-sky-500 focus:outline-none' placeholder='••••••••' />
            </div>
          )}

          {mode === 'reset' && (
            <div>
              <label className='block text-sm font-medium text-slate-700 mb-2'>Reset token</label>
              <input type='text' value={token} onChange={e => setToken(e.target.value)} className='w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 focus:border-sky-500 focus:outline-none' placeholder='Paste the reset token' />
            </div>
          )}

          <button type='submit' className='w-full rounded-2xl bg-sky-600 px-4 py-3 text-base font-semibold text-white hover:bg-sky-700 transition'>
            {mode === 'forgot' ? 'Send reset link' : mode === 'reset' ? 'Reset password' : 'Log in'}
          </button>
        </form>

        <p className='mt-6 text-center text-sm text-slate-500'>New user? <button onClick={() => navigate('/register')} className='font-semibold text-sky-600 hover:text-sky-700'>Create an account</button></p>
      </div>
    </div>
  )
}
