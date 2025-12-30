from global_airports import AIRPORTS_BY_IATA, AIRPORTS_BY_CITY, AIRPORTS_BY_NAME

# Only commercial airports suitable for flights
ALLOWED_TYPES = {"large_airport", "medium_airport"}


def score_airport(airport, query_city=None):
    score = 0

    # Strong preference for large airports
    if airport["type"] == "large_airport":
        score += 150
    elif airport["type"] == "medium_airport":
        score += 80

    # Prefer airports whose city contains the query city
    if query_city and airport.get("city"):
        if query_city.lower() in airport["city"].lower():
            score += 50

    return score


def resolve_location(user_input: str):
    if not user_input or not user_input.strip():
        return {
            "type": "unknown",
            "message": "Empty input"
        }

    raw = user_input.strip().upper()
    norm = user_input.strip().lower()

    # -------------------------------------------------
    # 1️⃣ Exact IATA code (JFK, LHR, HND)
    # -------------------------------------------------
    if raw in AIRPORTS_BY_IATA:
        airport = AIRPORTS_BY_IATA[raw]
        return {
            "type": "airport",
            "airports": [airport],
            "primary": airport
        }

    # -------------------------------------------------
    # 2️⃣ City match (PARTIAL, NOT EXACT)
    # -------------------------------------------------
    city_matches = []

    for city_key, airports in AIRPORTS_BY_CITY.items():
        if norm in city_key:
            for airport in airports:
                if airport["type"] in ALLOWED_TYPES:
                    city_matches.append(airport)

    if city_matches:
        city_matches.sort(
            key=lambda a: score_airport(a, user_input),
            reverse=True
        )

        return {
            "type": "city",
            "city": user_input.title(),
            "airports": city_matches,
            "primary": city_matches[0]
        }

    # -------------------------------------------------
    # 3️⃣ Airport name match (Heathrow, Haneda)
    # -------------------------------------------------
    name_matches = [
        airport
        for name, airport in AIRPORTS_BY_NAME.items()
        if norm in name
        and airport["type"] in ALLOWED_TYPES
    ]

    if name_matches:
        name_matches.sort(
            key=lambda a: score_airport(a, user_input),
            reverse=True
        )

        return {
            "type": "airport",
            "airports": name_matches,
            "primary": name_matches[0]
        }

    # -------------------------------------------------
    # 4️⃣ Not found
    # -------------------------------------------------
    return {
        "type": "unknown",
        "message": f"Could not resolve location: '{user_input}'"
    }
