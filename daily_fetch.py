import os
import pandas as pd
import numpy as np
import googleapiclient.discovery

def main():
    # Fetch today's videos
    df_videos = fetch_videos_for_today(query="space news", max_results=5)
    
    # Save to JSON in "records" format
    output_path = os.path.join("DB", "todays_videos.json")
    df_videos.to_json(output_path, orient="records")

if __name__ == "__main__":
    main()

