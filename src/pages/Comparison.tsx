
import { useData } from '../hooks/useData';
import { useStore } from '../store';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const COLORS = ['#6366f1', '#ef4444', '#06b6d4', '#f59e0b', '#10b981', '#8b5cf6'];

export default function Comparison() {
  const { data } = useData();
  const { selectedCountry, compareCountries, yearRange, setCompareCountries } = useStore();

  const countries = data ? Object.keys(data).sort() : [];
  const allCompare = [selectedCountry, ...compareCountries];

  // Merge data for the chart
  // Recharts line chart wants: [{ year: 2000, USA: 500, China: 800 }, ...]
  const years = Array.from({ length: yearRange[1] - yearRange[0] + 1 }, (_, i) => yearRange[0] + i);
  
  const chartData = years.map(y => {
    const row: any = { year: y };
    allCompare.forEach(c => {
      const cData = data?.[c]?.data.find(d => d.year === y);
      if (cData) row[c] = cData.co2;
    });
    return row;
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <h2 className="text-xl font-bold text-slate-100">Country Compare</h2>
        <div className="w-full sm:w-96">
          <label className="block text-xs text-slate-400 mb-1">Add Countries</label>
          <select 
            className="w-full bg-slate-900 border border-slate-700 rounded-md p-2 text-sm text-slate-200"
            onChange={(e) => {
              if (e.target.value && !compareCountries.includes(e.target.value)) {
                setCompareCountries([...compareCountries, e.target.value]);
              }
              e.target.value = '';
            }}
            value=""
          >
            <option value="">Select country...</option>
            {countries.filter(c => !allCompare.includes(c)).map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
      </div>

      <div className="flex gap-2 flex-wrap">
        {compareCountries.map(c => (
          <div key={c} className="bg-slate-800 px-3 py-1 rounded-full text-sm flex items-center gap-2">
            {c}
            <button 
              onClick={() => setCompareCountries(compareCountries.filter(x => x !== c))}
              className="text-slate-400 hover:text-red-400"
            >
              ×
            </button>
          </div>
        ))}
      </div>

      <div className="h-[500px] bg-slate-900/30 border border-slate-800/50 rounded-xl p-4">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="year" stroke="#64748b" fontSize={12} tickLine={false} />
            <YAxis stroke="#64748b" fontSize={12} tickLine={false} tickFormatter={(val) => `${val}Mt`} />
            <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '8px' }} />
            {allCompare.map((c, i) => (
              <Line key={c} type="monotone" dataKey={c} stroke={COLORS[i % COLORS.length]} strokeWidth={2} dot={false} />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
