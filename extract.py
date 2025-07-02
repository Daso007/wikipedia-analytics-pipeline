import requests
import os
import json
from datetime import datetime , timedelta, timezone

def fetch_wikipedia_pageviews(year,month,day,hour):
    """
    Fetch the top 100 most viewed wikipedia articles for a specific hour.

    API Documentation: https://wikitech.wikimedia.org/wiki/Analytics/AQS/Pageviews
    """

    print(f"Fetching data for {year}-{month:02d}-{day:02d} at {hour:02d}:00 UTC...")

    API_URL = (
        f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/"
        f"{year}/{month:02d}/{day:02d}"
    )


    HEADERS = {
        'User-Agent': 'wikipedia-analytics-pipeline (dibyajyotidatta410@gmail.com)'
    } 
    try:

        response = requests.get(API_URL, headers = HEADERS)

        response.raise_for_status()

        data = response.json()
        print("Data fetched successfully!")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

        return None

def save_data_to_file(data,year,month,day):
    """
    Saves the fetched data to a JSON file in a structured folder.
    """

    if not data:
        print("Not data to save.")
        return
    
    dir_path =f"data/raw/{year}/{month:02d}/{day:02d}"
    os.makedirs(dir_path, exist_ok = True)

    file_path = f"{dir_path}/daily_top_views.json"

    try:
        with open(file_path,'w', encoding = 'utf-8') as f:
            json.dump(data,f,ensure_ascii= False, indent = 4)

            print(f"Data saved successfully to {file_path}")

    except IOError as e:
        print(f"Error saving data to file: {e}")


if __name__ == "__main__":
    now = datetime.now(timezone.utc)
    target_datetime = now - timedelta(days=1)
    year = target_datetime.year
    month = target_datetime.month
    day = target_datetime.day

    

    pageviews_data = fetch_wikipedia_pageviews(year,month,day,0)

    save_data_to_file(pageviews_data,year,month,day)
