import React, { useState } from 'react';
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
      // Build prompt
      const countryData = data?.[selectedCountry]?.data || [];
      const latest = countryData[countryData.length - 1];
      const prompt = `Analyze CO2 for ${selectedCountry}. In ${latest?.year}, it was ${latest?.co2} Mt. Talk like caveman. Short. Efficient.`;

      // Since we don't have a real API key in the environment to avoid exposing it,
      // we mock the Hugging Face API call for the frontend unless the user configures VITE_HF_API_KEY.
      // Recommended model: TinyLlama/TinyLlama-1.1B-Chat-v1.0
      
      const apiKey = import.meta.env.VITE_HF_API_KEY;
      
      if (!apiKey) {
        // Fallback mock caveman speech if no API key
        setTimeout(() => {
          let text = `${selectedCountry} make much fire in ${latest?.year}. ${latest?.co2} big smoke. Earth get hot. Must stop fire. Use sun. Use wind.`;
          if ((latest?.co2 || 0) < 50) text = `${selectedCountry} make small fire. Only ${latest?.co2} smoke. Good. Keep air clean.`;
          setInsight(text);
          setLoading(false);
        }, 1500);
        return;
      }

      const response = await fetch(
        "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        {
          headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
          method: "POST",
          body: JSON.stringify({ inputs: `<|system|>\nYou are caveman. Speak short.\n<|user|>\n${prompt}\n<|assistant|>` }),
        }
      );
      
      const result = await response.json();
      setInsight(result[0]?.generated_text?.split('<|assistant|>')[1]?.trim() || "Error make thought.");
    } catch (e) {
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
        Note: To use real Hugging Face model, add VITE_HF_API_KEY to your .env file.
      </div>
    </div>
  );
}
