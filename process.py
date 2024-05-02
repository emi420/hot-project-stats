from datetime import datetime

import pandas as pd
import requests


def get_interval_options():
    return [
        {"label": "hourly", "value": "PT1H"},
        {"label": "daily", "value": "P1D"},
        {"label": "weekly", "value": "P1W"},
        {"label": "monthly", "value": "P1M"},
        {"label": "quarterly", "value": "P3M"},
        {"label": "yearly", "value": "P1Y"},
    ]


HUBS = {
    "asia-pacific": "AFG,BGD,BTN,BRN,KHM,TLS,FSM,FJI,IND,IDN,KIR,LAO,MYS,MMR,NPL,PAK,PNG,PHL,SLB,LKA,TON,UZB,VUT,VNM,YEM",
    "la-carribean": "ATG,BLZ,BOL,BRA,CHL,CRI,DMA,DOM,ECU,SLV,GTM,GUY,HTI,HND,JAM,MEX,NIC,PAN,PER,TTO,URY,VEN",
    "wna": "DZA,BEN,BFA,CMR,CPV,CAF,TCD,CIV,GNQ,GHA,GIN,GNB,LBR,MLI,MRT,MAR,NER,NGA,STP,SEN,SLE,GMB,TGO",
    "esa": "AGO,BDI,COM,COD,DJI,EGY,SWZ,ETH,KEN,LSO,MDG,MWI,MUS,MOZ,NAM,RWA,SOM,SSD,SDN,TZA,UGA,ZMB,ZWE",
}
IMPACT_AREAS = {
    "disaster": "wash,waterway,social_facility,place,lulc",
    "sus_cities": "wash,waterway,social_facility,lulc,amenity,education,commercial,financial",
    "pub_health": "wash,waterway,social_facility,place,healthcare",
    "migration": "waterway,social_facility,lulc,amenity,education,commercial,healthcare",
    "g_equality": "wash,social_facility,education",
}


def fetch_data(
    hashtags, start_date, end_date, interval, selected_hubs, selected_impact_areas
):
    data_frames = []
    topic_data_frames = []
    summary_data_frames = []
    topics = ",".join(
        ["_".join(IMPACT_AREAS[area].split("_")) for area in selected_impact_areas]
    )
    start_date_obj = datetime.combine(start_date, datetime.min.time())
    end_date_obj = datetime.combine(end_date, datetime.max.time())

    for hub in selected_hubs:
        countries = HUBS[hub].split(",")
        countries_str = ",".join(countries)
        selected_hubs_str = hub
        selected_impact_areas_str = ",".join(selected_impact_areas)

        interval_option = next(
            (
                option
                for option in get_interval_options()
                if option["value"] == interval
            ),
            {"value": "P1M"},
        )
        interval_str = interval_option["value"]

        for hashtag in hashtags:
            # General stats
            url = f"https://stats.now.ohsome.org/api/stats/{hashtag}/interval?startdate={start_date_obj.isoformat()}Z&enddate={end_date_obj.isoformat()}Z&interval={interval_str}&countries={countries_str}"
            response = requests.get(url)
            df_data = response.json()["result"]
            df = pd.DataFrame(df_data)
            df["hashtag"] = hashtag
            df["region"] = selected_hubs_str
            df["impact_area"] = selected_impact_areas_str
            data_frames.append(df)

            # Topic-wise stats
            url_topics = f"https://stats.now.ohsome.org/api/topic/{topics}/interval?hashtag={hashtag}&startdate={start_date_obj.isoformat()}Z&enddate={end_date_obj.isoformat()}Z&countries={countries_str}&interval={interval_str}"
            response_topics = requests.get(url_topics)
            transformed_data = {}
            for topic, topic_data in response_topics.json()["result"].items():
                topic_values = topic_data["value"]
                start_date = topic_data["startDate"]
                end_date = topic_data["endDate"]
                transformed_data[topic] = topic_values
                transformed_data["startDate"] = start_date
                transformed_data["endDate"] = end_date
                transformed_data["region"] = selected_hubs_str
                transformed_data["hashtag"] = hashtag

            df_topic = pd.DataFrame(transformed_data)
            topic_data_frames.append(df_topic)

            # Summary
            url_summary = f"https://stats.now.ohsome.org/api/stats/{hashtag}?startdate={start_date_obj.isoformat()}Z&enddate={end_date_obj.isoformat()}Z&countries={countries_str}"
            summary = requests.get(url_summary)

            summary_df = pd.DataFrame(summary.json()["result"], index=[0])
            summary_df["hashtag"] = hashtag
            summary_df["region"] = selected_hubs_str
            summary_df["impact_area"] = selected_impact_areas_str
            summary_df["startDate"] = f"{start_date_obj.isoformat()}Z"
            summary_df["endDate"] = f"{end_date_obj.isoformat()}Z"

            url_summary_topics = f"https://stats.now.ohsome.org/api/topic/{topics}?hashtag={hashtag}&startdate={start_date_obj.isoformat()}Z&enddate={end_date_obj.isoformat()}Z&countries={countries_str}&interval={interval_str}"
            response_summary_topics = requests.get(url_summary_topics)
            for topic, topic_data in response_summary_topics.json()["result"].items():
                topic_value = topic_data["value"]
                summary_df[topic] = topic_value

            summary_data_frames.append(summary_df)

    final_df = pd.concat(data_frames, ignore_index=True).drop_duplicates()
    final_topic_df = pd.concat(topic_data_frames, ignore_index=True)
    final_summary_df = pd.concat(summary_data_frames, ignore_index=True)

    merged_df = pd.merge(
        final_df,
        final_topic_df,
        left_on=["startDate", "endDate", "region", "hashtag"],
        right_on=["startDate", "endDate", "region", "hashtag"],
        how="inner",
    )

    primary_fields = ["startDate", "endDate", "hashtag", "region", "impact_area"]
    merged_df = merged_df[
        primary_fields + [col for col in merged_df.columns if col not in primary_fields]
    ]
    final_summary_df = final_summary_df[
        primary_fields
        + [col for col in final_summary_df.columns if col not in primary_fields]
    ]

    return merged_df, final_summary_df
