from flask import Flask, jsonify
import os
import json
from flask_cors import CORS
from waitress import serve  # Import Waitress

import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
CORS(app)

# ---- logger stuff
handler = RotatingFileHandler('logs/years-today.log', maxBytes=1000000, backupCount=5)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

app.logger.setLevel(logging.INFO)
app.logger.info('years.today startup')

# ---- AWS stuff 
from botocore.exceptions import ClientError
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

import os
from dotenv import load_dotenv
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name = AWS_DEFAULT_REGION
)

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Specify your table
table = dynamodb.Table('videos')

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
    app.logger.info("Fetched daily videos")
    
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

"""
Get archive videos
"""
@app.route("/api/videos/todaytest", methods=["GET"])
def get_videos_today_test():
    try:
        # 1. Determine today's month and day in UTC
        today = datetime.utcnow()
        month_day = today.strftime('%m-%d')  # Format: 'MM-DD'

        # Tests:
        print(type(month_day))
        print(month_day)
        month_day = '11-11'


        app.logger.info(f"Fetching videos for month-day: {month_day}")
        
        # 2. Build the FilterExpression using Attr
        # Assuming datePublished is in ISO 8601 format: 'YYYY-MM-DDTHH:MM:SSZ'
        # We extract '-MM-DD' to match any year
        filter_expression = Attr('datePublished').contains(f'-{month_day}')
        
        # 3. Perform the Scan operation with the FilterExpression
        response = table.scan(
            FilterExpression=filter_expression
        )
        
        items = response.get('Items', [])
        app.logger.info(f"Number of items fetched in first scan: {len(items)}")
        
        # 4. Handle pagination if necessary
        while 'LastEvaluatedKey' in response:
            response = table.scan(
                FilterExpression=filter_expression,
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            fetched_items = response.get('Items', [])
            items.extend(fetched_items)
            app.logger.info(f"Number of items fetched in subsequent scan: {len(fetched_items)}")
        
        # 5. Transform the data to the desired format
        videos = []
        for item in items:
            video = {
                "author": item.get('author', ''),
                "datePublished": item.get('datePublished', ''),
                "description": item.get('description', ''),
                "id": item.get('videoId', ''),
                "link": item.get('link', ''),
                "title": item.get('title', ''),
                "viewCount": str(item.get('viewCount', '0'))  # Convert to string as per API spec
            }
            videos.append(video)
        
        app.logger.info(f"Total videos to return: {len(videos)}")
        
        # 6. Return the response
        return jsonify({"videos": videos}), 200

    except ClientError as e:
        app.logger.error(f"DynamoDB ClientError: {e.response['Error']['Message']}")
        return jsonify({"error": e.response['Error']['Message']}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Test route
@app.route("/")
def index():
    return "Flask service is up."

if __name__ == "__main__":
    # Serve the app using Waitress
    print("serving app")
    serve(app, host="127.0.0.1", port=5050)
