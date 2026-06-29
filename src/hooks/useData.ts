import { useState, useEffect } from 'react';

export interface Co2Record {
  year: number;
  co2?: number;
  co2_per_capita?: number;
  population?: number;
  gdp?: number;
  coal_co2?: number;
  oil_co2?: number;
  gas_co2?: number;
  cement_co2?: number;
  co2_growth_prct?: number;
  methane?: number;
  nitrous_oxide?: number;
  total_ghg?: number;
  share_global_co2?: number;
  temperature_change_from_co2?: number;
  temperature_change_from_ghg?: number;
}

export interface CountryData {
  iso_code: string | null;
  data: Co2Record[];
}

export interface GlobalData {
  [countryName: string]: CountryData;
}

let cachedData: GlobalData | null = null;

export function useData() {
  const [data, setData] = useState<GlobalData | null>(cachedData);
  const [loading, setLoading] = useState(!cachedData);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (cachedData) return;
    
    fetch('/api/data')
      .then(res => {
        if (!res.ok) throw new Error("Failed to load data");
        return res.json();
      })
      .then(json => {
        cachedData = json;
        setData(json);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return { data, loading, error };
}
