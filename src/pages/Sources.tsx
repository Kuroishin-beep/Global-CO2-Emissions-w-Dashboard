import React from 'react';
import { useData } from '../hooks/useData';
import { useStore } from '../store';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Sources() {
  const { data } = useData();
  const { selectedCountry, yearRange } = useStore();

  const countryData = data?.[selectedCountry]?.data || [];
  const chartData = countryData.filter(d => d.year >= yearRange[0] && d.year <= yearRange[1]);

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-slate-100">CO₂ Sources</h2>
      
      <div className="h-[450px] bg-slate-900/30 border border-slate-800/50 rounded-xl p-4">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} stackOffset="expand">
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="year" stroke="#64748b" fontSize={12} tickLine={false} />
            <YAxis stroke="#64748b" fontSize={12} tickLine={false} tickFormatter={(v) => `${(v * 100).toFixed(0)}%`} />
            <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '8px' }} />
            <Area type="monotone" dataKey="coal_co2" stackId="1" stroke="#334155" fill="#334155" name="Coal" />
            <Area type="monotone" dataKey="oil_co2" stackId="1" stroke="#ef4444" fill="#ef4444" name="Oil" />
            <Area type="monotone" dataKey="gas_co2" stackId="1" stroke="#06b6d4" fill="#06b6d4" name="Gas" />
            <Area type="monotone" dataKey="cement_co2" stackId="1" stroke="#94a3b8" fill="#94a3b8" name="Cement" />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4">
        {[
          { key: 'coal_co2', name: 'Coal', color: '#334155' },
          { key: 'oil_co2', name: 'Oil', color: '#ef4444' },
          { key: 'gas_co2', name: 'Gas', color: '#06b6d4' },
          { key: 'cement_co2', name: 'Cement', color: '#94a3b8' }
        ].map(src => (
          <div key={src.key} className="bg-slate-900/30 border border-slate-800/50 p-4 rounded-xl">
            <h3 className="text-slate-400 text-sm">{src.name} Trend</h3>
            <div className="h-24 mt-2">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData}>
                  <Area type="monotone" dataKey={src.key} stroke={src.color} fill={src.color} fillOpacity={0.2} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
