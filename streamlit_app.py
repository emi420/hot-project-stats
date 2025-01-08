import pandas as pd
import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta

from process import fetch_data

def main():
    st.title("HOT Projects Stats")

    # Initialize data
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame([{
            "Project Id (from finance)": "",
            "Title": "",
            "Hashtag": ""
        }])

    # Date and Time Range
    start_date = st.date_input("Start Date", value=datetime.now().replace(day=1)+relativedelta(months=-1))
    end_date = st.date_input("End Date", value=datetime.now().replace(day=1))

    st.write("---") 

    # Display editable table
    if len(st.session_state.data) > 0:
        edited_df = st.data_editor(
            st.session_state.data, 
            hide_index=True,
            num_rows="dynamic",
            column_config={
                "Id": st.column_config.Column(
                    "Id",
                    width="medium",
                    required=False,
                ),
                "Hashtag": st.column_config.Column(
                    "Hashtag",
                    width="medium",
                    required=True,
                ),
                "Title": st.column_config.Column(
                    "Title",
                    width="medium",
                    required=False,
                )
            }, 
        )

        # Get stats
        data = []
        if st.button("Get Statistics", type="primary"):
            with st.spinner("Loading data..."):
                for index, row in edited_df.iterrows():
                    if row["Hashtag"]:
                        interval_result = fetch_data(
                            row["Title"],
                            row["Project Id (from finance)"],
                            row["Hashtag"].replace("#", ""),
                            start_date,
                            end_date,
                        )
                        data.append(interval_result)

        # Display results
        if data:
            st.write("Summary")
            st.write(pd.concat(data, ignore_index=True))

if __name__ == "__main__":
    main()
