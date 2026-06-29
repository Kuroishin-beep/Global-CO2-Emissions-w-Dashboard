
import { useData } from '../hooks/useData';
import { useStore } from '../store';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Predictions() {
  const { data } = useData();
  const { selectedCountry } = useStore();

  const countryData = data?.[selectedCountry]?.data || [];
  
  // Linear regression on last 20 years
  const recent = countryData.filter(d => d.co2 != null).slice(-20);
  
  let chartData: any[] = [];

  
  if (recent.length > 5) {
    const n = recent.length;
    const sumX = recent.reduce((sum, d) => sum + d.year, 0);
    const sumY = recent.reduce((sum, d) => sum + d.co2!, 0);
    const sumXY = recent.reduce((sum, d) => sum + d.year * d.co2!, 0);
    const sumXX = recent.reduce((sum, d) => sum + d.year * d.year, 0);
    
    const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;
    
    const lastYear = recent[recent.length - 1].year;
    
    chartData = recent.map(d => ({ year: d.year, historical: d.co2, predicted: null }));
    
    for (let y = lastYear + 1; y <= 2050; y += 1) {
      chartData.push({ year: y, historical: null, predicted: Math.max(0, slope * y + intercept) });
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-slate-100">Forecast</h2>
      <p className="text-sm text-slate-400">Simple linear regression projection based on the last 20 years.</p>
      
      {chartData.length > 0 ? (
        <div className="h-[450px] bg-slate-900/30 border border-slate-800/50 rounded-xl p-4">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="year" stroke="#64748b" fontSize={12} tickLine={false} />
              <YAxis stroke="#64748b" fontSize={12} tickLine={false} tickFormatter={v => `${Math.round(v)}Mt`} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '8px' }} />
              <Line type="monotone" dataKey="historical" stroke="#6366f1" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="predicted" stroke="#f59e0b" strokeWidth={2} strokeDasharray="5 5" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <div className="p-4 bg-slate-900 rounded-lg text-slate-400">Not enough data to project.</div>
      )}
    </div>
  );
}
