
import React from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'

export default function TrendsChart({ data }) {
  // Expect data like [{ dueDate: '2025-09-10', title: 'HW1', avg_pct: 85 }, ...]
  const series = (data || []).map(d => ({
    ...d,
    x: d.dueDate || d.title,
    y: d.avg_pct
  }))

  return (
    <div style={{ width: '100%', height: 320 }}>
      <ResponsiveContainer>
        <LineChart data={series}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="x" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="y" dot />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
