

export default function MapView() {
  return (
    <div className="flex flex-col items-center justify-center h-full text-slate-400 space-y-4">
      <div className="text-6xl">🗺️</div>
      <h2 className="text-xl">Map View</h2>
      <p className="text-sm max-w-md text-center">
        Map visualizations require heavy GeoJSON datasets or map libraries (like Leaflet/Mapbox). 
        To keep this app lightweight and efficient, complex 3D mapping is disabled in this minimalist version.
      </p>
    </div>
  );
}
