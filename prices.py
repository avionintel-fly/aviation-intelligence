PRICE_DATA = {
    ("NYC", "LON"): {
        "current": 550,
        "avg_30d": 510,
        "lowest_90d": 480
    },
    ("LON", "NYC"): {
        "current": 530,
        "avg_30d": 500,
        "lowest_90d": 470
    }
}

def get_price_intelligence(origin, destination):
    key = (origin.upper(), destination.upper())
    data = PRICE_DATA.get(key)

    if not data:
        return None

    current = data["current"]
    avg = data["avg_30d"]

    if current <= avg:
        recommendation = "BUY"
        confidence = 70
        trend = "Below average"
    else:
        recommendation = "WAIT"
        confidence = 65
        trend = "Above average"

    return {
        "origin": origin.upper(),
        "destination": destination.upper(),
        "current_price": current,
        "avg_price": avg,
        "lowest_price": data["lowest_90d"],
        "recommendation": recommendation,
        "confidence": confidence,
        "trend": trend
    }
