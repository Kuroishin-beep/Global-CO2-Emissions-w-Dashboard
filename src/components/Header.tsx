
import { useStore } from '../store';
import { useData } from '../hooks/useData';

export default function Header() {
  const { data, loading, error } = useData();
  const { selectedCountry, yearRange } = useStore();

  if (loading) return <header className="h-16 border-b border-slate-800 bg-slate-900/50 flex items-center px-8 text-slate-400">Loading data...</header>;
  if (error) return <header className="h-16 border-b border-slate-800 bg-slate-900/50 flex items-center px-8 text-red-400">Error: {error}</header>;

  const countryData = data?.[selectedCountry]?.data || [];
  const filtered = countryData.filter(d => d.year >= yearRange[0] && d.year <= yearRange[1]);
  
  const latest = filtered.length > 0 ? filtered[filtered.length - 1] : null;

  return (
    <header className="h-20 border-b border-slate-800 bg-slate-900/50 flex items-center px-4 lg:px-8 justify-between">
      <div>
        <h2 className="text-2xl font-semibold text-slate-100">{selectedCountry}</h2>
        <p className="text-sm text-slate-400">Global CO₂ Overview ({yearRange[0]} - {yearRange[1]})</p>
      </div>
      
      {latest && (
        <div className="flex gap-6">
          <div className="text-right">
            <div className="text-xs text-slate-400 uppercase tracking-wider">Total CO₂</div>
            <div className="text-lg font-medium text-cyan-400">{latest.co2?.toLocaleString() ?? 0} Mt</div>
          </div>
          <div className="text-right">
            <div className="text-xs text-slate-400 uppercase tracking-wider">Per Capita</div>
            <div className="text-lg font-medium text-indigo-400">{latest.co2_per_capita?.toFixed(2) ?? 0} t</div>
          </div>
          <div className="text-right hidden sm:block">
            <div className="text-xs text-slate-400 uppercase tracking-wider">Global Share</div>
            <div className="text-lg font-medium text-amber-400">{latest.share_global_co2?.toFixed(2) ?? 0}%</div>
          </div>
        </div>
      )}
    </header>
  );
}
