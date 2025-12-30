import csv
from collections import defaultdict

AIRPORTS_BY_IATA = {}
AIRPORTS_BY_CITY = defaultdict(list)
AIRPORTS_BY_NAME = {}

DATA_FILE = "data/airports.csv"

def load_airports():
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            iata = row.get("iata_code")
            name = row.get("name")
            city = row.get("municipality")
            country = row.get("iso_country")
            lat = row.get("latitude_deg")
            lon = row.get("longitude_deg")
            airport_type = row.get("type")

            if not iata:
                continue

            record = {
                "iata": iata.upper(),
                "name": name,
                "city": city,
                "country": country,
                "lat": float(lat) if lat else None,
                "lon": float(lon) if lon else None,
                "type": airport_type
            }

            AIRPORTS_BY_IATA[iata.upper()] = record

            if city:
                AIRPORTS_BY_CITY[city.lower()].append(record)

            if name:
                AIRPORTS_BY_NAME[name.lower()] = record

# Load airport data at import time
load_airports()
