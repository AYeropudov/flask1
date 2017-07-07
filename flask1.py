from flask import Flask, render_template, request
import json, urllib, urllib3
import feedparser
app = Flask(__name__)

weather_api_server = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=cb22a5d44cba4381795a8b51562e2927"
weather_api_key = "cb22a5d44cba4381795a8b51562e2927"


RRS_FEEDS = {
    'cnn': "http://rss.cnn.com/rss/edition.rss",
    "bbc": "http://feeds.bbci.co.uk/news/rss.xml"
}


@app.route('/', methods=["GET", "POST"])
def get_publication():
    publisher = request.args.get("publisher", "bbc")
    publisher_uri = RRS_FEEDS.get(publisher.lower(), False)
    message = False
    articles = False
    weather = False
    city = request.args.get("city", "London,UK")
    weather = get_weather(city)
    if not publisher_uri:
        message = "Sorry no eny feeds"
        return render_template("feed.html", articles=articles, title=publisher, message=message, weather=weather)

    feed = feedparser.parse(publisher_uri)
    return render_template("feed.html", articles=feed['entries'], title=publisher, message=message, weather=weather)


def get_weather(city):
    city = urllib.parse.quote(city)
    url = weather_api_server.format(city)
    data = request.get_json(url)
    parsed = data
    weather = None
    if parsed.get("weather"):
        weather = {
            "description": parsed["weather"][0]["description"],
            "temperature": parsed["main"]["temp"],
            "city": parsed["name"]
            }
    return weather

if __name__ == '__main__':
    app.run()
