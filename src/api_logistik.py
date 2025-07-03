from flask import Flask, jsonify
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["supplychain"]
collection = db["logistikdaten"]

@app.route("/api/logistikdaten")
def get_logistikdaten():
    daten = list(collection.find())
    return dumps(daten)  # bson.json_util.dumps für ObjectId-Kompatibilität

if __name__ == "__main__":
    app.run(debug=True, port=5000)