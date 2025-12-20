AIRPORTS = {
    "london": [
        {"code": "LHR", "name": "Heathrow Airport", "distance_km": 23, "avg_price": 550},
        {"code": "LGW", "name": "Gatwick Airport", "distance_km": 47, "avg_price": 480},
        {"code": "STN", "name": "Stansted Airport", "distance_km": 64, "avg_price": 420},
    ],
    "new york": [
        {"code": "JFK", "name": "John F. Kennedy International", "distance_km": 26, "avg_price": 520},
        {"code": "EWR", "name": "Newark Liberty International", "distance_km": 24, "avg_price": 500},
        {"code": "LGA", "name": "LaGuardia Airport", "distance_km": 13, "avg_price": 540},
    ]
}

def score_airports(airports):
    scored = []

    for a in airports:
        distance_score = max(0, 100 - a["distance_km"])   # closer = higher score
        price_score = max(0, 100 - (a["avg_price"] / 10)) # cheaper = higher score

        total_score = round((distance_score * 0.6) + (price_score * 0.4), 2)

        a["score"] = total_score
        scored.append(a)

    return sorted(scored, key=lambda x: x["score"], reverse=True)

def get_intelligent_airports(city):
    city = city.lower()
    airports = AIRPORTS.get(city, [])
    return score_airports(airports)

