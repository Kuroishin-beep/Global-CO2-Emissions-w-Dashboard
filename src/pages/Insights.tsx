import { useState } from 'react';
import { useStore } from '../store';
import { useData } from '../hooks/useData';

export default function Insights() {
  const { selectedCountry } = useStore();
  const { data } = useData();
  const [insight, setInsight] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const generateInsight = async () => {
    setLoading(true);
    setInsight(null);
    try {
      const countryData = data?.[selectedCountry]?.data || [];
      const latest = countryData[countryData.length - 1];
      
      const response = await fetch("/api/insights", {
        headers: { "Content-Type": "application/json" },
        method: "POST",
        body: JSON.stringify({ 
          country: selectedCountry, 
          year: latest?.year || 2022, 
          co2: latest?.co2 || 0 
        }),
      });
      
      if (!response.ok) throw new Error("Failed");
      const result = await response.json();
      setInsight(result.insight || "Error make thought.");
    } catch {
      setInsight("Brain hurt. No think now.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl space-y-6">
      <h2 className="text-2xl font-bold text-slate-100">AI Insights</h2>
      <p className="text-sm text-slate-400">Ask AI about {selectedCountry}. (Caveman speech mode)</p>
      
      <button 
        onClick={generateInsight}
        disabled={loading}
        className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-medium transition-colors disabled:opacity-50"
      >
        {loading ? 'Thinking...' : 'Make Insight'}
      </button>

      {insight && (
        <div className="mt-6 p-6 bg-slate-900 border border-indigo-500/30 rounded-xl">
          <p className="text-lg text-slate-200 font-mono">"{insight}"</p>
        </div>
      )}
      
      <div className="mt-8 text-xs text-slate-500">
        Note: To use real AI insights, configure OPENROUTER_API_KEY in your backend environment.
      </div>
    </div>
  );
}
