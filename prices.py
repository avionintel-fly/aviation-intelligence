from datetime import datetime, date
from real_prices import get_real_price


def get_price_intelligence(origin, destination, departure_date):
    origin = origin.upper().strip()
    destination = destination.upper().strip()

    dep_date = datetime.strptime(departure_date, "%Y-%m-%d").date()
    today = date.today()
    days_out = (dep_date - today).days

    real = get_real_price(origin, destination, departure_date)

    if not real or "error" in real:
        return {
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "error": "No pricing data available for this date."
        }

    min_price = real["min_price"]
    avg_price = real["avg_price"]
    max_price = real["max_price"]

    # ---- DATE SANITY LOGIC ----
    if days_out < 21:
        window = "Very close to departure"
        base_confidence = 45
        note = "Prices are volatile close to departure."
    elif days_out <= 180:
        window = "Optimal booking window"
        base_confidence = 80
        note = "Prices are within a reliable prediction window."
    elif days_out <= 330:
        window = "Early booking window"
        base_confidence = 65
        note = "Prices may change as airlines adjust demand."
    else:
        window = "Very early pricing"
        base_confidence = 50
        note = "Prices this far ahead are often placeholders."

    # ---- PRICE SPREAD LOGIC ----
    spread = max_price - min_price
    spread_ratio = spread / avg_price if avg_price else 0

    if spread_ratio > 0.25:
        base_confidence -= 10
        note += " High price variability detected."

    # ---- BUY / WAIT ----
    if min_price < avg_price * 0.95:
        recommendation = "BUY"
        trend = "Below average"
    elif min_price > avg_price * 1.05:
        recommendation = "WAIT"
        trend = "Above average"
    else:
        recommendation = "WAIT"
        trend = "Near average"

    confidence = max(30, min(90, base_confidence))

    return {
        "origin": origin,
        "destination": destination,
        "departure_date": departure_date,
        "days_out": days_out,
        "window": window,
        "note": note,
        "current_price": round(min_price, 2),
        "avg_price": round(avg_price, 2),
        "highest_price": round(max_price, 2),
        "trend": trend,
        "recommendation": recommendation,
        "confidence": confidence,
        "source": "Amadeus"
    }
