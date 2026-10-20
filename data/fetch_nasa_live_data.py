"""
Script to download LIVE raw satellite active fire records directly from NASA FIRMS.
Official Source: NASA EOSDIS / NOAA-21 VIIRS 375m Active Fire Data
"""
import urllib.request
import csv
import io
import os

NASA_URL = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-21-viirs-c2/csv/J2_VIIRS_C2_SouthEast_Asia_7d.csv"

def fetch_nasa_kalimantan_fires(max_records=50):
    print(f"Connecting to official NASA FIRMS server:\n{NASA_URL} ...")
    req = urllib.request.Request(NASA_URL, headers={"User-Agent": "Mozilla/5.0"})
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw_data = resp.read().decode("utf-8")
        
    reader = csv.DictReader(io.StringIO(raw_data))
    kalimantan_records = []
    
    for row in reader:
        lat = float(row["latitude"])
        lon = float(row["longitude"])
        # Bounding box for Kalimantan: Latitude [-4.5, 4.5], Longitude [108.0, 119.0]
        if -4.5 <= lat <= 4.5 and 108.0 <= lon <= 119.0:
            kalimantan_records.append(row)
            if len(kalimantan_records) >= max_records:
                break
                
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nasa_raw_kalimantan_fires.csv")
    if kalimantan_records:
        keys = kalimantan_records[0].keys()
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(kalimantan_records)
            
    print(f"\n[SUCCESS] Downloaded {len(kalimantan_records)} real NASA fire detections.")
    print(f"Saved raw verification data to: {output_path}")
    return kalimantan_records

if __name__ == "__main__":
    fires = fetch_nasa_kalimantan_fires(max_records=30)
    print("\nSample Real NASA Satellite Detections in Kalimantan:")
    for f in fires[:5]:
        print(f"  Date: {f['acq_date']} | Lat: {f['latitude']:<9} | Lon: {f['longitude']:<10} | Temp: {f['bright_ti4']} K | Conf: {f['confidence']} | Sat: {f['satellite']}")
