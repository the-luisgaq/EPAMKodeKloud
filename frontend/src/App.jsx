import { useEffect, useState } from 'react'
import './App.css'

export default function App() {
  const [data, setData] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/report/data')
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch')
        return res.json()
      })
      .then(setData)
      .catch(err => setError(err.message))
  }, [])

  if (error) return <div className="error">{error}</div>

  return (
    <main>
      <h1>Kode Kloud Report</h1>
      <table>
        <thead>
          <tr>
            {data[0] && Object.keys(data[0]).map(key => (
              <th key={key}>{key}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr key={idx}>
              {Object.values(row).map((val, i) => (
                <td key={i}>{val}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  )
}
