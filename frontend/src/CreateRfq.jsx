import { useState } from 'react'

export default function CreateRfq() {
  const [message, setMessage] = useState('')

  async function submit(e) {
    e.preventDefault()
    const form = e.target
    const data = Object.fromEntries(new FormData(form))
    for (const key of ['bid_start', 'bid_close', 'forced_close']) {
      data[key] = new Date(data[key]).toISOString()
    }
    try {
      const res = await fetch('/api/rfqs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      const body = await res.json()
      if (!res.ok) return setMessage(body.detail.map((d) => d.msg.replace('Value error, ', '')).join(', '))
      form.reset()
      setMessage(`RFQ #${body.id} created`)
    } catch {
      setMessage('Could not create RFQ')
    }
  }

  return (
    <form onSubmit={submit}>
      <h2>Create RFQ</h2>
      <label>RFQ name / reference ID <input name="name" required /></label>
      <label>Bid start <input name="bid_start" type="datetime-local" required /></label>
      <label>Bid close <input name="bid_close" type="datetime-local" required /></label>
      <label>Forced bid close <input name="forced_close" type="datetime-local" required /></label>
      <label>Pickup / service date <input name="service_date" type="date" required /></label>
      <label>Trigger window (X minutes) <input name="trigger_window" type="number" min="1" max="1440" defaultValue="10" required /></label>
      <label>Extension duration (Y minutes) <input name="extension_duration" type="number" min="1" max="1440" defaultValue="5" required /></label>
      <label>
        Extension trigger{' '}
        <select name="trigger_type">
          <option value="BID_RECEIVED">Bid received</option>
          <option value="RANK_CHANGE">Any rank change</option>
          <option value="L1_CHANGE">L1 change</option>
        </select>
      </label>
      <button>Create</button>
      {message && <p role="status">{message}</p>}
    </form>
  )
}
