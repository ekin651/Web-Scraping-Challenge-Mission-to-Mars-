 


from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import webscrapping


app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
@app.route("/")
def home():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = webscrapping.scrape()
    mars.update({}, mars_data, upsert=True)
    return render_template("index.html", mars=mars)
if __name__ == "__main__":
    app.run(debug=True)