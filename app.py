from flask import Flask, jsonify
import os
import json
from flask_cors import CORS
from waitress import serve  # Import Waitress

import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
CORS(app)


handler = RotatingFileHandler('logs/years-today.log', maxBytes=1000000, backupCount=5)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

app.logger.setLevel(logging.INFO)
app.logger.info('MyApp startup')

"""
Get today's videos
"""
@app.route("/api/videos/today", methods=["GET"])
def get_videos_today():

    # Path:
    data_file_path = os.path.join("DB", "videos.json")
    
    if not os.path.exists(data_file_path):
        return jsonify({"error": "No data available for today."}), 404
    
    with open(data_file_path, "r", encoding="utf-8") as f:
        videos_list = json.load(f)  # This will be a list of dictionaries

    print("fetch daily videos")
    app.logger.info("Fetched daily videosss")
    
    # Wrap a dict
    return jsonify({"videos": videos_list})

"""
Get archive videos
"""
@app.route("/api/videos/archive", methods=["GET"])
def get_videos_archive():

    # Path:
    data_file_path = os.path.join("DB", "old_videos.json")
    
    if not os.path.exists(data_file_path):
        return jsonify({"error": "No archive data available."}), 404
    
    with open(data_file_path, "r", encoding="utf-8") as f:
        videos_list = json.load(f)  # This will be a list of dictionaries

    print("fetch archive vids")
    app.logger.info("Fetched archive videos")
    
    # Wrap a dict
    return jsonify({"videos": videos_list})

# Test route
@app.route("/")
def index():
    return "Flask service is up."

if __name__ == "__main__":
    # Serve the app using Waitress
    print("serving app")
    serve(app, host="127.0.0.1", port=5050)
