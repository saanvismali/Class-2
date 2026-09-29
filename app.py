from flask import Flask, render_template, render_templates, request
import json
import urllib.request
from urllib.parse import quote

app = Flask(__name__)

def fetch_json(url):
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode("utf-8"))

@app.route("/getweather", methods=["POST" , "GET"])
def get_weather():
    location = request.form.get("city", "").strip() if request.method == "POST" else "Chennai"
    if not location:
        return render_templates("index.html", error="Please enter a city name.")

    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={quote(location)}&count=1&language=en&format=json"
        geo_data = fetch_json(geo_url)

        if not geo_data.get("results"):
            return render_template("index.html", error="City not found. try another one.")


        place = geo_data["results"][0]
        lat = place["latitude"]
        lon = place["longitude"]