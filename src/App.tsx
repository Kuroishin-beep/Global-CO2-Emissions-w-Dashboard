import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Overview from './pages/Overview';
import Sources from './pages/Sources';
import Comparison from './pages/Comparison';
import MapView from './pages/MapView';
import Predictions from './pages/Predictions';
import Analytics from './pages/Analytics';
import DataPage from './pages/DataPage';
import Info from './pages/Info';
import Insights from './pages/Insights';

function App() {
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden font-sans">
        <Sidebar />
        <div className="flex-1 flex flex-col min-w-0">
          <Header />
          <main className="flex-1 overflow-auto p-4 lg:p-8">
            <Routes>
              <Route path="/" element={<Navigate to="/overview" replace />} />
              <Route path="/overview" element={<Overview />} />
              <Route path="/sources" element={<Sources />} />
              <Route path="/comparison" element={<Comparison />} />
              <Route path="/map" element={<MapView />} />
              <Route path="/predictions" element={<Predictions />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/data" element={<DataPage />} />
              <Route path="/info" element={<Info />} />
              <Route path="/insights" element={<Insights />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
