import csv
import json
import os

def process_data():
    csv_path = os.path.join("Data_Sets", "global_co2_emissions.csv")
    
    # Columns we actually care about based on Streamlit views
    cols = ["country", "iso_code", "year", "co2", "co2_per_capita", "population", "gdp", 
            "coal_co2", "oil_co2", "gas_co2", "cement_co2",
            "co2_growth_prct", "methane", "nitrous_oxide", "total_ghg",
            "share_global_co2", "temperature_change_from_co2", "temperature_change_from_ghg"]
    
    data_by_country = {}
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        
        # Determine available columns
        available_cols = [c for c in cols if c in headers]
        
        for row in reader:
            country = row.get("country")
            year_str = row.get("year")
            if not country or not year_str:
                continue
                
            try:
                year = int(year_str)
            except:
                continue
                
            if country not in data_by_country:
                iso_code = row.get("iso_code")
                data_by_country[country] = {
                    "iso_code": iso_code if iso_code else None,
                    "data": []
                }
                
            record = {"year": year}
            has_data = False
            for c in available_cols:
                if c not in ["country", "iso_code", "year"]:
                    val_str = row.get(c)
                    if val_str:
                        try:
                            val = float(val_str)
                            record[c] = round(val, 4) if "." in val_str else int(val)
                            has_data = True
                        except ValueError:
                            pass
            
            if has_data:
                data_by_country[country]["data"].append(record)
                
    # Sort data by year for each country
    for country in data_by_country:
        data_by_country[country]["data"] = sorted(data_by_country[country]["data"], key=lambda x: x["year"])
            
    os.makedirs("public", exist_ok=True)
    with open(os.path.join("public", "data.json"), "w", encoding="utf-8") as f:
        json.dump(data_by_country, f, separators=(',', ':'))

if __name__ == "__main__":
    process_data()
    print("Data processed to public/data.json")
