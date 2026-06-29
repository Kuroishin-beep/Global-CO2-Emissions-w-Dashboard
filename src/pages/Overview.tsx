import React, { useState } from 'react';
import { useData } from '../hooks/useData';
import { useStore } from '../store';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function Overview() {
  const { data } = useData();
  const { selectedCountry, yearRange } = useStore();
  const [chartType, setChartType] = useState<'line' | 'area' | 'bar'>('line');

  const countryData = data?.[selectedCountry]?.data || [];
  const chartData = countryData.filter(d => d.year >= yearRange[0] && d.year <= yearRange[1]);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold text-slate-100">Historical CO₂</h2>
        <div className="flex bg-slate-900 rounded-lg p-1 border border-slate-800">
          {['line', 'area', 'bar'].map(t => (
            <button
              key={t}
              onClick={() => setChartType(t as any)}
              className={`px-3 py-1 text-sm rounded-md transition-colors capitalize ${
                chartType === t ? 'bg-indigo-500/20 text-indigo-400' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      <div className="h-[400px] bg-slate-900/30 border border-slate-800/50 rounded-xl p-4">
        <ResponsiveContainer width="100%" height="100%">
          {chartType === 'line' ? (
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="year" stroke="#64748b" fontSize={12} tickLine={false} />
              <YAxis stroke="#64748b" fontSize={12} tickLine={false} tickFormatter={(val) => `${val}Mt`} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '8px' }} />
              <Line type="monotone" dataKey="co2" stroke="#6366f1" strokeWidth={2} dot={false} />
            </LineChart>
          ) : chartType === 'area' ? (
            <AreaChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="year" stroke="#64748b" fontSize={12} tickLine={false} />
              <YAxis stroke="#64748b" fontSize={12} tickLine={false} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '8px' }} />
              <Area type="monotone" dataKey="co2" fill="#6366f1" stroke="#6366f1" fillOpacity={0.2} />
            </AreaChart>
          ) : (
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="year" stroke="#64748b" fontSize={12} tickLine={false} />
              <YAxis stroke="#64748b" fontSize={12} tickLine={false} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '8px' }} />
              <Bar dataKey="co2" fill="#6366f1" radius={[2, 2, 0, 0]} />
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>

      <h2 className="text-xl font-bold text-slate-100 pt-4">Growth Rate</h2>
      <div className="h-[300px] bg-slate-900/30 border border-slate-800/50 rounded-xl p-4">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="year" stroke="#64748b" fontSize={12} tickLine={false} />
            <YAxis stroke="#64748b" fontSize={12} tickLine={false} tickFormatter={(v) => `${v}%`} />
            <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '8px' }} />
            <Bar dataKey="co2_growth_prct" fill="#06b6d4">
              {
                chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.co2_growth_prct && entry.co2_growth_prct < 0 ? '#10b981' : '#ef4444'} />
                ))
              }
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
