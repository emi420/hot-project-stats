import pandas as pd
import streamlit as st

from process import HUBS, IMPACT_AREAS, fetch_data, get_interval_options


def main():
    st.title("HOTOSM Stats")

    # Hashtag input
    hashtag_input = st.text_input(
        "Hashtag separated by , e.g.: hotosm,missingmaps", value="hotosm"
    )

    # Date and Time Range
    start_date = st.date_input(
        "Start Date", value=pd.to_datetime("2023-04-30 00:00:00")
    )
    end_date = st.date_input("End Date", value=pd.to_datetime("2024-04-30 00:00:00"))

    # Interval options
    interval_options = get_interval_options()
    selected_interval = st.selectbox(
        "Interval", options=[option["label"] for option in interval_options], index=3
    )

    # HOT-Priority-Regions
    selected_hubs = st.multiselect(
        "HOT-Priority-Regions", options=list(HUBS.keys()), default=list(HUBS.keys())[0]
    )

    # HOT-Impact-Areas
    selected_impact_areas = st.multiselect(
        "HOT-Impact-Areas",
        options=list(IMPACT_AREAS.keys()),
        default=list(IMPACT_AREAS.keys())[0],
    )

    hashtags = [s.strip() for s in hashtag_input.split(",") if s.strip()]

    if st.button("Get Statistics"):
        with st.spinner("Loading data..."):
            interval_result, summary_result = fetch_data(
                hashtags,
                start_date,
                end_date,
                next(
                    (
                        option["value"]
                        for option in interval_options
                        if option["label"] == selected_interval
                    ),
                    "P1M",
                ),
                selected_hubs,
                selected_impact_areas,
            )

        st.write("Summary")
        st.write(summary_result)

        st.write("Interval detail")
        st.write(interval_result)


if __name__ == "__main__":
    main()
