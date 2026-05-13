import os

import dotenv
import pandas as pd
import requests
from datetime import datetime

dotenv.load_dotenv()

# topics
TOPICS = ["contributor", "building", "edit", "road", "amenity", "body_of_water",
          "education", "financial", "healthcare", "lulc", "place",
          "poi", "commercial", "social_facility", "wash", "waterway"]

# Monthly interval
INTERVAL = "P1M"

# Tags labels
LABELS = {
    'user': 'Unique Mappers (OSM)',
    'building': 'Buildings Added',
    'road': 'KM Roads Added',
    "amenity": "Amenities Added",
    "body_of_water": "Bodies of Water",
    "education": "Educational Facilities",
    "financial": "Financial Facilities",
    "healthcare": "Healthcare Facilities",
    "lulc": "Land Use/Land Cover",
    "place": "Places Names Added",
    "poi": "Points of Interest",
    "commercial": "Shops",
    "social_facility": "Social Facilities",
    "wash": "WASH Facilities",
    "waterway": "KM Waterways",
}

def fetch_data(
        title, id, hashtags, start_date, end_date
):
    start_date_obj = datetime.combine(start_date, datetime.min.time())
    end_date_obj = datetime.combine(end_date, datetime.max.time())

    partial_dfs = []

    for hashtag in hashtags.split(","):
        topic_df = pd.DataFrame([])
        url = f"https://api.heigit.org/ohsome-now/v1/stats/interval?hashtag={hashtag}&startdate={start_date_obj.isoformat()}Z&enddate={end_date_obj.isoformat()}Z&interval={INTERVAL}&topics={",".join(TOPICS)}"
        response = requests.get(url, headers={"Authorization": f"{os.getenv("HEIGIT_TOKEN")}"})
        result = response.json()["result"]
        for topic, topic_data in result["topics"].items():
            if topic == "user":
                topic_df[LABELS[topic]] = topic_data["value"]
            elif topic in LABELS.keys():
                topic_df[LABELS[topic]] = topic_data["added"]
        topic_df["startDate"] = result["startDate"]
        topic_df["endDate"] = result["endDate"]
        partial_dfs.append(topic_df)

    # Sum
    response_df = pd.concat(partial_dfs).groupby(['startDate', 'endDate']).sum().reset_index()

    # Add extra columns
    response_df["Title"] = title
    response_df["Hashtags"] = hashtags
    response_df["Map Data ID"] = response_df.apply(lambda row: f"MD-{row['Title']}-{row['endDate']}", axis=1)
    response_df["Project ID (From Finance)"] = id

    # Re-order, rename and remove extra columns
    firstColumns = ["Map Data ID", "Project ID (From Finance)", "Title", "Hashtags", "startDate", "endDate"]
    columns = firstColumns + [col for col in response_df.columns if col not in firstColumns]
    response_df = response_df[columns]
    response_df = response_df.rename(columns={
        'startDate': 'Start Date',
        'endDate': 'End Date',
    })

    return response_df
