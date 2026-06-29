import { create } from 'zustand';

interface StoreState {
  selectedCountry: string;
  compareCountries: string[];
  yearRange: [number, number];
  setSelectedCountry: (c: string) => void;
  setCompareCountries: (c: string[]) => void;
  setYearRange: (r: [number, number]) => void;
}

export const useStore = create<StoreState>((set) => ({
  selectedCountry: 'United States',
  compareCountries: ['China', 'India'],
  yearRange: [1900, 2022],
  setSelectedCountry: (c) => set({ selectedCountry: c }),
  setCompareCountries: (c) => set({ compareCountries: c }),
  setYearRange: (r) => set({ yearRange: r }),
}));
