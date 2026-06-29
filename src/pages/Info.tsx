

export default function Info() {
  return (
    <div className="max-w-2xl space-y-6">
      <h2 className="text-2xl font-bold text-slate-100">About this App</h2>
      
      <div className="prose prose-invert prose-slate">
        <p className="text-slate-300">
          This dashboard shows global CO₂ emissions data over time. It was rebuilt from Streamlit to a sleek React (Vite) app for better performance and speed.
        </p>
        
        <h3 className="text-xl font-semibold mt-6 text-slate-200">Data Source</h3>
        <p className="text-slate-300">
          Data comes from Our World in Data. It tracks emissions, GDP, and population from 1900 to 2022.
        </p>

        <h3 className="text-xl font-semibold mt-6 text-slate-200">Metrics</h3>
        <ul className="list-disc pl-5 space-y-2 text-slate-300">
          <li><strong>Mt:</strong> Million Metric Tonnes</li>
          <li><strong>Per Capita:</strong> Tonnes per person</li>
          <li><strong>Global Share:</strong> Percentage of world emissions</li>
        </ul>
      </div>
    </div>
  );
}
