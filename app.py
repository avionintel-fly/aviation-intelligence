from flask import Flask, render_template, request

# Airport intelligence
from airports import get_intelligent_airports

# Flight price intelligence
from prices import get_price_intelligence

# Price alerts
from alerts import add_alert

app = Flask(__name__)

# -----------------------
# Home page
# -----------------------
@app.route("/")
def home():
    return render_template("home.html")

# -----------------------
# Flight Price Intelligence (BUY / WAIT)
# -----------------------
@app.route("/flight")
def flight():
    origin = request.args.get("origin")
    destination = request.args.get("destination")
    info = None

    if origin and destination:
        info = get_price_intelligence(origin, destination)

    return render_template(
        "flight.html",
        info=info,
        searched=bool(origin and destination)
    )

# -----------------------
# Airport Intelligence (Ranked)
# -----------------------
@app.route("/airport")
def airport():
    city = request.args.get("city")
    airports = []

    if city:
        airports = get_intelligent_airports(city)

    return render_template(
        "airport.html",
        city=city,
        airports=airports
    )

# -----------------------
# Price Alert (Watch price)
# -----------------------
@app.route("/alert", methods=["POST"])
def alert():
    email = request.form.get("email")
    origin = request.form.get("origin")
    destination = request.form.get("destination")
    target_price = request.form.get("target_price")

    add_alert(email, origin, destination, target_price)

    return """
    <h3>✅ Price alert set!</h3>
    <p>We will notify you when the price drops.</p>
    <a href="/flight">Back to Flight Intelligence</a>
    """

# -----------------------
# Run app (MUST BE LAST)
# -----------------------
if __name__ == "__main__":
    app.run()
