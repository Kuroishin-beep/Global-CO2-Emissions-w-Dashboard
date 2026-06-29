import React from 'react';
import { NavLink } from 'react-router-dom';
import { useStore } from '../store';
import { useData } from '../hooks/useData';
import { LineChart, PieChart, BarChart2, Globe, TrendingUp, FlaskConical, Database, Info, Lightbulb } from 'lucide-react';

const navItems = [
  { path: '/overview', name: 'Overview', icon: <LineChart size={18} /> },
  { path: '/sources', name: 'Sources', icon: <PieChart size={18} /> },
  { path: '/comparison', name: 'Comparison', icon: <BarChart2 size={18} /> },
  { path: '/map', name: 'Map', icon: <Globe size={18} /> },
  { path: '/predictions', name: 'Predictions', icon: <TrendingUp size={18} /> },
  { path: '/analytics', name: 'Analytics', icon: <FlaskConical size={18} /> },
  { path: '/data', name: 'Data', icon: <Database size={18} /> },
  { path: '/insights', name: 'Insights', icon: <Lightbulb size={18} /> },
  { path: '/info', name: 'Info', icon: <Info size={18} /> },
];

export default function Sidebar() {
  const { data } = useData();
  const { selectedCountry, setSelectedCountry, yearRange, setYearRange } = useStore();

  const countries = data ? Object.keys(data).sort() : [];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col hidden md:flex">
      <div className="p-4 border-b border-slate-800">
        <h1 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-indigo-500 bg-clip-text text-transparent">
          CO₂ Dashboard
        </h1>
      </div>

      <nav className="flex-1 overflow-y-auto p-4 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                isActive
                  ? 'bg-indigo-500/10 text-indigo-400 font-medium'
                  : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800'
              }`
            }
          >
            {item.icon}
            {item.name}
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-slate-800 space-y-4">
        <h2 className="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-2">Controls</h2>
        
        <div className="space-y-1">
          <label className="text-sm text-slate-400">Country</label>
          <select 
            value={selectedCountry}
            onChange={(e) => setSelectedCountry(e.target.value)}
            className="w-full bg-slate-950 border border-slate-700 rounded-md p-2 text-sm text-slate-200 outline-none focus:border-indigo-500"
          >
            {countries.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>

        <div className="space-y-1">
          <label className="text-sm text-slate-400 flex justify-between">
            <span>Year</span>
            <span>{yearRange[0]} - {yearRange[1]}</span>
          </label>
          <div className="flex gap-2 items-center">
            <input 
              type="range" 
              min={1900} 
              max={2022} 
              value={yearRange[0]} 
              onChange={(e) => setYearRange([parseInt(e.target.value), yearRange[1]])}
              className="w-full accent-indigo-500"
            />
            <input 
              type="range" 
              min={1900} 
              max={2022} 
              value={yearRange[1]} 
              onChange={(e) => setYearRange([yearRange[0], parseInt(e.target.value)])}
              className="w-full accent-indigo-500"
            />
          </div>
        </div>
      </div>
    </aside>
  );
}
