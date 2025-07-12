import { useState, useEffect } from 'react';
import * as XLSX from 'xlsx';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid
} from 'recharts';

export default function KodeKloudDashboard({ user }) {
  const [data, setData] = useState([]);
  const [filter, setFilter] = useState('all');
  const [sortKey, setSortKey] = useState('Video Hours Watched');
  const [search, setSearch] = useState('');
  const [darkMode, setDarkMode] = useState(false);
  const licenseLimit = 40;

  useEffect(() => {
  document.title = "Kode Kloud License Usage";

  const fetchData = () => {
    fetch('https://stcloudkitdevcus.blob.core.windows.net/cloudkit-inputs/kodekloud_data.json?sp=r&st=2025-06-09T15:09:14Z&se=2026-02-28T23:09:14Z&sv=2024-11-04&sr=b&sig=An7b7jFr7Uh%2FnFYqoTaILe7eqw8usBFsY79QUh%2F7r2E%3D')
      .then(res => {
        if (!res.ok) throw new Error(`HTTP error ${res.status}`);
        return res.json();
      })
      .then(json => {
        const enriched = json.map(u => {
          const noActivity =
            (u['Lessons Completed'] === 0 || u['Lessons Completed'] === '0') &&
            (u['Video Hours Watched'] === 0 || u['Video Hours Watched'] === '0') &&
            (u['Labs Completed'] === 0 || u['Labs Completed'] === '0');
          return {
            ...u,
            Status: noActivity ? 'No activity or progress' : u.Status || '-',
          };
        });
        setData(enriched);
      })
      .catch(err => {
        console.error("Failed to fetch JSON:", err);
        alert("Failed to load data. Please check your Blob Storage CORS settings.");
      });
  };

  fetchData(); // Carga inicial
  const interval = setInterval(fetchData, 300 * 1000); // Cada 300 segundos

  return () => clearInterval(interval); // Cleanup al desmontar
}, []);

  const normalize = val => String(val).trim().toLowerCase();
  const isActive = user => normalize(user['License Accepted']) === '✓';
  const isNoActivity = user => normalize(user['Status']) === 'no activity or progress';

  const filteredAll = data.filter(user => user.Program !== 'LPC');
  const sorted = [...filteredAll].sort((a, b) => {
    if (sortKey === 'Name' || sortKey === 'Program') {
      return String(a[sortKey]).localeCompare(String(b[sortKey]));
    }
    return (b[sortKey] || 0) - (a[sortKey] || 0);
  });

  const filtered = sorted.filter(user => {
    if (filter === 'active') return isActive(user);
    if (filter === 'inactive') return !isActive(user) || isNoActivity(user);
    if (search && !user.Name.toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  const activeCount = filteredAll.filter(isActive).length;
  const noActivityCount = filteredAll.filter(isNoActivity).length;
  const averageVideoHours = (
    filteredAll.reduce((sum, user) => sum + parseFloat(user['Video Hours Watched'] || 0), 0) /
    filteredAll.length
  ).toFixed(1);

  const exportToExcel = () => {
    const ws = XLSX.utils.json_to_sheet(filtered);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Usage');
    XLSX.writeFile(wb, 'kodekloud_usage.xlsx');
  };

  const getTopLessons = (dataset, program = null) => {
    return dataset
      .filter(u => (program ? u.Program === program : true))
      .sort((a, b) => b['Lessons Completed'] - a['Lessons Completed'])
      .slice(0, 5)
      .map(u => ({ name: u.Name, value: u['Lessons Completed'] }));
  };

  const charts = [
    { title: 'Top 5 Users by Lessons', data: getTopLessons(data) },
    { title: 'Top 5 in XPORT1-MX', data: getTopLessons(data, 'XPORT1-MX') },
    { title: 'Top 5 in XPORT2-MX', data: getTopLessons(data, 'XPORT2-MX') },
    { title: 'Top 5 in MXEPAMGOOGLE', data: getTopLessons(data, 'MXEPAMGOOGLE') },
  ];

  const themeClasses = darkMode ? 'bg-gray-900 text-white' : 'bg-white text-gray-900';
  const cardTheme = darkMode ? 'bg-gray-800 text-white' : 'bg-gray-100 text-gray-900';
  const cardTitle = darkMode ? 'text-lg font-bold text-white' : 'text-lg font-bold text-gray-900';
  const chartTheme = darkMode ? 'bg-gray-800 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-900';
  const tableTheme = darkMode ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-100 hover:bg-gray-200';
  const inputTheme = darkMode ? 'bg-gray-800 text-white border-gray-600' : 'bg-white text-black border-gray-300';

  return (
    <div className={`min-h-screen ${themeClasses} p-4`}>
      <header className="bg-[#052E57] p-6 shadow mb-4 flex flex-wrap justify-between items-center text-white sticky top-0 z-10">
        <div className="flex items-center gap-4">
          <img
            src="https://www.epam.com/content/dam/epam/homepage/epam_logo_light.svg"
            alt="EPAM Logo"
            className="h-10 invert"
          />
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <input
            type="text"
            placeholder="Search by name..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className={`px-2 py-1 rounded ${inputTheme}`}
          />
          <select onChange={e => setSortKey(e.target.value)} className={`px-2 py-1 rounded ${inputTheme}`}>
            <option value="Video Hours Watched">Video Hours</option>
            <option value="Name">Name</option>
            <option value="Program">Program</option>
          </select>
          <button onClick={() => setFilter('all')} className="bg-[#0072CE] text-white px-3 py-1 rounded hover:bg-[#005fa3]">All</button>
          <button onClick={() => setFilter('active')} className="bg-[#0072CE] text-white px-3 py-1 rounded hover:bg-[#005fa3]">Active</button>
          <button onClick={() => setFilter('inactive')} className="bg-[#0072CE] text-white px-3 py-1 rounded hover:bg-[#005fa3]">Inactive</button>
          <button onClick={exportToExcel} className="bg-[#007A33] text-white px-3 py-1 rounded hover:bg-[#00662b]">Export to Excel</button>
          <button onClick={() => setDarkMode(!darkMode)} className="bg-gray-500 text-white px-3 py-1 rounded hover:bg-gray-600">
            {darkMode ? 'Light Mode' : 'Dark Mode'}
          </button>

          {user && (
            <div className="flex flex-col text-sm ml-4">
              <span>Hola, {user.user_claims?.find(c => c.typ === 'name')?.val || user.userDetails}</span>
              <span>{user.user_claims?.find(c => c.typ === 'preferred_username')?.val}</span>
              <a
                href={`https://login.microsoftonline.com/b41b72d0-4e9f-4c26-8a69-f949f367c91d/oauth2/v2.0/logout?post_logout_redirect_uri=${window.location.origin}/signed-out`}
                className="bg-red-600 text-white px-2 py-1 mt-1 rounded hover:bg-red-700 text-center"
              >
                Cerrar sesión
              </a>
            </div>
          )}
        </div>
      </header>


      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div className={`p-4 rounded-lg shadow hover:shadow-lg ${cardTheme}`}>
          <p className={`${cardTitle}`}>Total Users</p>
          <p className="text-3xl font-bold">{filteredAll.length}</p>
        </div>
        <div className={`p-4 rounded-lg shadow hover:shadow-lg ${cardTheme}`}>
          <p className={`${cardTitle}`}>Active Licenses</p>
          <p className="text-3xl font-bold">{activeCount} / {licenseLimit}</p>
        </div>
        <div className={`p-4 rounded-lg shadow hover:shadow-lg ${cardTheme}`}>
          <p className={`${cardTitle}`}>No Progress</p>
          <p className="text-3xl font-bold text-red-600 dark:text-red-400">{noActivityCount}</p>
        </div>
        <div className={`p-4 rounded-lg shadow hover:shadow-lg ${cardTheme}`}>
          <p className={`${cardTitle}`}>Avg. Video Hours</p>
          <p className="text-3xl font-bold">{averageVideoHours}</p>
        </div>
      </section>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6 px-4">
        {charts.map((chart, index) => (
          <section key={index} className={`p-6 rounded-md border ${chartTheme}`}>
            <h2 className="text-lg font-semibold mb-4">{chart.title}</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chart.data} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" stroke={darkMode ? '#fff' : '#000'} />
                <YAxis type="category" dataKey="name" width={150} stroke={darkMode ? '#fff' : '#000'} />
                <Tooltip />
                <Bar dataKey="value" fill="#0072CE" />
              </BarChart>
            </ResponsiveContainer>
          </section>
        ))}
      </div>

      <div className="overflow-x-auto px-4">
        <table className="min-w-full table-auto border border-gray-300">
          <thead className="bg-[#052E57] text-white">
            <tr>
              <th className="px-4 py-2">Name</th>
              <th className="px-4 py-2">Email</th>
              <th className="px-4 py-2">Lessons</th>
              <th className="px-4 py-2">Video Hours</th>
              <th className="px-4 py-2">Labs</th>
              <th className="px-4 py-2">Program</th>
              <th className="px-4 py-2">Active</th>
              <th className="px-4 py-2">Status</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((u, i) => (
              <tr
                key={i}
                className={
                  isNoActivity(u)
                    ? 'bg-red-100 text-red-900 hover:bg-red-200'
                    : !isActive(u)
                    ? 'bg-orange-100 text-orange-900 hover:bg-orange-200'
                    : i % 2 === 0
                    ? tableTheme
                    : tableTheme
                }
              >
                <td className="px-4 py-2 whitespace-nowrap">{u.Name}</td>
                <td className="px-4 py-2 whitespace-nowrap">{u.Email}</td>
                <td className="px-4 py-2 text-center">{u['Lessons Completed']}</td>
                <td className="px-4 py-2 text-center">{u['Video Hours Watched']}</td>
                <td className="px-4 py-2 text-center">{u['Labs Completed']}</td>
                <td className="px-4 py-2 text-center">{u.Program}</td>
                <td className="px-4 py-2 text-center">{isActive(u) ? '✔️' : '❌'}</td>
                <td className="px-4 py-2 text-center">{u.Status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <footer className="text-center mt-8 p-4 text-sm text-gray-500 border-t border-gray-300">
        Portal created by Luis Alvarez (luis_alvarez1@epam.com)
      </footer>
    </div>
  );
}
