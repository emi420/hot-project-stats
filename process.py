import pandas as pd
import requests
from datetime import datetime

# Tags
TAGS = "amenity,body_of_water,education,financial,healthcare,lulc,place,poi,commercial,social_facility,wash,waterway"

# Monthly interval
INTERVAL="P1M"

# Tags labels
LABELS = {
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

        # General stats
        stats_url = f"https://stats.now.ohsome.org/api/stats/{hashtag}/interval?startdate={start_date_obj.isoformat()}Z&enddate={end_date_obj.isoformat()}Z&interval={INTERVAL}"
        response_stats = requests.get(stats_url)
        df_data = response_stats.json()["result"]
        stats_df = pd.DataFrame(df_data)

        # Stats by tag
        tags_df = pd.DataFrame([])
        url = f"https://stats.now.ohsome.org/api/topic/{TAGS}/interval?hashtag={hashtag}&startdate={start_date_obj.isoformat()}Z&enddate={end_date_obj.isoformat()}Z&interval={INTERVAL}"
        
        response = requests.get(url)
        for tag, tag_data in response.json()["result"].items():
            tags_df[LABELS[tag]] = tag_data["added"]
            tags_df["startDate"] = tag_data["startDate"]
            tags_df["endDate"] = tag_data["endDate"]

        # Merge data
        partial_df = pd.merge(stats_df, tags_df, on=["startDate", "endDate"], how="left")
        partial_dfs.append(partial_df)

    # Sum
    response_df = pd.concat(partial_dfs).groupby(['startDate', 'endDate']).sum().reset_index()

    # Add extra columns
    response_df["Title"] = title
    response_df["Hashtags"] = hashtags
    response_df["Map Data ID"] = response_df.apply(lambda row: f"MD-{row['Title']}-{row['endDate']}", axis=1)
    response_df["Project ID (From Finance)"] = id

    # Re-order, rename and remove extra columns
    response_df = response_df.drop('changesets', axis=1)
    response_df = response_df.drop('edits', axis=1)
    firstColumns = ["Map Data ID", "Project ID (From Finance)", "Title", "Hashtags", "startDate", "endDate"]
    columns = firstColumns + [col for col in response_df.columns if col not in firstColumns]
    response_df = response_df[columns]
    response_df = response_df.rename(columns={
        'startDate': 'Start Date', 
        'endDate': 'End Date',
        'users': 'Unique Mappers (OSM)',
        'buildings': 'Buildings Added',
        'roads': 'KM Roads Added',
    })

    return response_df
