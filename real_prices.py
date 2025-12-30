import os
from amadeus import Client, ResponseError
from dotenv import load_dotenv

load_dotenv()

amadeus = Client(
    client_id=os.getenv("AMADEUS_API_KEY"),
    client_secret=os.getenv("AMADEUS_API_SECRET")
)

def get_real_price(origin, destination):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            adults=1,
            max=5
        )

        prices = [
            float(offer["price"]["total"])
            for offer in response.data
        ]

        return {
            "min_price": min(prices),
            "avg_price": round(sum(prices) / len(prices), 2),
            "max_price": max(prices),
            "source": "Amadeus"
        }

    except ResponseError as error:
        return {"error": str(error)}
