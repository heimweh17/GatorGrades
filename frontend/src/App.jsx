import React, { useEffect, useState } from 'react'
import axios from 'axios'
import DistributionChart from './components/DistributionChart'
import TrendsChart from './components/TrendsChart'

export default function App() {
  const [courses, setCourses] = useState([])
  const [selected, setSelected] = useState(null)
  const [summary, setSummary] = useState(null)
  const [buckets, setBuckets] = useState([])
  const [trends, setTrends] = useState([])
  const [file, setFile] = useState(null)

  useEffect(() => {
    axios.get('/api/courses').then(res => setCourses(res.data.courses))
  }, [])

  useEffect(() => {
    if (!selected) return
    axios.get(`/api/courses/${selected}/summary`).then(res => setSummary(res.data))
    axios.get(`/api/courses/${selected}/distribution`).then(res => setBuckets(res.data.buckets))
    axios.get(`/api/courses/${selected}/trends`).then(res => setTrends(res.data.trends))
  }, [selected])

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!file) return
    const form = new FormData()
    form.append('file', file)
    await axios.post('/api/upload', form)
    // refresh
    const { data } = await axios.get('/api/courses')
    setCourses(data.courses)
  }

  return (
    <div style={{ maxWidth: 900, margin: '2rem auto', fontFamily: 'system-ui, Arial, sans-serif' }}>
      <h1>GatorGrades</h1>

      <form onSubmit={handleUpload} style={{ margin: '1rem 0' }}>
        <input type="file" accept=".csv" onChange={e => setFile(e.target.files?.[0])} />
        <button type="submit" style={{ marginLeft: 8 }}>Upload CSV</button>
      </form>

      <label style={{ display: 'block', marginTop: 12 }}>Select Course:</label>
      <select value={selected || ''} onChange={e => setSelected(Number(e.target.value) || null)}>
        <option value="">-- choose --</option>
        {courses.map(c => <option key={c.id} value={c.id}>{c.code} - {c.term}</option>)}
      </select>

      {summary && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem', marginTop: '1rem' }}>
          <Card title="Students" value={summary.students} />
          <Card title="Assignments" value={summary.assignments} />
          <Card title="Average %" value={summary.avg_pct.toFixed(1)} />
          <Card title="Median %" value={summary.median_pct.toFixed(1)} />
          <Card title="Std Dev %" value={summary.stddev_pct.toFixed(1)} />
          <Card title="Pass Rate %" value={summary.pass_rate_pct.toFixed(1)} />
        </div>
      )}

      <div style={{ marginTop: '2rem' }}>
        <h2>Distribution</h2>
        <DistributionChart data={buckets} />
      </div>
    
      <div style={{ marginTop: '2rem' }}>
        <h2>Trends</h2>
        <TrendsChart data={trends} />
      </div>
    </div>
  )
}

function Card({ title, value }) {
  return (
    <div style={{ border: '1px solid #ddd', borderRadius: 8, padding: 12 }}>
      <div style={{ fontSize: 12, color: '#666' }}>{title}</div>
      <div style={{ fontSize: 24, fontWeight: 600 }}>{value}</div>
    
      <div style={{ marginTop: '2rem' }}>
        <h2>Trends</h2>
        <TrendsChart data={trends} />
      </div>
    </div>
  )
}
