
import { useData } from '../hooks/useData';
import { useStore } from '../store';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Analytics() {
  const { data } = useData();
  const { selectedCountry, yearRange } = useStore();

  const countryData = data?.[selectedCountry]?.data || [];
  const chartData = countryData.filter(d => d.year >= yearRange[0] && d.year <= yearRange[1] && d.gdp != null && d.co2 != null);

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-slate-100">Deep Analytics</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-slate-900/30 border border-slate-800/50 rounded-xl p-4">
          <h3 className="text-sm font-semibold text-slate-300 mb-4">CO₂ vs GDP</h3>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="gdp" type="number" stroke="#64748b" fontSize={12} tickLine={false} tickFormatter={v => `$${(v/1e9).toFixed(0)}B`} />
                <YAxis dataKey="co2" type="number" stroke="#64748b" fontSize={12} tickLine={false} tickFormatter={v => `${v}Mt`} />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '8px' }} />
                <Scatter data={chartData} fill="#06b6d4" />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-slate-900/30 border border-slate-800/50 rounded-xl p-4">
          <h3 className="text-sm font-semibold text-slate-300 mb-4">CO₂ vs Population</h3>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="population" type="number" stroke="#64748b" fontSize={12} tickLine={false} tickFormatter={v => `${(v/1e6).toFixed(0)}M`} />
                <YAxis dataKey="co2" type="number" stroke="#64748b" fontSize={12} tickLine={false} tickFormatter={v => `${v}Mt`} />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '8px' }} />
                <Scatter data={chartData} fill="#6366f1" />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
