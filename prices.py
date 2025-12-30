from real_prices import get_real_price


def get_price_intelligence(origin, destination):
    """
    Real flight price intelligence using Amadeus data.
    Returns BUY / WAIT recommendation with confidence.
    """

    # Normalize input (Amadeus requires uppercase IATA codes)
    origin = origin.upper().strip()
    destination = destination.upper().strip()

    # Fetch real prices
    real = get_real_price(origin, destination)

    # If API failed or returned nothing
    if not real or "error" in real:
        return {
            "origin": origin,
            "destination": destination,
            "error": "Unable to fetch real-time prices at the moment."
        }

    current_price = real["min_price"]
    avg_price = real["avg_price"]
    highest_price = real["max_price"]

    # Simple but real intelligence logic
    if current_price < avg_price * 0.95:
        trend = "Below average"
        recommendation = "BUY"
        confidence = 75
    elif current_price > avg_price * 1.05:
        trend = "Above average"
        recommendation = "WAIT"
        confidence = 70
    else:
        trend = "Near average"
        recommendation = "WAIT"
        confidence = 60

    return {
        "origin": origin,
        "destination": destination,
        "current_price": round(current_price, 2),
        "avg_price": round(avg_price, 2),
        "lowest_price": round(current_price, 2),
        "highest_price": round(highest_price, 2),
        "trend": trend,
        "recommendation": recommendation,
        "confidence": confidence,
        "source": "Amadeus"
    }
