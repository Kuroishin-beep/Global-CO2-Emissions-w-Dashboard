import React from 'react';
import { useData } from '../hooks/useData';
import { useStore } from '../store';

export default function DataPage() {
  const { data } = useData();
  const { selectedCountry, yearRange } = useStore();

  const countryData = data?.[selectedCountry]?.data || [];
  const displayData = countryData.filter(d => d.year >= yearRange[0] && d.year <= yearRange[1]).reverse();

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold text-slate-100">Raw Data</h2>
        <div className="text-sm text-slate-400">{displayData.length} rows</div>
      </div>
      
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="text-xs text-slate-400 uppercase bg-slate-900/50 border-b border-slate-800">
            <tr>
              <th className="px-4 py-3">Year</th>
              <th className="px-4 py-3">CO₂ (Mt)</th>
              <th className="px-4 py-3">Per Capita (t)</th>
              <th className="px-4 py-3">GDP ($)</th>
              <th className="px-4 py-3">Population</th>
            </tr>
          </thead>
          <tbody>
            {displayData.map(row => (
              <tr key={row.year} className="border-b border-slate-800/50 hover:bg-slate-800/20">
                <td className="px-4 py-2 font-medium">{row.year}</td>
                <td className="px-4 py-2 text-cyan-400">{row.co2 ?? '-'}</td>
                <td className="px-4 py-2 text-indigo-400">{row.co2_per_capita ?? '-'}</td>
                <td className="px-4 py-2">{row.gdp ? (row.gdp / 1e9).toFixed(2) + 'B' : '-'}</td>
                <td className="px-4 py-2">{row.population ? (row.population / 1e6).toFixed(2) + 'M' : '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
