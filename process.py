from datetime import datetime

import pandas as pd
import requests

IMPACT_AREAS = {
    "all": "amenity,body_of_water,education,financial,healthcare,lulc,place,poi,commercial,social_facility,wash,waterway",
}


def fetch_data(
    name, id, hashtag, start_date, end_date
):
    topic_data_frames = []
    summary_data_frames = []
    start_date_obj = datetime.combine(start_date, datetime.min.time())
    end_date_obj = datetime.combine(end_date, datetime.max.time())
    topics = IMPACT_AREAS["all"]
    interval_str="P1Y"

    # General stats
    url = f"https://stats.now.ohsome.org/api/stats/{hashtag}/interval?startdate={start_date_obj.isoformat()}Z&enddate={end_date_obj.isoformat()}Z&interval={interval_str}"
    response = requests.get(url)
    df_data = response.json()["result"]
    df = pd.DataFrame(df_data)
    df["hashtag"] = hashtag

    # Topic-wise stats
    url_topics = f"https://stats.now.ohsome.org/api/topic/{topics}/interval?hashtag={hashtag}&startdate={start_date_obj.isoformat()}Z&enddate={end_date_obj.isoformat()}Z&interval={interval_str}"
    response_topics = requests.get(url_topics)
    transformed_data = {}
    for topic, topic_data in response_topics.json()["result"].items():
        topic_values = topic_data["value"]
        start_date = topic_data["startDate"]
        end_date = topic_data["endDate"]
        transformed_data[topic] = topic_values
        transformed_data["startDate"] = start_date
        transformed_data["endDate"] = end_date
        transformed_data["hashtag"] = hashtag

    df_topic = pd.DataFrame(transformed_data)
    topic_data_frames.append(df_topic)

    # Summary
    url_summary = f"https://stats.now.ohsome.org/api/stats/{hashtag}?startdate={start_date_obj.isoformat()}Z&enddate={end_date_obj.isoformat()}Z&interval={interval_str}"
    summary = requests.get(url_summary)

    summary_df = pd.DataFrame(summary.json()["result"], index=[0])
    summary_df["hashtag"] = hashtag
    summary_df["Map Data ID (Name +Date)"] = name + "-" + f"{end_date_obj.isoformat()}Z" if name else f"{end_date_obj.isoformat()}Z"
    summary_df["name"] = name
    summary_df["id"] = id
    summary_df["startDate"] = f"{start_date_obj.isoformat()}Z"
    summary_df["endDate"] = f"{end_date_obj.isoformat()}Z"

    url_summary_topics = f"https://stats.now.ohsome.org/api/topic/{topics}?hashtag={hashtag}&startdate={start_date_obj.isoformat()}Z&enddate={end_date_obj.isoformat()}Z&interval={interval_str}"
    response_summary_topics = requests.get(url_summary_topics)
    for topic, topic_data in response_summary_topics.json()["result"].items():
        topic_value = topic_data["value"]
        summary_df[topic] = topic_value

    summary_data_frames.append(summary_df)

    final_summary_df = pd.concat(summary_data_frames, ignore_index=True)

    primary_fields = ["Map Data ID (Name +Date)", "id", "name", "hashtag","startDate", "endDate"]
    final_summary_df = final_summary_df[
        primary_fields
        + [col for col in final_summary_df.columns if col not in primary_fields]
    ]

    return final_summary_df
